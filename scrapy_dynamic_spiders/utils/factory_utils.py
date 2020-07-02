# third party
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


def construct_rule(extractor_config: dict, rule_config: dict) -> Rule:
    """
    Constructs a Rule object using two kwarg dictionaries

    :param extractor_config: a dictionary of kwargs for a LinkExtractor
    :param rule_config: a dictionary of kwargs for a Rule
    :return: a Rule object
    """
    return Rule(LinkExtractor(**extractor_config), **rule_config)
