from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django_svg_sprite',
]

SVG_SPRITE = 'sprite.svg'

STATIC_URL = 'static/'

TIMEZONE = 'UTC'

USE_TZ = True
