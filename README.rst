favicon
=======

.. image:: https://travis-ci.org/scottwernervt/favicon.svg?branch=master
   :target: https://travis-ci.org/scottwernervt/favicon

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: /LICENSE

Requirements
------------

* `requests <http://docs.python-requests.org/>`_
* `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_

Installation
------------

To install favicon:

.. code-block:: bash

    pip install favicon

Usage
-----

.. code-block:: python

    >>> import favicon
    >>> icons = favicon.get('https://pypi.org/')
    Icon(url='https://www.python.org/static/apple-touch-icon-144x144-precomposed.png', width=144, height=144, format='png')
    Icon(url='https://www.python.org/static/apple-touch-icon-114x114-precomposed.png', width=114, height=114, format='png')
    Icon(url='https://www.python.org/static/apple-touch-icon-72x72-precomposed.png', width=72, height=72, format='png')
    Icon(url='https://www.python.org/static/apple-touch-icon-precomposed.png', width=0, height=0, format='png')
    Icon(url='https://www.python.org/static/favicon.ico', width=0, height=0, format='ico')

Inspiration
-----------

* `pyfav <https://github.com/phillipsm/pyfav>`_
* `besticon <https://github.com/mat/besticon/>`_
* `How to get high resolution website logo (favicon) for a given URL <https://stackoverflow.com/questions/21991044/how-to-get-high-resolution-website-logo-favicon-for-a-given-url>`_
