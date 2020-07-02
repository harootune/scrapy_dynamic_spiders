# stdlib
import copy

# third party
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


def construct_rule(extractor_config: dict, rule_config: dict) -> Rule:
    return Rule(LinkExtractor(**extractor_config), **rule_config)


def construct_custom_settings(spidercls, custom_settings: dict, settings_ow: bool) -> dict:
    """Dynamically constructs custom settings for a temporary spider class. Colliding settings will favor those in
    the custom_settings parameter"""
    if settings_ow:
        settings = {}
    else:
        try:
            settings = copy.deepcopy(spidercls.custom_settings)
        except AttributeError:
            settings = {}

    for key, value in custom_settings.items():
        settings[key] = value

    return settings
