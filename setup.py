from typing import List, Tuple

from setuptools import setup, find_packages
import os
import sys
import warnings
import re

LOWEST_PYTHON_VERSION_SUPPORTED: Tuple[int, int] = (3, 10)
FIRST_PYTHON_VERSION_NOT_TESTED: Tuple[int, int] = (3, 11)
DESCRIPTION_PATH: str = ".description"
VERSION_PATH: str = ".ver"
REQUIREMENTS_PATH: str = "requirements.txt"
SETUP_COMMAND_WHEN_MISSING: List[str] = ["install"]
PACKAGE_NAME: str = "sql-query-parser"
AUTHOR: str = "Matteo Morando"
AUTHOR_EMAIL: str = "morandomatteo98@gmail.com"
EXCLUDED_PACKAGES: List[str] = []
REPOSITORY_URL: str = "https://github.com/Morry98/sql-parser"
LICENSE_PATH: str = "LICENSE"
DOWNLOAD_URL: str = ""
KEYWORDS: List[str] = ["sql", "parser", "sql-parser", "sql-query-parser"]

# Python supported version checks.
if sys.version_info[:2] < LOWEST_PYTHON_VERSION_SUPPORTED:
    raise RuntimeError(
        f"Python version >= {LOWEST_PYTHON_VERSION_SUPPORTED[0]}.{LOWEST_PYTHON_VERSION_SUPPORTED[1]} required.")

current_dir: str = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


# read first line of DESCRIPTION_PATH file
def read_description() -> List[str]:
    try:
        with open(os.path.join(current_dir, DESCRIPTION_PATH), "r", encoding="utf-8") as f:
            description = f.read()
    except IOError:
        description = ""
    return description.split("\n")


# read LICENSE_PATH file
def read_license() -> str:
    try:
        with open(os.path.join(current_dir, LICENSE_PATH), "r", encoding="utf-8") as f:
            license_file = f.read()
    except IOError:
        license_file = ""
    return license_file


# read first line of VERSION_PATH file
def read_version() -> str:
    try:
        with open(os.path.join(current_dir, VERSION_PATH), "r", encoding="utf-8") as f:
            version = f.read().split("\n")[0]
    except IOError:
        version = "0.0.0"
    return version


def read_requirements() -> List[str]:
    with open(os.path.join(current_dir, REQUIREMENTS_PATH), "r", encoding="utf-8") as f:
        requirements = f.read().split("\n")
    return requirements


FULL_VERSION = read_version()


_V_MATCH = re.match(r"(\d+)\.(\d+)\.(\d+)", FULL_VERSION)
if _V_MATCH is None:
    raise RuntimeError(f"Cannot parse version {FULL_VERSION}")
MAJOR, MINOR, MICRO = _V_MATCH.groups()
VERSION = "{}.{}.{}".format(MAJOR, MINOR, MICRO)

# Warning if Python version is not tested yes
if sys.version_info >= FIRST_PYTHON_VERSION_NOT_TESTED:
    fmt = "{} {} may not yet support Python {}.{}."
    warnings.warn(
        fmt.format(PACKAGE_NAME, VERSION, *sys.version_info[:2]),
        RuntimeWarning)
    del fmt


def get_docs_url() -> str:
    return "??/{}.{}".format(MAJOR, MINOR)


def setup_package() -> None:
    metadata = dict(
        name=PACKAGE_NAME,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=read_description()[0],
        long_description="\n".join(read_description()),
        url=REPOSITORY_URL,
        download_url=DOWNLOAD_URL.format(PACKAGE_NAME, VERSION),
        project_urls={
            "Bug Tracker": REPOSITORY_URL + "/issues",
            # "Documentation": get_docs_url(),
            "Source Code": REPOSITORY_URL,
        },
        license=read_license(),
        platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
        test_suite="pytest",
        version=FULL_VERSION,
        python_requires=f">={LOWEST_PYTHON_VERSION_SUPPORTED[0]}.{LOWEST_PYTHON_VERSION_SUPPORTED[1]}",
        install_requires=read_requirements(),
        packages=find_packages(exclude=EXCLUDED_PACKAGES),
        include_package_data=True,
        keywords=KEYWORDS
    )

    setup(**metadata)


if __name__ == "__main__":
    if not sys.argv[1:]:
        sys.argv[1:] = SETUP_COMMAND_WHEN_MISSING
    setup_package()
