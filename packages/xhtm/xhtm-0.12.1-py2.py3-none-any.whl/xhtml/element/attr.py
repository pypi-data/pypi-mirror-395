# coding:utf-8

from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple
from typing import TypeVar


class Attr:
    """HTML Attribute"""

    def __init__(self, k: str, v: str = ""):
        self.__k: str = k
        self.__v: str = v

    def __str__(self) -> str:
        return f"{self.k}=\"{self.v}\"" if self.v else ""

    @property
    def k(self) -> str:
        return self.__k

    @property
    def v(self) -> str:
        return self.__v

    @v.setter
    def v(self, v: str):
        self.__v = v


Arguments = TypeVar("Arguments", List[Attr], Dict[str, str])
Attribute = TypeVar("Attribute", str, Attr)


class Args():
    """HTML Attribute Arguments"""

    def __init__(self, args: Arguments = []):
        _args: List[Attr] = [Attr(k, v) for k, v in args.items()
                             ] if isinstance(args, Dict) else args
        self.__args: Dict[str, Attr] = {_arg.k: _arg for _arg in _args}

    def __len__(self) -> int:
        return len(self.__args)

    def __iter__(self) -> Iterator[Attr]:
        return iter(self.__args.values())

    def __contains__(self, k: str) -> bool:
        return k in self.__args

    def __getitem__(self, k: str) -> Attr:
        return self.__args[k]

    def __setitem__(self, k: str, v: Attribute):
        self.__args[k] = self.new(k, v)

    def keys(self) -> Tuple[str, ...]:
        return tuple(self.__args.keys())

    def values(self) -> Tuple[Attr, ...]:
        return tuple(self.__args.values())

    def items(self) -> Tuple[Tuple[str, Attr], ...]:
        return tuple(self.__args.items())

    def new(self, k: str, v: Attribute) -> Attr:
        """alloc attribute object"""
        return v if isinstance(v, Attr) else Attr(k, v)

    def get(self, k: str) -> Attr:
        """get attribute"""
        if k not in self.__args:
            self.__args.setdefault(k, Attr(k))
        return self.__args[k]

    def set(self, k: str, v: Attribute):
        """set attribute"""
        self.__args[k] = self.new(k, v)

    def hit(self, k: str, v: Attribute):
        """set default value for attribute"""
        if k not in self.__args:
            self.__args.setdefault(k, self.new(k, v))
