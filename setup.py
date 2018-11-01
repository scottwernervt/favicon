import io
import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(
            join(dirname(__file__), *names),
            encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='favicon',
    version='0.4.2',
    license='MIT',
    description="Get a website's favicon.",
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub(
            '', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Scott Werner',
    author_email='scott.werner.vt@gmail.com',
    url='https://github.com/scottwernervt/favicon',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
    ],
    keywords=' '.join([
        'favicon',
        'icon',
    ]),
    install_requires=[
        'requests>=2.1.0',  # Apache 2.0
        'beautifulsoup4>=4.3.2',  # BSD
    ],
    extras_require={

    },
    setup_requires=[
        'pytest-runner',  # MIT
    ],
    tests_require=[
        'pytest',  # MIT
        'requests-mock',  # Apache 2
    ],
    test_suite='tests',
)
