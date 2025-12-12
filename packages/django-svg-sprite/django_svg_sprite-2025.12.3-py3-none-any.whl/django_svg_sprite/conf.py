from django.conf import settings as django_settings


class Defaults:
    # The file name of the SVG sprite to be used.
    SVG_SPRITE = ''

    # Default attributes that will be added to each sprite (unless overridden).
    SVG_SPRITE_DEFAULT_ATTRIBUTES = {}


class Settings:
    def __getattr__(self, name):
        try:
            return getattr(django_settings, name)
        except AttributeError:
            return getattr(Defaults, name)


settings = Settings()
