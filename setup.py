import os
import re

from setuptools import find_packages, setup

ROOT = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

install_requires = ['requests>=2.1.0', 'beautifulsoup4>=4.3.2']


def get_version():
    init = open(os.path.join(ROOT, 'favicon', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


download_url = 'https://github.com/scottwernervt/favicon' \
               'archive/%s.tar.gz' % get_version()

setup(
    name='favicon',
    version=get_version(),
    author='Scott Werner',
    author_email='scott.werner.vt@gmail.com',
    description="Find a website's favicon",
    long_description=open('README.rst').read(),
    license='MIT',
    platforms='any',
    keywords=' '.join([
        'favicon',
        'favicons',
        'icon',
        'icons',
    ]),
    url='https://github.com/scottwernervt/favicon',
    download_url=download_url,
    install_requires=install_requires,
    extras_require={
        'tests': 'pytest',  # MIT
    },
    setup_requires=[
        'pytest-runner',  # MIT
    ],
    tests_require=[
        'pytest',  # MIT
        'requests-mock',  # Apache 2
    ],
    test_suite='tests',
    packages=find_packages(exclude=['contrib', 'docs' 'tests*']),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
    ],
)
