# ChangeLog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

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

