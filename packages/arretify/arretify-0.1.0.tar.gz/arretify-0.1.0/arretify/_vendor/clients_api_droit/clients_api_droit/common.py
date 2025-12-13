from typing import Optional, TypeVar, Generic
import logging
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import mkdtemp
from functools import cached_property

from requests.exceptions import HTTPError as RequestsHTTPError
from requests_cache import CachedSession, CachedResponse


GenericClientSettings = TypeVar("GenericClientSettings", bound="BaseClientSettings")


class HTTPError(RequestsHTTPError):
    def __str__(self):
        url = self.response.request.url
        method = self.response.request.method
        formatted_error_msg = self.response.text
        if self.response.headers.get('Content-Type') == 'application/json':
            error_data = self.response.json()
            formatted_error_msg = error_data.get('error_description') or formatted_error_msg
        return f"{method} {url} - HTTP {self.response.status_code} \n\"{formatted_error_msg}\""


@dataclass(frozen=True, kw_only=True)
class BaseClientSettings:
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None
    tmp_dir: Path = field(
        default_factory=lambda: Path(mkdtemp(prefix='clients-api-droit-'))
    )


@dataclass(frozen=True, kw_only=True)
class BaseClient(Generic[GenericClientSettings]):
    settings: GenericClientSettings

    @cached_property
    def request_session(self):
        return CachedSession(
            cache_name=self.settings.tmp_dir / 'clients-api-droit_requests-cache',
            backend='sqlite',
            expire_after=3600 * 24,  # 1 day
            allowable_methods=('GET', 'POST')
        )

    @property
    def zeep_cache_path(self) -> Path:
        return self.settings.tmp_dir / 'clients-api-droit_zeep-cache.db'

    def __post_init__(self):
        if not self.settings.tmp_dir.exists():
            self.settings.tmp_dir.mkdir(parents=True, exist_ok=True)


def debug_log_response(logger: logging.Logger, response: CachedResponse):
    logger.debug(
        f"Response <from cache={response.from_cache}>: {
            response.status_code} {response.request.method} {response.url}"
    )


def get_http_proxies(settings: BaseClientSettings):
    http_proxies = dict()
    if settings.http_proxy:
        http_proxies["http"] = settings.http_proxy
    if settings.https_proxy:
        http_proxies["https"] = settings.https_proxy
    return http_proxies