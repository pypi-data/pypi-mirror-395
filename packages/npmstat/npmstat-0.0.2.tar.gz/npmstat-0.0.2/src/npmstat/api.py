from typing import Optional

from requests_cache import CachedResponse, CachedSession, OriginalResponse


session = CachedSession("npmstat", use_cache_dir=True, expire_after=3600 * 4)

session.headers.update({"user-agent": "requests/npmstat"})


def get_package(name: str, version: Optional[str] = None) -> OriginalResponse | CachedResponse:
    url = f"https://registry.npmjs.org/{name}"
    if version:
        url += f"/{version}"
    r = session.get(url)
    r.raise_for_status()
    return r


def get_downloads(name: str, period: str = "last-day", is_range=False) -> OriginalResponse | CachedResponse:
    period_type = "range" if is_range else "point"
    url = f"https://api.npmjs.org/downloads/{period_type}/{period}/{name}"
    r = session.get(url)
    r.raise_for_status()
    return r
