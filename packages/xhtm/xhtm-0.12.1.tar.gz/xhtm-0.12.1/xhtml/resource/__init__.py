# coding:utf-8

from os.path import abspath
from os.path import dirname
from os.path import isdir
from os.path import isfile
from os.path import join
from os.path import splitext
from typing import Optional

from jinja2 import Environment
from xkits_lib.cache import CacheMiss
from xkits_lib.cache import CachePool
from xkits_lib.unit import TimeUnit

BASE_DIR = dirname(abspath(__file__))


class FileResource():
    def __init__(self, path: str):
        if not isinstance(path, str) or not isfile(path):
            message = f"No such file: {path}"
            raise FileNotFoundError(message)
        self.__ext: str = splitext(path)[1]
        self.__data: Optional[bytes] = None
        self.__path: str = path

    @property
    def ext(self) -> str:
        return self.__ext

    @property
    def path(self) -> str:
        return self.__path

    def loadb(self) -> bytes:
        if self.__data is None:
            with open(self.path, "rb") as rhdl:
                self.__data = rhdl.read()
        return self.__data

    def loads(self, encoding: str = "utf-8") -> str:
        return self.loadb().decode(encoding=encoding)

    def render(self, **context: str) -> str:
        """render html template"""
        return Environment().from_string(self.loads()).render(**context)


class Resource():
    FAVICON: str = "favicon.ico"

    def __init__(self, base: Optional[str] = None, lifetime: TimeUnit = 0):
        self.__cache: CachePool[str, FileResource] = CachePool(lifetime)
        self.__base: str = base if base and isdir(base) else BASE_DIR

    @property
    def base(self) -> str:
        return self.__base

    @property
    def favicon(self) -> FileResource:
        return self.seek(self.FAVICON)

    def find(self, *args: str) -> Optional[FileResource]:
        def check(base: str, real: str) -> Optional[str]:
            return path if isfile(path := join(base, real)) else check(BASE_DIR, real) if base != BASE_DIR else None  # noqa:E501

        if (real := join(*args)) in self.__cache:
            try:
                return self.__cache.get(real)
            except CacheMiss:
                pass

        resource: Optional[FileResource] = None
        if isinstance(path := check(self.base, real), str):
            resource = FileResource(path)
            self.__cache.put(real, resource)
        return resource

    def seek(self, *args: str) -> FileResource:
        if not isinstance(resource := self.find(*args), FileResource):
            raise FileNotFoundError(f"No such file: {join(*args)}")
        return resource
