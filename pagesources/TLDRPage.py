from typing import List, Optional, Tuple, Union, Type
from .AbstractPage import AbstractPage

import tldr

class TLDRPage(AbstractPage):

    def __init__(self, name, content: List[str]):
        self.page_name = name
        self.content = content

    @classmethod
    def get_page(cls, name: str) -> 'TLDRPage':
        return cls(name, tldr.get_page(name))

    @classmethod
    def has_page(cls, name: str) -> bool:
        return tldr.get_page(name) is not False

    def description(self, detailed = False) -> str:
        description = ""
        lines = self.content[2:4] if detailed else self.content[2:3]
        for line in lines:
            line = line.rstrip().decode('utf-8')
            if line[0] == ">":
                line = line[1:].lstrip()
            description = description + line + "\n" 
        return description.rstrip()