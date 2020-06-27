# -*- coding: utf-8 -*-
"""favicon
:copyright: (c) 2019 by Scott Werner.
:license: MIT, see LICENSE for more details.
"""
import os
import re
import warnings

from collections import namedtuple

try:
    from urllib.parse import urljoin, urlparse, urlunparse
except ImportError:
    from urlparse import urljoin, urlparse, urlunparse

import requests

from bs4 import BeautifulSoup

__all__ = ['get', 'Icon']

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/33.0.1750.152 Safari/537.36'
}

LINK_RELS = [
    'icon',
    'shortcut icon',
    'apple-touch-icon',
    'apple-touch-icon-precomposed',
]

META_NAMES = ['msapplication-TileImage', 'og:image']

SIZE_RE = re.compile(r'(?P<width>\d{2,4})x(?P<height>\d{2,4})', flags=re.IGNORECASE)

Icon = namedtuple('Icon', ['url', 'width', 'height', 'format'])


def get(url, *args, html_override=None, verify_default_icon=True, **request_kwargs):
    """Get all fav icons for a url.

    :param url: Homepage.
    :type url: str

    :param html_override: HTML input, as string. Will be used instead of an HTTP response from
        the `url`.
    :type html_override: str or None

    :param verify_default_icon: Whether to verify the existence of the default
        https://www.domain.com/favicon.ico file, or to return it as a probable result which
        still requires verification, like the other results.
    :type verify_default_icon: bool

    :param request_kwargs: Request headers argument.
    :type request_kwargs: Dict

    :return: List of fav icons found sorted by icon dimension.
    :rtype: list[:class:`Icon`]
    """
    if args:  # backwards compatible with <= v0.6.0
        warnings.warn(
            "headers arg is deprecated. Use headers key in request_kwargs dict.",
            DeprecationWarning
        )
        request_kwargs.setdefault('headers', args[0])

    request_kwargs.setdefault('headers', HEADERS)
    request_kwargs.setdefault('allow_redirects', True)

    if html_override is None:
        response = requests.get(url, **request_kwargs)
        response.raise_for_status()
        final_url = response.url
        html_override = response.text
    else:
        final_url = url

    icons = set()

    default_icon = default(final_url, verify_default_icon, **request_kwargs)
    if default_icon:
        icons.add(default_icon)

    link_icons = tags(final_url, html_override)
    if link_icons:
        icons.update(link_icons)

    return sorted(icons, key=lambda i: i.width + i.height, reverse=True)


def default(url, verify_default_icon, **request_kwargs):
    """Get icon using default filename favicon.ico.

    :param url: Url for site.
    :type url: str

    :param verify_default_icon: Whether to verify the existence of the default
        https://www.domain.com/favicon.ico file, or to return it as a probable result
        which still requires verification, like the other results.
    :type verify_default_icon: bool

    :param request_kwargs: Request headers argument.
    :type request_kwargs: Dict

    :return: Icon or None.
    :rtype: :class:`Icon` or None
    """
    parsed = urlparse(url)
    favicon_url = urlunparse((parsed.scheme, parsed.netloc, 'favicon.ico', '', '', ''))
    if not verify_default_icon:
        return Icon(favicon_url, 0, 0, 'ico')

    response = requests.head(favicon_url, **request_kwargs)
    if response.status_code == 200:
        return Icon(response.url, 0, 0, 'ico')


def tags(url, html):
    """Get icons from link and meta tags.

    .. code-block:: html

       <link rel="apple-touch-icon" sizes="144x144" href="apple-touch-icon.png">
       <meta name="msapplication-TileImage" content="favicon.png">

    :param url: Url for site.
    :type url: str

    :param html: Body of homepage.
    :type html: str

    :return: Icons found.
    :rtype: set
    """
    soup = BeautifulSoup(html, features='html.parser')

    link_tags = set()
    for rel in LINK_RELS:
        for link_tag in soup.find_all(
            'link', attrs={'rel': lambda r: r and r.lower() == rel, 'href': True}
        ):
            link_tags.add(link_tag)

    meta_tags = set()
    for meta_tag in soup.find_all('meta', attrs={'content': True}):
        meta_type = meta_tag.get('name') or meta_tag.get('property') or ''
        meta_type = meta_type.lower()
        for name in META_NAMES:
            if meta_type == name.lower():
                meta_tags.add(meta_tag)

    icons = set()
    for tag in link_tags | meta_tags:
        href = tag.get('href', '') or tag.get('content', '')
        href = href.strip()

        if not href or href.startswith('data:image/'):
            continue

        if is_absolute(href):
            url_parsed = href
        else:
            url_parsed = urljoin(url, href)

        # repair '//cdn.network.com/favicon.png' or `icon.png?v2`
        scheme = urlparse(url).scheme
        url_parsed = urlparse(url_parsed, scheme=scheme)

        width, height = dimensions(tag)
        _, ext = os.path.splitext(url_parsed.path)

        icon = Icon(url_parsed.geturl(), width, height, ext[1:].lower())
        icons.add(icon)

    return icons


def is_absolute(url):
    """Check if url is absolute.

    :param url: Url for site.
    :type url: str

    :return: True if homepage and false if it has a path.
    :rtype: bool
    """
    return bool(urlparse(url).netloc)


def dimensions(tag):
    """Get icon dimensions from size attribute or icon filename.

    :param tag: Link or meta tag.
    :type tag: :class:`bs4.element.Tag`

    :return: If found, width and height, else (0,0).
    :rtype: tuple(int, int)
    """
    sizes = tag.get('sizes', '')
    if sizes and sizes != 'any':
        size = sizes.split(' ')  # '16x16 32x32 64x64'
        size.sort(reverse=True)
        width, height = re.split(r'[x\xd7/]', size[0])
    else:
        filename = tag.get('href') or tag.get('content')
        size = SIZE_RE.search(filename)
        if size:
            width, height = size.group('width'), size.group('height')
        else:
            width, height = '0', '0'

    # repair bad html attribute values: sizes='192x192+'
    width = ''.join(c for c in width if c.isdigit())
    height = ''.join(c for c in height if c.isdigit())
    return int(width), int(height)
