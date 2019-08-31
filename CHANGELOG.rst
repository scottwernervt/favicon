Changelog
=========

0.7.0 (2019-08-31)
------------------

* Handle empty `href` and `content` attribute values (`#22 <https://github.com/scottwernervt/favicon/issues/22>`_).
* Support passing request library parameters to `favicon.get()` (`#21 <https://github.com/scottwernervt/favicon/issues/21>`_).

  * Deprecate `headers` argument. Use keyword arguments: `favicon.get(url, headers={'User-Agent'; 'my-agent'}`.

0.6.0 (2019-08-10)
------------------

* Upgrade ``beautifulsoup4`` and ``requests`` package dependencies.

0.5.1 (2018-11-05)
------------------

* Fix 'NoneType' object has no attribute 'lower' for meta tags (`#16 <https://github.com/scottwernervt/favicon/issues/16>`_).

0.5.0 (2018-11-05)
------------------

* Add support for meta tags (`#15 <https://github.com/scottwernervt/favicon/pull/15>`_).
* Set bs4 parser to ``html.parser`` (`#13 <https://github.com/scottwernervt/favicon/issues/13>`_).
* Use ``src`` package structure (`#11 <https://github.com/scottwernervt/favicon/issues/11>`_).

0.4.1 (2018-10-01)
------------------

* Update ``requirements.txt`` and ``dev-requirements.txt``.

0.4.0 (2018-07-19)
------------------

* Add support for Python 2.7 and PyPy.
* Get icon size for New York Times (`#9 <https://github.com/scottwernervt/favicon/issues/9>`_).

0.3.0 (2018-05-18)
------------------

* Fav icon not found for microsoft.com (`#7 <https://github.com/scottwernervt/favicon/issues/7>`_).

0.2.0 (2018-05-17)
------------------

* Handle poor html values in links (`#5 <https://github.com/scottwernervt/favicon/issues/5>`_).
* Use given website for icon url scheme (`#6 <https://github.com/scottwernervt/favicon/issues/6>`_).

0.1.0 (2018-05-07)
------------------

* First release.
