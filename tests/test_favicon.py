import pytest
from bs4 import BeautifulSoup

import favicon
from favicon.favicon import is_absolute

s = BeautifulSoup('')


def test_default(m):
    m.get('http://mock.com/', text='body')
    m.head('http://mock.com/favicon.ico', text='icon')
    m.get('http://mock.com/favicon.ico', text='icon')

    icons = favicon.get('http://mock.com/')
    assert icons

    icon = icons[0]
    assert icon.url == 'http://mock.com/favicon.ico'


@pytest.mark.parametrize('link', [
    '<link rel="icon" href="favicon.ico">',
    '<link rel="ICON" href="favicon.ico">',
    '<link rel="shortcut icon" href="favicon.ico">',
    '<link rel="apple-touch-icon" href="favicon.ico">',
    '<link rel="apple-touch-icon-precomposed" href="favicon.ico">',
], ids=[
    'icon',
    'ICON (#7)',
    'shortcut icon',
    'apple-touch-icon',
    'apple-touch-icon-precomposed',
])
def test_link_rel_attribute(m, link):
    m.head('http://mock.com/favicon.ico', text='Not Found', status_code=404)
    m.get('http://mock.com/', text=link)

    icons = favicon.get('http://mock.com/')
    assert icons


@pytest.mark.parametrize('link,size', [
    ('<link rel="icon" href="logo.png" sizes="any">', (0, 0)),
    ('<link rel="icon" href="logo.png" sizes="16x16">', (16, 16)),
    ('<link rel="icon" href="logo.png" sizes="24x24+">', (24, 24)),
    ('<link rel="icon" href="logo.png" sizes="32x32 64x64">', (64, 64)),
    ('<link rel="icon" href="logo.png" sizes="64x64 32x32">', (64, 64)),
    ('<link rel="icon" href="logo-128x128.png" sizes="any">', (128, 128)),
], ids=[
    'any',
    '16x16',
    '24x24+',
    '32x32 64x64',
    '64x64 32x32',
    'logo-128x128.png',
])
def test_link_sizes_attribute(m, link, size):
    m.head('http://mock.com/favicon.ico', text='Not Found', status_code=404)
    m.get('http://mock.com/', text=link)

    icons = favicon.get('http://mock.com/')
    assert icons

    icon = icons[0]
    assert icon.width == size[0] and icon.height == size[1]


@pytest.mark.parametrize('link,url', [
    ('<link rel="icon" href="logo.png">', 'http://mock.com/logo.png'),
    ('<link rel="icon" href="logo.png\t">', 'http://mock.com/logo.png'),
    ('<link rel="icon" href="/static/logo.png">',
     'http://mock.com/static/logo.png'),
    ('<link rel="icon" href="https://cdn.mock.com/logo.png">',
     'https://cdn.mock.com/logo.png'),
    ('<link rel="icon" href="//cdn.mock.com/logo.png">',
     'http://cdn.mock.com/logo.png'),
    ('<link rel="icon" href="http://mock.com/logo.png?v2">',
     'http://mock.com/logo.png?v2'),
], ids=[
    'filename',
    'filename \\t (#5)',
    'relative',
    'https',
    'forward slashes',
    'query string (#7)',
])
def test_link_href_attribute(m, link, url):
    m.head('http://mock.com/favicon.ico', text='Not Found', status_code=404)
    m.get('http://mock.com/', text=link)

    icons = favicon.get('http://mock.com/')
    assert icons

    icon = icons[0]
    assert icon.url == url


@pytest.mark.parametrize('url,expected', [
    ('http://mock.com/favicon.ico', True),
    ('favicon.ico', False),
    ('/favicon.ico', False),
])
def test_is_absolute(url, expected):
    assert is_absolute(url) == expected
