# coding:utf-8

from xhtml.element.tag import Html


class HtmlDoc(Html):
    def __init__(self, doctype: str = "html"):
        self.__doctype: str = doctype
        super().__init__()

    def __str__(self) -> str:
        return f"<!DOCTYPE {self.doctype}>\n{super().__str__()}"

    @property
    def doctype(self) -> str:
        return self.__doctype
