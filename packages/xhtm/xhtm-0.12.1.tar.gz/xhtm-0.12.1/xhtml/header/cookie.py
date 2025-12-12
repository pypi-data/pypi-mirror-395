# coding:utf-8

from typing import Dict
from typing import Iterator


class Cookies():
    def __init__(self, *cookies: str):
        self.__cookies: Dict[str, str] = {}
        for _cookies in cookies:
            for _cookie in [_c for _c in _cookies.split("; ") if _c.strip()]:
                k, v = _cookie.split("=", maxsplit=1)
                self.__cookies[k] = v

    def __len__(self) -> int:
        return len(self.__cookies)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__cookies)

    def __getitem__(self, key: str) -> str:
        return self.__cookies[key]

    def __contains__(self, key: str) -> bool:
        return key in self.__cookies

    def get(self, key: str, default: str = "") -> str:
        return self.__cookies.get(key, default)
