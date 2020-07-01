# third party
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


def construct_rule(extractor_config: dict, rule_template: dict) -> Rule:
    return Rule(LinkExtractor(**extractor_config), **rule_template)


def construct_custom_settings(spidercls, custom_settings: dict) -> dict:
    """Dynamically constructs custom settings for a temporary spider class. Colliding settings will favor those in
    the custom_settings parameter"""
    try:
        settings = spidercls.custom_settings.deepcopy()
    except AttributeError:
        settings = {}

    for key, value in custom_settings.items():
        settings[key] = value

    return settings
