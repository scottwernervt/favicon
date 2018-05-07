"""favicon
:copyright: (c) 2018 by Scott Werner.
:license: MIT, see LICENSE for more details.
"""
# TODO: Icons in manifest.json and browserconfig.xml.
# TODO: MS icons in <meta name='msapplication-TileImage' content='icon.png'>

import os
import re
from collections import namedtuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

__all__ = ['get', 'Icon']

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/33.0.1750.152 Safari/537.36',
}

LINK_RELS = [
    'icon',
    'shortcut icon',
    'apple-touch-icon',
    'apple-touch-icon-precomposed',
]

SIZE_RE = re.compile(
    r'(?P<width>\d{2,4})x(?P<height>\d{2,4})',
    flags=re.IGNORECASE)

Icon = namedtuple('Icon', ['url', 'width', 'height', 'format'])


def get(url, headers=None):
    """Get all fav icons for a url.

    :param url: Homepage.
    :type url: str

    :param headers: Request headers.
    :type headers: dict or None

    :return: List of fav icons found sorted by icon dimension.
    :rtype: list[:class:`Icon`]
    """
    if not headers:
        headers = HEADERS

    response = requests.get(url, headers=headers, allow_redirects=True)
    response.raise_for_status()

    icons = set()

    default_icon = get_default(response.url, headers)
    if default_icon:
        icons.add(default_icon)

    link_icons = get_links(response.url, response.text)
    if link_icons:
        icons.update(link_icons)

    return sorted(icons, key=lambda i: i.width + i.height, reverse=True)


def get_default(url, headers):
    """Get icon using default filename favicon.ico.

    :param url: Url for site.
    :type url: str

    :param headers: Request headers.
    :type headers: dict

    :return: Icon or None.
    :rtype: :class:`Icon` or None
    """
    favicon_url = urljoin(url, 'favicon.ico')
    response = requests.head(favicon_url, headers=headers, allow_redirects=True)
    if response.status_code == 200:
        return Icon(response.url, 0, 0, 'ico')


def get_links(url, html):
    """Get icons from link tags.

    :param url: Url for site.
    :type url: str

    :param html: Body of homepage.
    :type html: str

    :return: Icons found.
    :rtype: set
    """
    soup = BeautifulSoup(html, 'html.parser')

    icons = set()
    for rel in LINK_RELS:
        for link in soup.find_all('link', {'rel': rel, 'href': True}):
            href = link['href']
            if href.startswith('data:image/'):
                # TODO: Add support for 'data:image/png;base64,...'
                continue

            if is_absolute(href):
                icon_url = href
            else:
                icon_url = urljoin(url, href)

            # bad urls: href='//cdn.network.com/favicon.png'
            icon_url = urlparse(icon_url, scheme='https').geturl()

            width, height = dimensions(link)
            _, ext = os.path.splitext(icon_url)

            icon = Icon(icon_url, width, height, ext[1:].lower())
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


def dimensions(link):
    """Get icon dimensions from size attribute or icon filename.

    <link rel="apple-touch-icon" sizes="144x144" href="apple-touch-icon.png">

    :param link: Link tag.
    :type link: :class:`bs4.element.Tag`

    :return: If found, width and height, else (0,0).
    :rtype: tuple(int, int)
    """
    sizes = link.get('sizes', '')
    if sizes and sizes != 'any':
        size = sizes.split(' ')  # '16x16 32x32 64x64'
        size.sort(reverse=True)
        width, height = size[0].split('x')
    else:
        size = SIZE_RE.search(link['href'])
        if size:
            width, height = size.group('width'), size.group('height')
        else:
            width, height = '0', '0'

    # repair bad html attribute values: sizes='192x192+'
    width = ''.join(c for c in width if c.isdigit())
    height = ''.join(c for c in height if c.isdigit())
    return int(width), int(height)
