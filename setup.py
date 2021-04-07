import io
import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


INSTALL_REQUIRES = [
    "requests>=2.21.0",  # Apache 2.0
    "beautifulsoup4>=4.7.0",  # BSD
]
EXTRAS_REQUIRE = {
    "tests": ["flake8==3.9.0 ", "pytest==6.2.3"],
    "lint": [
        "black==20.8b1",
        "flake8-bugbear==21.4.3",
        "flake8==3.9.0",
        "pre-commit==2.12.0",
    ],
    "check": [
        "check-manifest==0.46",
        "readme-renderer==29.0",
        "twine==3.4.1 ",
    ],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["lint"] + ["tox"]


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname, "r") as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


setup(
    name="favicon",
    version=find_version("src/favicon/__init__.py"),
    license="MIT",
    description="Fetch a website's favicon.",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    long_description_content_type="text/x-rst",
    author="Scott Werner",
    author_email="scott.werner.vt@protonmail.com",
    url="https://github.com/scottwernervt/favicon/",
    packages=find_packages("src", exclude=("test*", "docs*")),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords=" ".join(["favicon", "icon"]),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    test_suite="tests",
    project_urls={
        "Changelog": "https://github.com/scottwernervt/favicon/blob/master/CHANGELOG.rst",
        "Issues": "https://github.com/scottwernervt/favicon/issues",
    },
)
