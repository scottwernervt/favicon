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
    mock_com_html = '''<!DOCTYPE html><!--[if lt IE 7]> <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="en-US" prefix="og: http://ogp.me/ns#"> <![endif]--><!--[if IE 7]> <html class="no-js lt-ie9 lt-ie8" lang="en-US" prefix="og: http://ogp.me/ns#"> <![endif]--><!--[if IE 8]> <html class="no-js lt-ie9" lang="en-US" prefix="og: http://ogp.me/ns#"> <![endif]--><!--[if gt IE 8]><!--> <html class="no-js" lang="en-US" prefix="og: http://ogp.me/ns#"> <!--<![endif]--><head> <meta charset="utf-8"> <title>Home - MOCK.com</title> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <link rel="shortcut icon" type="image/x-icon" href="http://mock.com/wp-content/uploads/2014/03/favicon.ico" /> <!-- This site is optimized with the Yoast SEO plugin v9.6 - https://yoast.com/wordpress/plugins/seo/ --><link rel="canonical" href="http://mock.com/" /><meta property="og:locale" content="en_US" /><meta property="og:type" content="website" /><meta property="og:title" content="Home - MOCK.com" /><meta property="og:url" content="http://mock.com/" /><meta property="og:site_name" content="MOCK.com" /><script type='application/ld+json'>{"@context":"https:\/\/schema.org","@type":"WebSite","@id":"http:\/\/mock.com\/#website","url":"http:\/\/mock.com\/","name":"MOCK.com","potentialAction":{"@type":"SearchAction","target":"http:\/\/mock.com\/?s={search_term_string}","query-input":"required name=search_term_string"}}</script><!-- / Yoast SEO plugin. --><link rel='dns-prefetch' href='//fonts.googleapis.com' /><link rel='dns-prefetch' href='//s.w.org' /><link rel="alternate" type="application/rss+xml" title="MOCK.com &raquo; Feed" href="http://mock.com/feed" /><link rel="alternate" type="application/rss+xml" title="MOCK.com &raquo; Comments Feed" href="http://mock.com/comments/feed" /> <script type="text/javascript"> window._wpemojiSettings = {"baseUrl":"https:\/\/s.w.org\/images\/core\/emoji\/11.2.0\/72x72\/","ext":".png","svgUrl":"https:\/\/s.w.org\/images\/core\/emoji\/11.2.0\/svg\/","svgExt":".svg","source":{"concatemoji":"http:\/\/mock.com\/wp-includes\/js\/wp-emoji-release.min.js?ver=5.1.1"}}; !function(a,b,c){function d(a,b){var c=String.fromCharCode;l.clearRect(0,0,k.width,k.height),l.fillText(c.apply(this,a),0,0);var d=k.toDataURL();l.clearRect(0,0,k.width,k.height),l.fillText(c.apply(this,b),0,0);var e=k.toDataURL();return d===e}function e(a){var b;if(!l||!l.fillText)return!1;switch(l.textBaseline="top",l.font="600 32px Arial",a){case"flag":return!(b=d([55356,56826,55356,56819],[55356,56826,8203,55356,56819]))&&(b=d([55356,57332,56128,56423,56128,56418,56128,56421,56128,56430,56128,56423,56128,56447],[55356,57332,8203,56128,56423,8203,56128,56418,8203,56128,56421,8203,56128,56430,8203,56128,56423,8203,56128,56447]),!b);case"emoji":return b=d([55358,56760,9792,65039],[55358,56760,8203,9792,65039]),!b}return!1}function f(a){var c=b.createElement("script");c.src=a,c.defer=c.type="text/javascript",b.getElementsByTagName("head")[0].appendChild(c)}var g,h,i,j,k=b.createElement("canvas"),l=k.getContext&&k.getContext("2d");for(j=Array("flag","emoji"),c.supports={everything:!0,everythingExceptFlag:!0},i=0;i<j.length;i++)c.supports[j[i]]=e(j[i]),c.supports.everything=c.supports.everything&&c.supports[j[i]],"flag"!==j[i]&&(c.supports.everythingExceptFlag=c.supports.everythingExceptFlag&&c.supports[j[i]]);c.supports.everythingExceptFlag=c.supports.everythingExceptFlag&&!c.supports.flag,c.DOMReady=!1,c.readyCallback=function(){c.DOMReady=!0},c.supports.everything||(h=function(){c.readyCallback()},b.addEventListener?(b.addEventListener("DOMContentLoaded",h,!1),a.addEventListener("load",h,!1)):(a.attachEvent("onload",h),b.attachEvent("onreadystatechange",function(){"complete"===b.readyState&&c.readyCallback()})),g=c.source||{},g.concatemoji?f(g.concatemoji):g.wpemoji&&g.twemoji&&(f(g.twemoji),f(g.wpemoji)))}(window,document,window._wpemojiSettings); </script> <style type="text/css">img.wp-smiley,img.emoji {	display: inline !important;	border: none !important;	box-shadow: none !important;	height: 1em !important;	width: 1em !important;	margin: 0 .07em !important;	vertical-align: -0.1em !important;	background: none !important;	padding: 0 !important;}</style>	<link rel='stylesheet' id='wp-block-library-css' href='http://mock.com/wp-includes/css/dist/block-library/style.min.css?ver=5.1.1' type='text/css' media='all' /><link rel='stylesheet' id='kadence_theme-css' href='http://mock.com/wp-content/themes/virtue/assets/css/virtue.css?ver=255' type='text/css' media='all' /><link rel='stylesheet' id='virtue_skin-css' href='http://mock.com/wp-content/themes/virtue/assets/css/skins/default.css' type='text/css' media='all' /><link rel='stylesheet' id='redux-google-fonts-virtue-css' href='http://fonts.googleapis.com/css?family=Pacifico%3A400%7CLato%3A400%2C700%7COpen+Sans%3A400&#038;subset=latin&#038;ver=1437753749' type='text/css' media='all' /><script type='text/javascript' src='http://mock.com/wp-includes/js/jquery/jquery.js?ver=1.12.4'></script><script type='text/javascript' src='http://mock.com/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1'></script><script type='text/javascript' src='http://mock.com/wp-content/themes/virtue/assets/js/vendor/modernizr.min.js'></script><link rel='https://api.w.org/' href='http://mock.com/wp-json/' /><link rel="EditURI" type="application/rsd+xml" title="RSD" href="http://mock.com/xmlrpc.php?rsd" /><link rel="wlwmanifest" type="application/wlwmanifest+xml" href="http://mock.com/wp-includes/wlwmanifest.xml" /> <meta name="generator" content="WordPress 5.1.1" /><link rel='shortlink' href='http://mock.com/' /><link rel="alternate" type="application/json+oembed" href="http://mock.com/wp-json/oembed/1.0/embed?url=http%3A%2F%2Fmock.com%2F" /><link rel="alternate" type="text/xml+oembed" href="http://mock.com/wp-json/oembed/1.0/embed?url=http%3A%2F%2Fmock.com%2F&#038;format=xml" /><script type="text/javascript">	jQuery(document).ready(function(){ jQuery('img[usemap]').rwdImageMaps();	});</script><style type="text/css">	img[usemap] { max-width: 100%; height: auto; }</style><style type="text/css">#logo {padding-top:25px;}#logo {padding-bottom:10px;}#logo {margin-left:0px;}#logo {margin-right:0px;}#nav-main {margin-top:40px;}#nav-main {margin-bottom:10px;}.headerfont, .tp-caption {font-family:Lato;} .topbarmenu ul li {font-family:Open Sans;} #kadbreadcrumbs {font-family:Verdana, Geneva, sans-serif;}.home-message:hover {background-color:#1e73be; background-color: rgba(30, 115, 190, 0.6);} nav.woocommerce-pagination ul li a:hover, .wp-pagenavi a:hover, .panel-heading .accordion-toggle, .variations .kad_radio_variations label:hover, .variations .kad_radio_variations label.selectedValue {border-color: #1e73be;} a, #nav-main ul.sf-menu ul li a:hover, .product_price ins .amount, .price ins .amount, .color_primary, .primary-color, #logo a.brand, #nav-main ul.sf-menu a:hover, .woocommerce-message:before, .woocommerce-info:before, #nav-second ul.sf-menu a:hover, .footerclass a:hover, .posttags a:hover, .subhead a:hover, .nav-trigger-case:hover .kad-menu-name, .nav-trigger-case:hover .kad-navbtn, #kadbreadcrumbs a:hover, #wp-calendar a, .star-rating {color: #1e73be;}.widget_price_filter .ui-slider .ui-slider-handle, .product_item .kad_add_to_cart:hover, .product_item:hover a.button:hover, .product_item:hover .kad_add_to_cart:hover, .kad-btn-primary, html .woocommerce-page .widget_layered_nav ul.yith-wcan-label li a:hover, html .woocommerce-page .widget_layered_nav ul.yith-wcan-label li.chosen a,.product-category.grid_item a:hover h5, .woocommerce-message .button, .widget_layered_nav_filters ul li a, .widget_layered_nav ul li.chosen a, .wpcf7 input.wpcf7-submit, .yith-wcan .yith-wcan-reset-navigation,#containerfooter .menu li a:hover, .bg_primary, .portfolionav a:hover, .home-iconmenu a:hover, p.demo_store, .topclass, #commentform .form-submit #submit, .kad-hover-bg-primary:hover, .widget_shopping_cart_content .checkout,.login .form-row .button, .variations .kad_radio_variations label.selectedValue, #payment #place_order, .wpcf7 input.wpcf7-back, .shop_table .actions input[type=submit].checkout-button, .cart_totals .checkout-button, input[type="submit"].button, .order-actions .button {background: #1e73be;}.color_gray, .subhead, .subhead a, .posttags, .posttags a, .product_meta a {color:#ffffff;}.contentclass, .nav-tabs>.active>a, .nav-tabs>.active>a:hover, .nav-tabs>.active>a:focus {background:transparent url(http://mock.com/wp-content/uploads/2014/04/Background4.jpg) no-repeat center top;}.topclass {background:transparent ;}.headerclass {background: url(http://mock.com/wp-content/uploads/2014/03/Header_351.png) ;}.navclass {background:transparent ;}.footerclass {background:#3d3d3d ;}body {background: url(http://mock.com/wp-content/uploads/2014/04/Background4.jpg); background-position: 0% 0%; }.product_item .product_details h5 {min-height:40px;}[class*="wp-image"] {-webkit-box-shadow: none;-moz-box-shadow: none;box-shadow: none;border:none;}[class*="wp-image"]:hover {-webkit-box-shadow: none;-moz-box-shadow: none;box-shadow: none;border:none;}.page-header {display:none;}.flex-direction-nav {display:none}img.alignleft {margin:0px;padding:10px}</style><!--[if lt IE 9]><script src="http://mock.com/wp-content/themes/virtue/assets/js/vendor/respond.min.js"></script><![endif]--><style type="text/css" title="dynamic-css" class="options-output">header #logo a.brand,.logofont{font-family:Pacifico;line-height:40px;font-weight:400;font-style:normal;font-size:32px;}.kad_tagline{font-family:Lato;line-height:20px;font-weight:400;font-style:normal;color:#444444;font-size:14px;}.product_item .product_details h5{font-family:Lato;line-height:20px;font-weight:700;font-style:normal;font-size:16px;}h1{font-family:Lato;line-height:40px;font-weight:400;font-style:normal;font-size:38px;}h2{font-family:Lato;line-height:40px;font-weight:normal;font-style:normal;font-size:32px;}h3{font-family:Lato;line-height:40px;font-weight:400;font-style:normal;font-size:28px;}h4{font-family:Lato;line-height:40px;font-weight:400;font-style:normal;font-size:24px;}h5{font-family:Lato;line-height:24px;font-weight:700;font-style:normal;font-size:18px;}body{font-family:Verdana, Geneva, sans-serif;line-height:20px;font-weight:400;font-style:normal;font-size:14px;}#nav-main ul.sf-menu a{font-family:"Open Sans";line-height:18px;font-weight:400;font-style:normal;font-size:18px;}#nav-second ul.sf-menu a{font-family:Lato;line-height:22px;font-weight:400;font-style:normal;font-size:18px;}.kad-nav-inner .kad-mnav, .kad-mobile-nav .kad-nav-inner li a,.nav-trigger-case{font-family:Lato;line-height:20px;font-weight:400;font-style:normal;font-size:16px;}</style></head> <body class="home page-template-default page page-id-13 wide"> <div id="wrapper" class="container"> <div id="kt-skip-link"><a href="#content">Skip to Main Content</a></div><header class="banner headerclass" role="banner"> <div class="container"> <div class="row"> <div class="col-md-4 clearfix kad-header-left"> <div id="logo" class="logocase"> <a class="brand logofont" href="http://mock.com/"> <div id="thelogo"> <img src="http://mock.com/wp-content/uploads/2015/06/Mock.comLOGO.png" alt="MOCK.com" class="kad-standard-logo" /> </div> </a> </div> <!-- Close #logo --> </div><!-- close logo span --> <div class="col-md-8 kad-header-right"> <nav id="nav-main" class="clearfix" role="navigation"> <ul id="menu-mainmenu" class="sf-menu"><li class="menu-home menu-item-770"><a href="index.php">Home</a></li><li class="menu-about menu-item-16"><a href="http://mock.com/about">About</a></li><li class="menu-shop sf-dropdown menu-item-27"><a>Shop</a><ul class="sf-dropdown-menu">	<li class="menu-pacific-rim menu-item-29"><a target="_blank" href="http://pacificrim.mock.com">Pacific Rim</a></li>	<li class="menu-the-janoskians menu-item-30"><a target="_blank" href="http://janoskians.mock.com">The Janoskians</a></li></ul></li><li class="menu-contact-us menu-item-24"><a href="http://mock.com/contact-us">Contact Us</a></li></ul> </nav> </div> <!-- Close menuclass--> </div> <!-- Close Row --> <div id="mobile-nav-trigger" class="nav-trigger"> <button class="nav-trigger-case mobileclass collapsed" data-toggle="collapse" data-target=".kad-nav-collapse"> <span class="kad-navbtn"><i class="icon-reorder"></i></span> <span class="kad-menu-name">Menu</span> </button> </div> <div id="kad-mobile-nav" class="kad-mobile-nav"> <div class="kad-nav-inner mobileclass"> <div class="kad-nav-collapse"> <ul id="menu-mainmenu-1" class="kad-mnav"><li class="menu-home menu-item-770"><a href="index.php">Home</a></li><li class="menu-about menu-item-16"><a href="http://mock.com/about">About</a></li><li class="menu-shop sf-dropdown menu-item-27"><a>Shop</a><ul class="sf-dropdown-menu">	<li class="menu-pacific-rim menu-item-29"><a target="_blank" href="http://pacificrim.mock.com">Pacific Rim</a></li>	<li class="menu-the-janoskians menu-item-30"><a target="_blank" href="http://janoskians.mock.com">The Janoskians</a></li></ul></li><li class="menu-contact-us menu-item-24"><a href="http://mock.com/contact-us">Contact Us</a></li></ul> </div> </div> </div> </div> <!-- Close Container --> </header> <div class="wrap contentclass" role="document"> <div class="sliderclass kad-desktop-slider"> <div id="imageslider" class="container"> <div class="flexslider kt-flexslider loading" style="max-width:1170px; margin-left: auto; margin-right:auto;" data-flex-speed="7000" data-flex-anim-speed="600" data-flex-animation="fade" data-flex-auto="1"> <ul class="slides"> <li> <a href="http://janoskians.mock.com" target="_self"> <img src="http://mock.com/wp-content/uploads/2015/06/Large_Janoskians2.png" alt="" /> </a> </li> </ul> </div> <!--Flex Slides--> </div><!--Container--></div><!--sliderclass--> <div id="content" class="container homepagecontent"> <div class="row"> <div class="main col-md-12" role="main"> <div class="entry-content" itemprop="mainContentOfPage"> <div class="homecontent clearfix home-margin"> <p><a href="http://pacificrim.mock.com"><img class="aligncenter size-full wp-image-1027" src="http://mock.com/wp-content/uploads/2013/07/Wide-Pacific-Rim.png" alt="Wide-Pacific-Rim" width="1150" height="290" srcset="http://mock.com/wp-content/uploads/2013/07/Wide-Pacific-Rim.png 1150w, http://mock.com/wp-content/uploads/2013/07/Wide-Pacific-Rim-300x76.png 300w, http://mock.com/wp-content/uploads/2013/07/Wide-Pacific-Rim-1024x258.png 1024w" sizes="(max-width: 1150px) 100vw, 1150px" /></a></p> </div> </div> </div><!-- /.main --> </div><!-- /.row--> </div><!-- /.content --> </div><!-- /.wrap --> <footer id="containerfooter" class="footerclass" role="contentinfo"> <div class="container"> <div class="row"> </div> <div class="footercredits clearfix"> <p>&copy; 2020 MOCK.com</p> </div> </div></footer><script type='text/javascript' src='http://mock.com/wp-content/plugins/responsive-image-maps/jquery.rwdImageMaps.min.js?ver=1.5'></script><script type='text/javascript' src='http://mock.com/wp-includes/js/imagesloaded.min.js?ver=3.2.0'></script><script type='text/javascript' src='http://mock.com/wp-includes/js/masonry.min.js?ver=3.3.2'></script><script type='text/javascript' src='http://mock.com/wp-content/themes/virtue/assets/js/min/plugins-min.js?ver=255'></script><script type='text/javascript' src='http://mock.com/wp-content/themes/virtue/assets/js/main.js?ver=255'></script><script type='text/javascript' src='http://mock.com/wp-includes/js/wp-embed.min.js?ver=5.1.1'></script> </div><!--Wrapper--> </body></html>''' # noqa

    icons = favicon.get(
        'http://mock.com/',
        html=mock_com_html,
    )
    assert icons
    assert icons[0].url == 'http://mock.com/favicon.ico'
    assert icons[1].url == 'http://mock.com/wp-content/uploads/2014/03/favicon.ico'
    print(icons)