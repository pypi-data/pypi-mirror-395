from django import template
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join

from ..conf import settings

register = template.Library()


SVG_TEMPLATE = '<svg{}>{}<use href="{}#{}"/></svg>'


@register.simple_tag
def svg_sprite(id_, title=None, **kwargs):
    """The `svg_sprite` template tag."""
    sprite = settings.SVG_SPRITE
    if not sprite:
        raise ImproperlyConfigured('The SVG_SPRITE setting must not be empty.')

    title_tag = format_html('<title>{}</title>', title) if title else ''

    attributes = settings.SVG_SPRITE_DEFAULT_ATTRIBUTES | kwargs
    attributes_str = format_html_join(
        '', ' {}="{}"', ((key, value) for key, value in attributes.items() if value)
    )

    path = static(sprite)

    return format_html(SVG_TEMPLATE, attributes_str, title_tag, path, id_)
