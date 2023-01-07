from typing import List, Optional, Tuple, Union, Type
from .AbstractPage import AbstractPage
import subprocess

class BashHelpPage(AbstractPage):
    """`help` documents the built-in commands of bash"""

    def __init__(self, name, content: str):
        self.page_name = name
        self.content = content

    def description(self, detailed = False) -> str:
        return self.content

    @classmethod
    def run_help(cls, name: str):
        return subprocess.run(["/bin/bash", "-c", '"help -d {name}"'.format(name=name)], capture_output=True)
        
    @classmethod
    def has_page(cls, name: str) -> bool:
        process = cls.run_help(name)
        return process.returncode == 0

    @classmethod
    def get_page(cls, name: str) -> 'BashHelpPage':
        process = cls.run_help(name)
        return cls(name, str(process.stdout))