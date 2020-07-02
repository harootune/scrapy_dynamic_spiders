# stdlib
import copy
from typing import List

# third party
from scrapy.spiders import Rule

# local
import scrapy_spider_wranglers.utils.factory_utils as f_utils
from scrapy_spider_wranglers.factories import SpiderClsFactory


class CrawlSpiderClsFactory(SpiderClsFactory):
    """Generates temporary CrawlSpider classes based on the factory's attributes."""
    def __init__(self, custom_settings: dict = None, settings_ow: bool = False,
                 extractor_configs: List[dict] = None, rule_configs: List[dict] = None, rule_ow: bool = False):

        # parent contructor #
        super().__init__(custom_settings=custom_settings, settings_ow=settings_ow)

        # public
        self.extractor_configs = extractor_configs if extractor_configs else []
        self.rule_configs = rule_configs if rule_configs else []
        self.rule_ow = rule_ow

    def _construct_rule_list(self, spidercls) -> List[Rule]:
        """
        Constructs a list of rules for a new temporary CrawlSpider subclass, based on the factory's attributes and
        the provided template spider class

        :param spidercls: The CrawlSpider class or a CrawlSpider subclass
        :return: a list of Rules
        """
        # construct rules
        if self.rule_ow:
            rules = []
        else:
            try:
                rules = copy.deepcopy(spidercls.rules)
            except AttributeError:
                rules = []

        for i in range(len(self.rule_configs)):
            if not self.extractor_configs:
                rules.append(f_utils.construct_rule({}, self.rule_configs[i]))
            else:
                # handles case where there are fewer extractor configs than rule configs
                try:
                    rules.append(f_utils.construct_rule(self.extractor_configs[i], self.rule_configs[i]))
                except IndexError:
                    rules.append(f_utils.construct_rule(self.extractor_configs[-1], self.rule_configs[i]))

        return rules

    def construct_spider(self, spidercls) -> type:
        """
        Generates a temporary spider class based off of a provided temporary class and the factory's attributes

        :param spidercls: The CrawlSpider class or a CrawlSpider subclass
        :return: A Spider-derived class object
        """
        if not spidercls:
            raise TypeError('Cannot construct a Spider without a template class.')

        settings = self._construct_custom_settings(spidercls)
        rules = self._construct_rule_list(spidercls)
        class_vars = {
            'custom_settings': settings,
            'rules': rules
        }
        return type('temp_spider', (spidercls,), class_vars)