from .AbstractPage import AbstractPage
import subprocess


class PackageManagerPage(AbstractPage):
    """These pages describe OS packages."""

    def __init__(self, name, content: str):
        self.name = name
        self.content = content

    @classmethod
    def run_package_manager(cls, name: str):
        return subprocess.run(["apt", "show", name], capture_output=True)

    @classmethod 
    def find_description(cls, stdout: str):
        description = ""
        description_started = False
        for line in stdout.splitlines():
            if description_started:
                if line == " .":
                    break
                if line.startswith(" "):
                    description += line.strip() + " "
            if line.startswith("Description"):
                description_started = True
            
        return description

    @classmethod
    def has_page(cls, name: str) -> bool:
        process = cls.run_package_manager(name)
        if process.returncode == 0:
            return cls.find_description(process.stdout.decode('utf-8')) != ""
        else:
            return False

    @classmethod
    def get_page(cls, name: str) -> 'PackageManagerPage':
        process = cls.run_package_manager(name)
        if process.returncode != 0:
            cls.raiseKeyError(name)
        description = cls.find_description(process.stdout.decode('utf-8'))
        return cls(name, description)

    def description(self, detailed=False) -> str:
        return self.content

    def page_type(self) -> str:
        return "package"
