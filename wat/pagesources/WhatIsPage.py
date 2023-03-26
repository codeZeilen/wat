from .AbstractPage import AbstractPage
import subprocess


class WhatIsPage(AbstractPage):
    """`whatis` makes use of the man page infrastructure of the OS.
    This also covers the output of `apropos`, `info`, and `man`."""

    def __init__(self, name, content: str):
        self.name = name
        self.content = content

    @classmethod
    def run_whatis(cls, name: str):
        return subprocess.run(["whatis", name], capture_output=True)

    @classmethod
    def get_page(cls, name: str) -> 'WhatIsPage':
        process = cls.run_whatis(name)
        if process.returncode != 0:
            cls.raiseKeyError(name)
        description = process.stdout.decode('utf-8')
        description = description.split(" - ")[1].strip()
        return cls(name, description)

    def description(self, detailed=False) -> str:
        return self.content

    def page_type(self) -> str:
        return "program"
