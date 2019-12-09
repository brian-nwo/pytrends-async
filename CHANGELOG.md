# ChangeLog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## 0.3.0 (2019-12-08)

### Added
- Retry support has been reintroduced (back by tenacity). Retry settings only apply when proxies are not in use.
- Python 3.8 is now offically tested and supported.

### Changed
- Reintroduced `retries` and `backoff_factor` to `TrendsReq.__init__()`. `retries` and `backoff_factor` are disabled by default (set to 0). These parameters will only affect retrying if proxies are not in use. 
- Proxies that return a 429 (Too Many Requests) will no longer be removed the proxy list. Instead, another proxy (or no proxy if all proxies have been exausted) will be used in the next request.
- Proxies that trigger an error that is not caused by a 429 response code (ConnectionRefusedError, SSLError) will be placed in `TrendReq.blacklisted_proxies` instead of removed from the proxies list.
- Underyling httpx library has been updated to version 0.9.3.

### Fixed
- `dailydata.py` now uses `asyncio.sleep` instead of `time.sleep`.

## 0.2.1 (2019-12-04)

### Changed
- Fixed importing issue

## 0.2.0 (2019-12-04)

### Added
- This changelog :)
- Proxy support has been introduced but still needs further testing.

### Changed
- `GetNewProxy()` replaced with internal method `_iterate_proxy()`
- Protocol changed from HTTP/2 to HTTP/1.1. This resolves a KeyError that was occurring with the underlying http2 lib.
- HTTP connections are now properly cleaned up after use.

## 0.1.0 (2019-12-01)

- Initial release of pytrends-async for testing purposes.

