from .AbstractPage import AbstractPage
import subprocess


class SystemCtlPage(AbstractPage):
    """systemctl has descriptions for running services"""

    def __init__(self, name, content: str):
        self.page_name = name
        self.content = content

    def description(self, detailed=False) -> str:
        return self.content

    @classmethod
    def run_systemctl(cls, name: str):
        return subprocess.run(["/bin/systemctl", "-c", '"systemctl list-units --all --no-legend {name}"'.format(name=name)], capture_output=True)

    @classmethod
    def extract_description(cls, systemctl_output: str) -> str:
        return systemctl_output.strip().split(" ", 4)[4:][0]

    @classmethod
    def has_page(cls, name: str) -> bool:
        return cls.run_systemctl(name).returncode == 0 and \
            cls.run_systemctl(name + ".service").returncode == 0

    @classmethod
    def get_page(cls, name: str) -> 'SystemCtlPage':
        process = cls.run_systemctl(name)
        if process.returncode == 0:
            return cls(name,
                       cls.extract_description(str(process.stdout)))

        process = cls.run_systemctl(name + ".service")
        if process.returncode == 0:
            return cls(name + ".service",
                       cls.extract_description(str(process.stdout)))

        raise NameError(name)
