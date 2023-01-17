from .AbstractPage import AbstractPage
import subprocess

SYSTEMCTL_AVAILABLE = subprocess.run("systemctl --version",
                                     capture_output=True,
                                     shell=True).returncode == 0


class SystemCtlPage(AbstractPage):
    """systemctl has descriptions for running services"""

    def __init__(self, name, content: str):
        self.page_name = name
        self.content = content

    def description(self, detailed=False) -> str:
        return self.content

    @classmethod
    def run_systemctl(cls, name: str):
        return subprocess.run("systemctl list-units --all --no-legend {name}".format(name=name), capture_output=True, shell=True)
            
    @classmethod
    def extract_description(cls, systemctl_output: bytes) -> str:
        string_output = systemctl_output.decode('utf-8')
        return string_output.strip().split(" ", 4)[4:][0]

    @classmethod
    def has_page(cls, name: str) -> bool:
        if not SYSTEMCTL_AVAILABLE:
            return False
        else:
            plain = cls.run_systemctl(name)
            with_service_ending = cls.run_systemctl(name + ".service")
            return cls.process_successfully_returned(plain) \
                    or cls.process_successfully_returned(with_service_ending)

    @classmethod
    def process_successfully_returned(cls, process:
            'subprocess.CompletedProcess') -> bool:
        return process.returncode == 0 and len(process.stdout) > 0

    @classmethod
    def get_page(cls, name: str) -> 'SystemCtlPage':
        process = cls.run_systemctl(name)
        if cls.process_successfully_returned(process):
            return cls(name,
                       cls.extract_description(process.stdout))

        process = cls.run_systemctl(name + ".service")
        if cls.process_successfully_returned(process):
            return cls(name + ".service",
                       cls.extract_description(process.stdout))

        raise NameError(name)
