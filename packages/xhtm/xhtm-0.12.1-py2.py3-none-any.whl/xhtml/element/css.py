# coding:utf-8

from xhtml.element.attr import Args
from xhtml.element.attr import Arguments
from xhtml.element.attr import Attr


class StyleCSS(Attr):
    """HTML CSS Inline Style"""
    K = "style"

    def __init__(self, definitions: Arguments = {}):
        self.__defs: Args = Args(definitions)
        super().__init__(self.K, "")

    def __str__(self) -> str:
        return str(Attr(self.K, " ".join([f"{a.k}: {a.v};" for a in self.__defs])))  # noqa:E501

    @property
    def display(self) -> Attr:
        return self.__defs.get("display")

    @property
    def height(self) -> Attr:
        return self.__defs.get("height")

    @property
    def margin(self) -> Attr:
        return self.__defs.get("margin")

    @property
    def margin_top(self) -> Attr:
        return self.__defs.get("margin-top")

    @property
    def margin_bottom(self) -> Attr:
        return self.__defs.get("margin-bottom")

    @property
    def margin_left(self) -> Attr:
        return self.__defs.get("margin-left")

    @property
    def margin_right(self) -> Attr:
        return self.__defs.get("margin-right")

    @property
    def place_items(self) -> Attr:
        return self.__defs.get("place-items")

    @property
    def text_align(self) -> Attr:
        return self.__defs.get("text-align")

    @property
    def vertical_align(self) -> Attr:
        return self.__defs.get("vertical-align")

    @property
    def width(self) -> Attr:
        return self.__defs.get("width")
