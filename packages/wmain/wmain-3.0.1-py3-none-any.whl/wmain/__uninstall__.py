from setuptools import Command
import subprocess
import sys


class UninstallCommand(Command):
    description = "卸载整个 wmain 生态"
    user_options = []

    def initialize_options(self): ...

    def finalize_options(self): ...

    def run(self):
        packages = ["wmain", "wmain-base", "wmain-api", "wmain-extensions", "wmain-mail"]
        for pkg in packages:
            subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", pkg])
