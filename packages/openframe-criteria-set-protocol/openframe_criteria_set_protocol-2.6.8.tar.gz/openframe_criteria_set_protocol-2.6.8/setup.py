import re

from setuptools import setup, find_packages

with open("pyproject.toml", "r") as file:
    content = file.read()
    name = re.compile('name = "([^"]+)"').search(content).group(1)
    version = re.compile('version = "([^"]+)"').search(content).group(1)
    description = re.compile('description = "([^"]+)"').search(content).group(1)

setup(
    name=name,
    packages=find_packages(),
    version=version,
    description=description,
    author='Andrés Angulo <aa@openframe.org>',
    setup_requires=['pytest-runner']
)
