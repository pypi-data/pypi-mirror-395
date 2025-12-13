import logging
from typing import Dict, Iterator, Literal, Optional
from pathlib import Path
from functools import cached_property
from dataclasses import dataclass

from lxml import etree
import zeep
from zeep.cache import SqliteCache as ZeepSqliteCache
from zeep.wsse.username import UsernameToken as ZeepUsernameToken

from .common import HTTPError, get_http_proxies, BaseClientSettings, BaseClient


SITE_ROOT = 'https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/'
CURRENT_DIR = Path(__file__).parent
WSDL_PATH = CURRENT_DIR / 'eurlex-ws.xml'


ActType = Literal['directive', 'regulation', 'decision']


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EurlexSettings(BaseClientSettings):
    web_service_username: str
    web_service_password: str


@dataclass(frozen=True, kw_only=True)
class EurlexClient(BaseClient[EurlexSettings]):
    settings: EurlexSettings

    @cached_property
    def zeep_client(self) -> zeep.client.Client:
        cache = ZeepSqliteCache(path=self.zeep_cache_path, timeout=60)
        transport = zeep.transports.Transport(cache=cache)
        # Use raw response because something seems broken.
        # See : https://github.com/mvantellingen/python-zeep/issues/1457
        zeep_settings = zeep.settings.Settings(raw_response=True)
        return zeep.client.Client(
            wsdl=str(WSDL_PATH),
            wsse=ZeepUsernameToken(
                self.settings.web_service_username,
                self.settings.web_service_password,
            ),
            transport=transport,
            settings=zeep_settings,
        )


def get_eur_lex_html(client: BaseClient, textId: str):
    url = f'{SITE_ROOT}?uri={textId}'
    response = client.request_session.get(
        url,
        proxies=get_http_proxies(client.settings),
    )
    if response.status_code != 200:
        raise HTTPError(response=response)
    return {
        'html': response.text,
        'url': url,
    }


def search_act(client: EurlexClient, act_type: ActType, year: int, number: int) -> Iterator[Dict]:
    # Pad number starting with zeros to have 4 digits
    padded_number = str(number).zfill(4)

    # Queries obtained using the advanced search form :
    #   https://eur-lex.europa.eu/advanced-search-form.html
    # testing for results, and then switching to expert search form.
    if act_type == 'directive':
        query = (
            f"DTS_SUBDOM = LEGISLATION AND ((DTA = {year} AND DTN = {padded_number}))"
            " AND DTC = false AND (FM_CODED = DIR OR DIR_DEL OR DIR_IMPL)"
        )
    elif act_type == 'decision':
        query = (
            f"DTS_SUBDOM = LEGISLATION AND ((DTA = {year} AND DTN = {padded_number}))"
            " AND (FM_CODED = DEC_ENTSCHEID OR DEC_DEL OR DEC_FRAMW OR DEC_IMPL"
            " OR JOINT_DEC OR DEC OR DEC_ADOPT_INTERNATION)"
        )
    elif act_type == 'regulation':
        query = (
            f"DTS_SUBDOM = LEGISLATION AND ((DTA = {year} AND DTN = {padded_number}))"
            " AND (FM_CODED = REG OR REG_DEL OR REG_FINANC OR REG_IMPL"
            " OR REG_ADOPT_INTERNATION)"
        )

    response = client.zeep_client.service.doQuery(
        expertQuery=query, 
        page=1, 
        pageSize=10, 
        searchLanguage="fr"
    )
    root = etree.fromstring(response.content)
    results = root.findall('.//{http://eur-lex.europa.eu/search}result')
    for result in results:
        document_link = result.find(
            "{http://eur-lex.europa.eu/search}document_link[@type='html']")
        if document_link is None:
            document_link = result.find(
                "{http://eur-lex.europa.eu/search}document_link[@type='pdf']")
        if document_link is None:
            raise ValueError('No document link found')

        yield dict(
            url=document_link.text
        )


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()

    client = EurlexClient(
        settings=EurlexSettings(
            web_service_username=os.environ['EURLEX_WEB_SERVICE_USERNAME'],
            web_service_password=os.environ['EURLEX_WEB_SERVICE_PASSWORD'],
            tmp_dir=Path('./tmp'),
        )
    )

    print('regulation 1996/2', list(search_act(client, 'regulation', 1996, 2)))
    print('directive 2010/75', list(search_act(client, 'directive', 2010, 75)))
    print('decision 2023/10', list(search_act(client, 'decision', 2023, 10)))
    print('regulation 2003/87', list(search_act(client, 'regulation', 2003, 87)))

    # law_html = get_eur_lex_html('CELEX:02023R1542-20240718')
    # print(law_html)
