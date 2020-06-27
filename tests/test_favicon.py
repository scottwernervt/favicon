# -*- coding: utf-8 -*-
import pytest
from bs4 import BeautifulSoup

import favicon
from favicon.favicon import is_absolute

s = BeautifulSoup(features='html.parser')


@pytest.mark.parametrize(
    'url,expected',
    [
        ('http://mock.com/', 'http://mock.com/favicon.ico'),
        ('https://mock.com/', 'https://mock.com/favicon.ico'),
        ('http://mock.com/mock/', 'http://mock.com/favicon.ico'),
        ('http://mock.com/mock/index.html', 'http://mock.com/favicon.ico'),
        (
            'http://mock.com/mock/index.html?q=mock',
            'http://mock.com/favicon.ico'
        ),
        (
            'http://mock.com:80/mock/index.html?q=mock',
            'http://mock.com:80/favicon.ico'
        ),
    ],
    ids=[
        'default',
        'https',
        'folder',
        'file',
        'parameter',
        'port',
    ],
)
def test_default(m, url, expected):
    m.get(url, text='body')
    m.head(expected, text='icon')
    m.get(expected, text='icon')

    icons = favicon.get(url)
    assert icons

    icon = icons[0]
    assert icon.url == expected


@pytest.mark.parametrize(
    'link',
    [
        '<link rel="icon" href="favicon.ico">',
        '<link rel="ICON" href="favicon.ico">',
        '<link rel="shortcut icon" href="favicon.ico">',
        '<link rel="apple-touch-icon" href="favicon.ico">',
        '<link rel="apple-touch-icon-precomposed" href="favicon.ico">',
    ],
    ids=[
        'icon',
        'ICON (#7)',
        'shortcut icon',
        'apple-touch-icon',
        'apple-touch-icon-precomposed',
    ],
)
def test_link_tag(m, link):
    m.get('http://mock.com/', text=link)

    icons = favicon.get('http://mock.com/')
    assert icons


@pytest.mark.parametrize(
    'link,size',
    [
        ('<link rel="icon" href="logo.png" sizes="any">', (0, 0)),
        ('<link rel="icon" href="logo.png" sizes="16x16">', (16, 16)),
        ('<link rel="icon" href="logo.png" sizes="24x24+">', (24, 24)),
        ('<link rel="icon" href="logo.png" sizes="32x32 64x64">', (64, 64)),
        ('<link rel="icon" href="logo.png" sizes="64x64 32x32">', (64, 64)),
        ('<link rel="icon" href="logo-128x128.png" sizes="any">', (128, 128)),
        (u'<link rel="icon" href="logo.png" sizes="16×16">', (16, 16)),
    ],
    ids=[
        'any',
        '16x16',
        '24x24+',
        '32x32 64x64',
        '64x64 32x32',
        'logo-128x128.png',
        'new york times (#9)',
    ],
)
def test_link_tag_sizes_attribute(m, link, size):
    m.get('http://mock.com/', text=link)

    icons = favicon.get('http://mock.com/')
    assert icons

    icon = icons[0]
    assert icon.width == size[0] and icon.height == size[1]


@pytest.mark.parametrize(
    'link,url',
    [
        ('<link rel="icon" href="logo.png">', 'http://mock.com/logo.png'),
        ('<link rel="icon" href="logo.png\t">', 'http://mock.com/logo.png'),
        (
            '<link rel="icon" href="/static/logo.png">',
            'http://mock.com/static/logo.png',
        ),
        (
            '<link rel="icon" href="https://cdn.mock.com/logo.png">',
            'https://cdn.mock.com/logo.png',
        ),
        (
            '<link rel="icon" href="//cdn.mock.com/logo.png">',
            'http://cdn.mock.com/logo.png',
        ),
        (
            '<link rel="icon" href="http://mock.com/logo.png?v2">',
            'http://mock.com/logo.png?v2',
        ),
    ],
    ids=[
        'filename',
        'filename \\t (#5)',
        'relative',
        'https',
        'forward slashes',
        'query string (#7)',
    ],
)
def test_link_tag_href_attribute(m, link, url):
    m.get('http://mock.com/', text=link)

    icons = favicon.get('http://mock.com/')
    assert icons

    icon = icons[0]
    assert icon.url == url


def test_link_tag_empty_href_attribute(m):
    """'NoneType' object has no attribute 'strip' #22"""
    m.get('http://mock.com/', text='<link rel="icon" href="">')

    with pytest.warns(None):
        icons = favicon.get('http://mock.com/')

    assert not icons


@pytest.mark.parametrize(
    'meta_tag',
    [
        '<meta name="msapplication-TileImage" content="favicon.ico">',
        '<meta name="msapplication-tileimage" content="favicon.ico">',
        '<meta property="og:image" content="favicon.png">',
    ],
    ids=['msapplication-TileImage', 'msapplication-tileimage', 'og:image'],
)
def test_meta_tag(m, meta_tag):
    m.get('http://mock.com/', text=meta_tag)

    icons = favicon.get('http://mock.com/')
    assert icons


def test_invalid_meta_tag(m):
    m.get(
        'http://mock.com/',
        text='<meta content="en-US" data-rh="true" itemprop="inLanguage"/>',
    )

    icons = favicon.get('http://mock.com/')
    assert not icons


def test_request_kwargs(m):
    """Add request timeout #21"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    }
    m.get('http://mock.com/', request_headers=headers, text='body')

    favicon.get('http://mock.com/', headers=headers)

    # Test deprecated header argument
    with pytest.warns(DeprecationWarning):
        favicon.get('http://mock.com/', headers)


@pytest.mark.parametrize(
    'url,expected',
    [
        ('http://mock.com/favicon.ico', True),
        ('favicon.ico', False),
        ('/favicon.ico', False),
    ],
)
def test_is_absolute_helper(url, expected):
    assert is_absolute(url) == expected


def test_html_input():
    # contents of mock.com
    mock_com_html = '''<!DOCTYPE html><!--[if lt IE 7]><html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en-US" prefix="og: http://ogp.me/ns#"> <![endif]--><!--[if IE 7]><html class="no-js lt-ie9 lt-ie8" lang="en-US" prefix="og: http://ogp.me/ns#"> <![endif]--><!--[if IE 8]><html class="no-js lt-ie9" lang="en-US" prefix="og: http://ogp.me/ns#"> <![endif]--><!--[if gt IE 8]><!--><html class="no-js" lang="en-US" prefix="og: http://ogp.me/ns#"> <!--<![endif]--><head>    <meta charset="utf-8">    <title>Home - MOCK.com</title>    <meta name="viewport" content="width=device-width, initial-scale=1.0">    <link rel="shortcut icon" type="image/x-icon" href="http://mock.com/wp-content/uploads/2014/03/favicon.ico"/>    <link rel="canonical" href="http://mock.com/"/>    <meta property="og:locale" content="en_US"/>    <meta property="og:type" content="website"/>    <meta property="og:title" content="Home - MOCK.com"/>    <meta property="og:url" content="http://mock.com/"/>    <meta property="og:site_name" content="MOCK.com"/></head><body>Test</body></html>''' # noqa

    icons = favicon.get(
        'http://mock.com/',
        html_override=mock_com_html,
    )
    assert icons
    icons.sort(key=lambda icon: icon.url)
    assert icons[0].url == 'http://mock.com/favicon.ico'
    assert icons[1].url == 'http://mock.com/wp-content/uploads/2014/03/favicon.ico'
