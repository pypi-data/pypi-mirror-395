import os

from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

version = {}
version_file = os.path.abspath(os.path.dirname(__file__)) + "/ntdrt_pychromedevtools/__version__.py"
with open(version_file) as file:
    exec(file.read(), version)

setup(
    name="ntdrt-pychromedevtools",
    version=version["__version__"],
    author="Tomáš Kolinger",
    author_email="tomas@kolinger.name",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["ntdrt_pychromedevtools"],
    install_requires=[
        "requests",
        "websocket-client",
    ],
    zip_safe=False
)
