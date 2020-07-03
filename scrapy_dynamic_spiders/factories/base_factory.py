# stdlib
import copy


class SpiderClsFactory:
    """Generates temporary Spider classes based on the factory's attributes. Can handle basic, XMLFeed, CSVFeed,
    and Sitemap generic spiders"""

    def __init__(self, custom_settings: dict = None, settings_ow: bool = False):
        # attributes #
        # private
        self._count = 0

        # public
        self.custom_settings = custom_settings if custom_settings else {}
        self.settings_ow = settings_ow

    def _construct_custom_settings(self, spidercls) -> dict:
        """
        Constructs a dictionary describing the custom_settings class attribute of a new temporary spider class, based
        on the factory's attributes and the provided template spider class

        :return: a custom_settings dicitonary
        """
        if self.settings_ow:
            settings = {}
        else:
            settings = copy.deepcopy(spidercls.custom_settings)
            if not settings:
                settings = {}

        for key, value in self.custom_settings.items():
            settings[key] = value

        return settings

    def construct_spider(self, spidercls) -> type:
        """
        Generates a temporary spider class based off of a provided temporary class and the factory's attributes

        :return: A Spider-derived class object
        """
        if not spidercls:
            raise TypeError('Cannot construct a Spider without a template class.')

        self._count += 1

        settings = self._construct_custom_settings(spidercls)
        class_vars = {
            'custom_settings': settings
        }
        return type(f'{spidercls.__name__}-{self._count}', (spidercls,), class_vars)