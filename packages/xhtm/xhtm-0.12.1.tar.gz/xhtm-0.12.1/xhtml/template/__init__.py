# coding:utf-8

from os.path import abspath
from os.path import dirname
from os.path import isdir
from typing import Optional

from xkits_lib.unit import TimeUnit

from xhtml.resource import Resource

BASE_DIR = dirname(abspath(__file__))


class Template(Resource):
    FAVICON: str = "favicon.ico"

    def __init__(self, base: Optional[str] = None, lifetime: TimeUnit = 0):
        super().__init__(base if base and isdir(base) else BASE_DIR, lifetime)
