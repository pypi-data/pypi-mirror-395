from typing import Iterator, Dict, Literal, TypedDict, Optional
from datetime import date
import logging
from dataclasses import dataclass, replace as dataclass_replace

import requests

from .common import get_http_proxies, HTTPError, BaseClient, BaseClientSettings, debug_log_response


API_ROOT = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app"


class LegifranceTokens(TypedDict):
    token_type: str
    access_token: str


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class LegifranceSettings(BaseClientSettings):
    client_id: str
    client_secret: str


@dataclass(frozen=True)
class LegifranceClient(BaseClient[LegifranceSettings]):
    settings: LegifranceSettings
    tokens: Optional[LegifranceTokens] = None


def authenticate(client: LegifranceClient) -> LegifranceClient:
    auth_response = requests.post(
        "https://oauth.piste.gouv.fr/api/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client.settings.client_id,
            "client_secret": client.settings.client_secret,
            "scope": "openid"
        },
        proxies=get_http_proxies(client.settings)
    )
    if auth_response.status_code != 200:
        raise HTTPError(response=auth_response)

    return dataclass_replace(
        client,
        tokens=auth_response.json(),
    )


def list_codes(client: LegifranceClient) -> Iterator[Dict]:
    # Pagination seems to be broken on the API side,
    # so we have to fetch all codes in one go.
    response = client.request_session.post(
        f"{API_ROOT}/list/code",
        json={
            "pageSize": 1000,
            "pageNumber": 1
        },
        headers=_get_http_headers(client),
        proxies=get_http_proxies(client.settings)
    )
    debug_log_response(LOGGER, response)

    if response.status_code != 200:
        raise HTTPError(response=response)

    results = response.json()['results']
    if len(results) == 0:
        raise RuntimeError("No code found")

    for code in results:
        yield code


def get_code_summary(client: LegifranceClient, code_id: str):
    response = client.request_session.post(
        f"{API_ROOT}/consult/legi/tableMatieres",
        json={
            "textId": code_id,
            "date": date.today().strftime(r'%Y-%m-%d'),
            "nature": "CODE",
        },
        headers=_get_http_headers(client),
        proxies=get_http_proxies(client.settings)
    )
    debug_log_response(LOGGER, response)

    if response.status_code != 200:
        raise HTTPError(response=response)
    return response.json()


def get_article(client: LegifranceClient, article_id: str):
    response = client.request_session.post(
        f"{API_ROOT}/consult/getArticle",
        json={
            "id": article_id,
        },
        headers=_get_http_headers(client),
        proxies=get_http_proxies(client.settings)
    )
    debug_log_response(LOGGER, response)

    if response.status_code != 200:
        raise HTTPError(response=response)
    return response.json()


def get_texte_jorf(client: LegifranceClient, texte_cid: str):
    response = client.request_session.post(
        f"{API_ROOT}/consult/jorf",
        json={
            "textCid": texte_cid,
        },
        headers=_get_http_headers(client),
        proxies=get_http_proxies(client.settings)
    )
    debug_log_response(LOGGER, response)

    if response.status_code != 200:
        raise HTTPError(response=response)
    return response.json()


def search_arrete(client: LegifranceClient, date: date, title: str) -> Iterator[Dict]:
    yield from _search_with_date(
        client, date, 'ARRETE', {'TITLE': title}
    )


def search_decret(
    client: LegifranceClient,
    date: date,
    num: str | None,
    title: str | None,
) -> Iterator[Dict]:
    if not num and not title:
        raise ValueError('Either num or title must be provided')
    if num:
        yield from _search_with_date(
            client, date, 'DECRET', {'NUM': num}
        )
    if title:
        yield from _search_with_date(
            client, date, 'DECRET', {'TITLE': title}
        )


def search_circulaire(client: LegifranceClient, date: date, title: str) -> Iterator[Dict]:
    yield from _search_with_date(
        client, date, 'CIRCULAIRE', {'TITLE': title}
    )


def build_jorf_url(cid: str):
    return f"https://www.legifrance.gouv.fr/jorf/id/{cid}"


def build_code_site_url(code_cid: str):
    return f"https://www.legifrance.gouv.fr/codes/texte_lc/{code_cid}"


def build_code_article_site_url(article_id: str):
    return f"https://www.legifrance.gouv.fr/codes/article_lc/{article_id}"


def iter_articles(parent_sections):
    parent_section = parent_sections[-1]
    if parent_section['sections']:
        for section in parent_section['sections']:
            yield from iter_articles(parent_sections + [section])
    else:
        for article in parent_section['articles']:
            yield parent_sections, article


def _search_with_date(
    client: LegifranceClient,
    date: date,
    nature: Literal['DECRET', 'ARRETE', 'CIRCULAIRE'],
    criteria: Dict[Literal['NUM', 'TITLE'], str]
) -> Iterator[Dict]:
    fond = dict(
        DECRET='LODA_DATE',
        ARRETE='LODA_DATE',
        CIRCULAIRE='JORF',
    )[nature]
    current_page = 1
    page_size = 10
    date_str = date.strftime(r'%Y-%m-%d')
    while True:
        response = client.request_session.post(
            f"{API_ROOT}/search",
            json={
                "recherche": {
                    "filtres": [
                        {
                            "valeurs": [nature],
                            "facette": "NATURE"
                        },
                        {
                            "dates": {
                                "start": date_str,
                                "end": date_str,
                            },
                            "facette": "DATE_SIGNATURE"
                        }
                    ],
                    "sort": "SIGNATURE_DATE_DESC",
                    "secondSort": "ID",
                    "champs": [
                        {
                            "criteres": [{
                                "proximite": 2,
                                "valeur": value,
                                "operateur": "ET",
                                "typeRecherche": "UN_DES_MOTS"
                            }],
                            "operateur": "ET",
                            "typeChamp": key
                        } for key, value in criteria.items()
                    ],
                    "pageSize": page_size,
                    "operateur": "ET",
                    "typePagination": "DEFAUT",
                    "pageNumber": current_page
                },
                "fond": fond
            },
            headers=_get_http_headers(client),
            proxies=get_http_proxies(client.settings)
        )
        debug_log_response(LOGGER, response)

        if response.status_code != 200:
            raise HTTPError(response=response)

        yield from response.json()['results']

        if response.json()['totalResultNumber'] <= current_page * page_size:
            break
        current_page += 1
    return response.json()


def _get_http_headers(client: LegifranceClient):
    if client.tokens is None:
        raise ValueError("Client is not authenticated")
    return {
        "Authorization": f"{client.tokens['token_type']} {client.tokens['access_token']}",
        "Content-Type": "application/json",
    }


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s %(levelname)s %(message)s',
    )

    client = LegifranceClient(
        settings=LegifranceSettings(
            client_id=os.environ['LEGIFRANCE_CLIENT_ID'],
            client_secret=os.environ['LEGIFRANCE_CLIENT_SECRET'],
        )
    )
    client = authenticate(client)

    print([result['titles'] for result in search_arrete(client, date(2016, 5, 23), (
        "relatif aux installations de production de chaleur et/ou d'électricité"
        " à partir de déchets non dangereux préparés"
    ))])
