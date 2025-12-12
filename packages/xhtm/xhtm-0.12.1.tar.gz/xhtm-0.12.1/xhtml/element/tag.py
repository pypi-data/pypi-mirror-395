# coding:utf-8

from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import TypeVar

from xhtml.attribute import __description__
from xhtml.attribute import __project__
from xhtml.element.attr import Args
from xhtml.element.attr import Arguments
from xhtml.element.attr import Attr
from xhtml.element.css import StyleCSS


class Attrs(Args):
    """HTML Tag Attributes"""

    def __init__(self, attrs: Arguments):
        super().__init__(attrs)

    @property
    def std_accesskey(self) -> Attr:
        return self.get("accesskey")

    @property
    def std_class(self) -> Attr:
        return self.get("class")

    @property
    def std_contenteditable(self) -> Attr:
        return self.get("contenteditable")

    @property
    def std_contextmenu(self) -> Attr:
        return self.get("contextmenu")

    @property
    def std_dir(self) -> Attr:
        return self.get("dir")

    @property
    def std_draggable(self) -> Attr:
        return self.get("draggable")

    @property
    def std_dropzone(self) -> Attr:
        return self.get("dropzone")

    @property
    def std_enterkeyhint(self) -> Attr:
        return self.get("enterkeyhint")

    @property
    def std_hidden(self) -> Attr:
        return self.get("hidden")

    @property
    def std_id(self) -> Attr:
        return self.get("id")

    @property
    def std_inert(self) -> Attr:
        return self.get("inert")

    @property
    def std_inputmode(self) -> Attr:
        return self.get("inputmode")

    @property
    def std_lang(self) -> Attr:
        return self.get("lang")

    @property
    def std_popover(self) -> Attr:
        return self.get("popover")

    @property
    def std_spellcheck(self) -> Attr:
        return self.get("spellcheck")

    @property
    def std_style(self) -> StyleCSS:
        k = StyleCSS.K
        v = self.get(k)
        if not isinstance(v, StyleCSS):
            v = StyleCSS()
            self.set(k, v)
        return v

    @property
    def std_tabindex(self) -> Attr:
        return self.get("tabindex")

    @property
    def std_title(self) -> Attr:
        return self.get("title")

    @property
    def std_translate(self) -> Attr:
        return self.get("translate")


Attributes = TypeVar("Attributes", List[Attr], Dict[str, str], Attrs)


def parse_attrs(attrs: Attributes) -> Attrs:
    return Attrs(attrs) if not isinstance(attrs, Attrs) else attrs


class Tag():
    """HTML Tag"""

    def __init__(self, name: str, empty: bool = False, attrs: Attributes = {}, child: "Tags" = []):  # noqa:E501
        tags = [child] if isinstance(child, Tag) else child if child is None else [i for i in child]  # noqa:E501
        self.__name: str = name  # tag name
        self.__empty: bool = empty  # empty tag
        self.__attrs: Attrs = parse_attrs(attrs)  # attributes
        self.__items: Optional[List[Tag]] = tags  # child elements

    def __str__(self) -> str:
        items: List[str] = [self.start, self.child, self.end]
        joint: str = "\n" if len(items[1]) > 10 else ""
        return joint.join(items)

    @property
    def name(self) -> str:
        """tag name"""
        return self.__name

    @property
    def empty(self) -> bool:
        """empty tag"""
        return self.__empty

    @property
    def attrs(self) -> Attrs:
        """attributes"""
        return self.__attrs

    @property
    def start(self) -> str:
        """start tag"""
        return f"<{' '.join([self.name] + [str(attr) for attr in self.attrs])}>"  # noqa:E501

    @property
    def child(self) -> str:
        """child elements"""
        tags: List[Tag] = self.__items or []
        return "\n".join(str(t) for t in tags)

    @property
    def end(self) -> str:
        """end tag"""
        return f"</{self.__name}>" if not self.empty else ""

    def add(self, tag: "Tag") -> None:
        """add child element"""
        if not self.empty and self.__items is not None:
            self.__items.append(tag)


Tags = TypeVar("Tags", Iterable[Tag], Tag, None)


class EmptyTag(Tag):
    """HTML Empty Tag"""

    def __init__(self, name: str, attrs: Attributes = {}):
        super().__init__(name, empty=True, attrs=attrs)

    def __str__(self) -> str:
        return self.start


class TextTag(Tag):
    """HTML Text Tag"""

    def __init__(self, name: str, text: str, attrs: Attributes = {}):
        super().__init__(name, attrs=attrs)
        self.__text: str = text

    def __str__(self) -> str:
        text = self.text.replace("\n", "<br>")
        return f"{self.start}{text}{self.end}"

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text


class Br(EmptyTag):
    T = "br"

    def __init__(self):
        super().__init__(self.T)


class Div(Tag):
    T = "div"

    def __init__(self, attrs: Arguments = {}, child: Tags = []):
        super().__init__(self.T, attrs=attrs, child=child)


class FormAttrs(Attrs):
    def __init__(self, attrs: Arguments):
        super().__init__(attrs)

    @property
    def method(self) -> Attr:
        return self.get("method")


class Form(Tag):
    T = "form"

    def __init__(self, attrs: Arguments = {}, child: Tags = []):
        self.__attrs: FormAttrs = FormAttrs(attrs)
        super().__init__(self.T, attrs=self.__attrs, child=child)

    @property
    def attrs(self) -> FormAttrs:
        return self.__attrs


class InputAttrs(Attrs):
    def __init__(self, attrs: Arguments):
        super().__init__(attrs)
        self.hit("type", "text")

    @property
    def name(self) -> Attr:
        return self.get("name")

    @property
    def placeholder(self) -> Attr:
        return self.get("placeholder")

    @property
    def type(self) -> Attr:
        return self.get("type")

    @property
    def value(self) -> Attr:
        return self.get("value")


class Input(EmptyTag):
    T = "input"

    def __init__(self, attrs: Arguments = {}):
        self.__attrs: InputAttrs = InputAttrs(attrs)
        super().__init__(self.T, attrs=self.__attrs)

    @property
    def attrs(self) -> InputAttrs:
        return self.__attrs


class Span(TextTag):
    T = "span"

    def __init__(self, text: str = "", attrs: Arguments = {}):
        super().__init__(self.T, text, attrs=attrs)


class Title(TextTag):
    T = "title"

    def __init__(self, text: str = ""):
        super().__init__(self.T, text)


class Head(Tag):
    T = "head"

    def __init__(self, attrs: Arguments = {}):
        self.__title: Title = Title(f"{__description__} by {__project__}")
        super().__init__(self.T, attrs=attrs, child=[self.__title])

    @property
    def title(self) -> Title:
        return self.__title


class Body(Tag):
    T = "body"

    def __init__(self, attrs: Arguments = {}, child: Tags = []):
        super().__init__(self.T, attrs=attrs, child=child)


class HtmlAttrs(Attrs):
    def __init__(self, attrs: Arguments):
        super().__init__(attrs)

    @property
    def xmlns(self) -> Attr:
        return self.get("xmlns")


class Html(Tag):
    T = "html"

    def __init__(self, attrs: Arguments = {}):
        self.__head: Head = Head()
        self.__body: Body = Body()
        self.__attrs: HtmlAttrs = HtmlAttrs(attrs)
        super().__init__(self.T, attrs=self.__attrs,
                         child=[self.__head, self.__body])

    @property
    def attrs(self) -> HtmlAttrs:
        return self.__attrs

    @property
    def head(self) -> Head:
        return self.__head

    @property
    def body(self) -> Body:
        return self.__body
