from setuptools import setup, find_packages

DESCRIPTION = "GMO社のFX API用Pythonライブラリ"
NAME = "gmo_fx"
AUTHOR = "Rikito Noto"
AUTHOR_EMAIL = "rikitonoto@gmail.com"
URL = "https://github.com/RikitoNoto/gmo-fx-py"
LICENSE = "MIT"
DOWNLOAD_URL = "https://github.com/RikitoNoto/gmo-fx-py"
VERSION = "0.8.1"
INSTALL_REQUIRES = [
    "requests>=2.31.0",
]

with open("README.md", "r") as fp:
    readme = fp.read()

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    download_url=DOWNLOAD_URL,
    version=VERSION,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)
