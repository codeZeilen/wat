from .AbstractPage import AbstractPage
import subprocess


class BashHelpPage(AbstractPage):
    """`help` documents the built-in commands of bash"""

    def __init__(self, name, content: str):
        self.name = name
        self.content = content

    @classmethod
    def run_help(cls, name: str):
        return subprocess.run(["/bin/bash", "-c", 'help -d {name}'.format(name=name)], capture_output=True)

    @classmethod
    def get_page(cls, name: str) -> 'BashHelpPage':
        process = cls.run_help(name)
        if process.returncode != 0:
            cls.raiseKeyError(name)
        return cls(name, process.stdout.decode("utf-8"))

    def description(self, detailed = False) -> str:
        return self.content

    def page_type(self) -> str:
        return "builtin"
