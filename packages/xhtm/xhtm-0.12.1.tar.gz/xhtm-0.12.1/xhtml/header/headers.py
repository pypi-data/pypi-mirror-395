# coding:utf-8

from enum import Enum
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import overload


class RequestLine():
    """HTTP requests

    Reference:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages#http_requests
    """

    def __init__(self, request_line: str):
        method, target, protocol = request_line.split()
        self.__protocol: str = protocol.strip()
        self.__method: str = method.strip()
        self.__target: str = target.strip()

    @property
    def protocol(self) -> str:
        return self.__protocol

    @property
    def method(self) -> str:
        return self.__method

    @property
    def target(self) -> str:
        return self.__target


class StatusLine():
    """HTTP responses

    Reference:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages#http_responses
    """

    def __init__(self, status_line: str):
        protocol, status_code, status_text = status_line.split(maxsplit=2)
        self.__status_code: int = int(status_code.strip())
        self.__status_text: str = status_text.strip()
        self.__protocol: str = protocol.strip()

    @property
    def protocol(self) -> str:
        return self.__protocol

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def status_text(self) -> str:
        return self.__status_text


class Headers(Enum):
    """HTTP headers

    Reference:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers

    In HTTP/1.X, a header is a case-insensitive name followed by
    a colon, then optional whitespace which will be ignored, and
    finally by its value (for example: Allow: POST).

    In HTTP/2 and above, headers are displayed in lowercase when
    viewed in developer tools (accept: */*), and prefixed with a
    colon for a special group of pseudo-headers (:status: 200).
    """
    ACCEPT = "Accept"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    ACCEPT_RANGES = "Accept-Ranges"
    ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
    ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
    ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ACCESS_CONTROL_EXPOSE_HEADERS = "Access-Control-Expose-Headers"
    ACCESS_CONTROL_MAX_AGE = "Access-Control-Max-Age"
    ACCESS_CONTROL_REQUEST_HEADERS = "Access-Control-Request-Headers"
    ACCESS_CONTROL_REQUEST_METHOD = "Access-Control-Request-Method"
    AGE = "Age"
    ALLOW = "Allow"
    AUTHORIZATION = "Authorization"
    CACHE_CONTROL = "Cache-Control"
    CONNECTION = "Connection"
    CONTENT_DISPOSITION = "Content-Disposition"
    CONTENT_ENCODING = "Content-Encoding"
    CONTENT_LANGUAGE = "Content-Language"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_LOCATION = "Content-Location"
    CONTENT_RANGE = "Content-Range"
    CONTENT_TYPE = "Content-Type"
    COOKIE = "Cookie"
    DATE = "Date"
    ETAG = "ETag"
    EXPIRES = "Expires"
    FROM = "From"
    HOST = "Host"
    IF_MATCH = "If-Match"
    IF_MODIFIED_SINCE = "If-Modified-Since"
    IF_NONE_MATCH = "If-None-Match"
    IF_RANGE = "If-Range"
    IF_UNMODIFIED_SINCE = "If-Unmodified-Since"
    KEEP_ALIVE = "Keep-Alive"
    LAST_MODIFIED = "Last-Modified"
    LOCATION = "Location"
    MAX_FORWARDS = "Max-Forwards"
    ORIGIN = "Origin"
    PRAGMA = "Pragma"
    PROXY_AUTHENTICATE = "Proxy-Authenticate"
    PROXY_AUTHORIZATION = "Proxy-Authorization"
    RANGE = "Range"
    REFERER = "Referer"
    RETRY_AFTER = "Retry-After"
    SERVER = "Server"
    SET_COOKIE = "Set-Cookie"
    TE = "TE"
    TRAILER = "Trailer"
    TRANSFER_ENCODING = "Transfer-Encoding"
    UPGRADE = "Upgrade"
    USER_AGENT = "User-Agent"
    VARY = "Vary"
    VIA = "Via"
    WARNING = "Warning"

    @property
    def http2(self):
        return self.value.lower()


class HeaderMapping():

    def __init__(self, headers: Iterable[Tuple[str, str]] = []) -> None:
        self.__headers: Dict[str, str] = {k.lower(): v for k, v in headers}

    def __len__(self) -> int:
        return len(self.__headers)

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(self.__headers.items())

    def __getitem__(self, key: str) -> str:
        return self.__headers[key.lower()]

    def __setitem__(self, key: str, value: str) -> None:
        self.__headers[key.lower()] = value

    def __contains__(self, key: str) -> bool:
        return key.lower() in self.__headers

    @overload
    def get(self, key: str) -> Optional[str]:
        ...  # pragma: no cover

    @overload
    def get(self, key: str, default: str) -> str:
        ...  # pragma: no cover

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self.__headers.get(key.lower(), default)

    @classmethod
    def parse(cls, headers: Iterable[str]) -> "HeaderMapping":
        return cls([
            (k.strip(), v.strip()) for header in headers
            for k, v in [header.split(":", maxsplit=1)]
        ])


class HeaderSequence():

    def __init__(self, headers: Iterable[Tuple[str, str]] = []) -> None:
        self.__headers: List[Tuple[str, str]] = [(k.lower(), v) for k, v in headers]  # noqa:E501

    def __len__(self) -> int:
        return len(self.__headers)

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(self.__headers)

    def add(self, key: str, value: str) -> None:
        self.__headers.append((key.lower(), value))

    @classmethod
    def parse(cls, headers: Iterable[str]) -> "HeaderSequence":
        return cls([
            (k.strip(), v.strip()) for header in headers
            for k, v in [header.split(":", maxsplit=1)]
        ])
