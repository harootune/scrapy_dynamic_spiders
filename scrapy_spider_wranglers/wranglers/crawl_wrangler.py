# stdlib
import warnings
from typing import List

# local
from .base_wrangler import SpiderWrangler
import scrapy_spider_wranglers.utils.wrangler_utils as wu


class CrawlSpiderWrangler(SpiderWrangler):
    """Provides an API for the dynamic creation and sequential running of Scrapy CrawlSpiders"""
    def __init__(self, spidercls = None, custom_settings: dict = None, settings_ow: bool = False,
                 extractor_configs: List[dict] = None, rule_configs: List[dict] = None, rule_ow: bool = True):

        super().__init__(spidercls=spidercls, custom_settings=custom_settings, settings_ow=settings_ow)

        # subclass attributes #
        self.extractor_configs = extractor_configs if extractor_configs else {}
        self.rule_configs = rule_configs if extractor_configs else {}
        self.rule_ow = rule_ow

    def construct_temp_spider(self) -> type:
        # construct settings
        temp_settings = wu.construct_custom_settings(self.spidercls, self.custom_settings, self.settings_ow)

        # construct rules
        if self.rule_ow:
            temp_rules = []
        else:
            try:
                temp_rules = self.spidercls.rules.deepcopy()
            except AttributeError:
                temp_rules = []

        for i in range(len(self.rule_configs)):
            # handles case where there are fewer extractor configs than rule configs
            try:
                temp_rules.append(wu.construct_rule(self.extractor_configs[i], self.rule_configs[i]))
            except IndexError:
                warnings.warn(f'CrawlSpiderWrangler wrangling {self.spidercls.__name__}: fewer extractor configs than'
                              f'rule configs, using last available.')
                temp_rules.append(wu.construct_rule(self.extractor_configs[-1], self.rule_configs[i]))

        class_vars = {
            'custom_settings': temp_settings,
            'rules': temp_rules
        }

        # construct temp class
        return type('temp_spider', (self.spidercls,), class_vars)



