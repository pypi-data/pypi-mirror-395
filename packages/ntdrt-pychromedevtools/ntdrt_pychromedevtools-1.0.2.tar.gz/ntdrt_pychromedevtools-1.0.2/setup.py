from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="ntdrt-pychromedevtools",
    version="1.0.2",
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
