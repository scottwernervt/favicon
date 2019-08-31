========
favicon
========

.. start-badges

.. image:: https://img.shields.io/pypi/v/favicon.svg
   :target: https://pypi.python.org/pypi/favicon

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: /LICENSE

.. image:: https://travis-ci.org/scottwernervt/favicon.svg?branch=master
   :target: https://travis-ci.org/scottwernervt/favicon

.. end-badges

``favicon`` is a Python library to find a website's favicon.

Installation
============

.. code-block:: bash

   pip install favicon

Usage
=====

Get all icons:

.. code-block:: python

   >>> import favicon
   >>> icons = favicon.get('https://www.python.org/')
   Icon(url='https://www.python.org/static/apple-touch-icon-144x144-precomposed.png', width=144, height=144, format='png')
   Icon(url='https://www.python.org/static/apple-touch-icon-114x114-precomposed.png', width=114, height=114, format='png')
   Icon(url='https://www.python.org/static/apple-touch-icon-72x72-precomposed.png', width=72, height=72, format='png')
   Icon(url='https://www.python.org/static/apple-touch-icon-precomposed.png', width=0, height=0, format='png')
   Icon(url='https://www.python.org/static/favicon.ico', width=0, height=0, format='ico')

Download largest icon:

.. code-block:: python

   import requests
   import favicon

   icons = favicon.get('https://www.python.org/')
   icon = icons[0]

   response = requests.get(icon.url, stream=True)
   with open('/tmp/python-favicon.{}'.format(icon.format), 'wb') as image:
       for chunk in response.iter_content(1024):
           image.write(chunk)

   # /tmp/python-favicon.png

`Request library <https://2.python-requests.org/>`_ parameters can be passed to ``favicon.get()`` as keyword
arguments:

.. code-block:: python

   import favicon

   user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
   headers = {'User-Agent': user_agent}
   favicon.get('https://www.python.org/', headers=headers, timeout=2)

Requirements
============

* `requests <http://docs.python-requests.org/>`_
* `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_

Inspiration
===========

* `pyfav <https://github.com/phillipsm/pyfav>`_
* `besticon <https://github.com/mat/besticon/>`_
* `How to get high resolution website logo (favicon) for a given URL <https://stackoverflow.com/questions/21991044/how-to-get-high-resolution-website-logo-favicon-for-a-given-url>`_
