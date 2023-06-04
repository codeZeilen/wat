from .AbstractPage import AbstractPage
from typing import List, Optional, Union
import tldr


def get_page(
    command: str,
    remote: Optional[str] = None,
    platforms: Optional[List[str]] = None,
    languages: Optional[List[str]] = None
) -> Union[str, bool]:
    if platforms is None:
        platforms = tldr.get_platform_list()
    if languages is None:
        languages = tldr.get_language_list()
    # really only use cache
    for platform in platforms:
        for language in languages:
            if platform is None:
                continue
            try:
                return tldr.get_page_for_platform(
                    command,
                    platform,
                    remote,
                    language,
                    only_use_cache=True,
                )
            except tldr.CacheNotExist:
                continue
    return False

tldr.get_page = get_page


class TLDRPage(AbstractPage):

    def __init__(self, name, content: str):
        self.name = name
        self.content = content

    @classmethod
    def update_page_source(cls):
        tldr.update_cache()

    @classmethod
    def get_page(cls, name: str) -> 'AbstractPage':
        content = tldr.get_page(name)
        if content is False:
            cls.raiseKeyError(name)
        return cls(name, content)       

    def description(self, detailed=False) -> str:
        description = ""
        lines = self.content[2:4] if detailed else self.content[2:3]
        for line in lines:
            line = line.rstrip().decode('utf-8')
            if line[0] == ">":
                line = line[1:].lstrip()
            description = description + line + "\n"
        return description.rstrip()

    def page_type(self) -> str:
        return "program"
