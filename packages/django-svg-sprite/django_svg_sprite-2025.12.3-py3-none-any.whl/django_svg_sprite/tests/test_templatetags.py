from xml.etree import ElementTree

import pytest
from django.core.exceptions import ImproperlyConfigured

from ..templatetags.svg_sprite import svg_sprite


def test_improperly_configured(settings):
    del settings.SVG_SPRITE
    with pytest.raises(ImproperlyConfigured):
        svg_sprite('foo')


def test_svg_sprite():
    expected = '<svg><use href="/static/sprite.svg#circle"/></svg>'
    assert svg_sprite('circle') == expected


def test_title():
    expected = (
        '<svg><title>Foo Bar</title><use href="/static/sprite.svg#circle"/></svg>'
    )
    assert svg_sprite('circle', title='Foo Bar') == expected


def test_attributes():
    expected = (
        '<svg class="foo bar" fill="red"><use href="/static/sprite.svg#circle"/></svg>'
    )
    assert svg_sprite('circle', **{'class': 'foo bar', 'fill': 'red'}) == expected


def test_default_attributes(settings):
    settings.SVG_SPRITE_DEFAULT_ATTRIBUTES = {
        'class': 'icon',
        'fill': '#ff0',
    }
    expected = (
        '<svg class="icon" fill="#ff0"><use href="/static/sprite.svg#circle"/></svg>'
    )
    assert svg_sprite('circle') == expected


def test_default_attributes_override(settings):
    settings.SVG_SPRITE_DEFAULT_ATTRIBUTES = {
        'class': 'foo',
        'fill': '#ff0',
    }
    expected = (
        '<svg class="bar" fill="#ff0"><use href="/static/sprite.svg#circle"/></svg>'
    )
    assert svg_sprite('circle', **{'class': 'bar'}) == expected


def test_default_attributes_remove(settings):
    settings.SVG_SPRITE_DEFAULT_ATTRIBUTES = {
        'class': 'icon',
        'fill': '#ff0',
    }
    expected = '<svg fill="#ff0"><use href="/static/sprite.svg#circle"/></svg>'
    assert svg_sprite('circle', **{'class': None}) == expected


def test_bobby_tables():
    result = svg_sprite('square', foo='"><script>alert("XSS")</script>')
    assert '<script>' not in result
    assert '&lt;script&gt;' in result


def test_parse():
    element = ElementTree.fromstring(
        svg_sprite('circle', title='Foo Bar', width=23, height=42)
    )
    assert element.tag == 'svg'
    assert element.attrib['width'] == '23'
    assert element.attrib['height'] == '42'
    assert element[0].tag == 'title'
    assert element[0].text == 'Foo Bar'
    assert element[1].tag == 'use'
    assert element[1].attrib['href'] == '/static/sprite.svg#circle'
