from typing import Optional

from requests_cache import CachedResponse, CachedSession, OriginalResponse

from ._version import __version__


session = CachedSession("npmstat", use_cache_dir=True, expire_after=3600)

session.headers.update({"user-agent": f"requests/npmstat-{__version__}"})


def get_package(name: str, version: Optional[str] = None, **kwargs) -> OriginalResponse | CachedResponse:
    url = f"https://registry.npmjs.org/{name}"
    if version:
        url += f"/{version}"
    r = session.get(url, **kwargs)
    r.raise_for_status()
    return r


def get_downloads(
    name: str, period: str = "last-day", get_range: bool = False, **kwargs
) -> OriginalResponse | CachedResponse:
    period_type = "range" if get_range else "point"
    url = f"https://api.npmjs.org/downloads/{period_type}/{period}/{name}"
    r = session.get(url, **kwargs)
    r.raise_for_status()
    return r
