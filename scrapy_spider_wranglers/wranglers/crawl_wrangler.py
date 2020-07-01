# stdlib
import warnings
from typing import List

# local
from .base_wrangler import SpiderWrangler
import scrapy_spider_wranglers.utils.wrangler_utils as wu


class CrawlSpiderWrangler(SpiderWrangler):

    def __init__(self, spidercls = None, custom_settings: dict = None,
                 extractor_config: List[dict] = None):

        super().__init__(spidercls=spidercls, custom_settings=custom_settings)

        # subclass attributes #
        self.extractor_config = extractor_config

    def construct_temp_spider(self) -> type:
        # construct settings
        temp_settings = wu.construct_custom_settings(self.spidercls, self.custom_settings)

        # construct rules
        rule_templates = self.spidercls.rule_templates

        temp_rules = []

        for i in range(len(self.spidercls.rule_configs)):
            try:
                temp_rules.append(wu.construct_rule(self.extractor_config[i], rule_templates[i]))
            except IndexError:
                temp_rules.append(wu.construct_rule(self.extractor_config[-1], rule_templates[i]))

        class_vars = {
            'custom_settings': temp_settings,
            'rules': temp_rules
        }

        return type('temp_spider', (self.spidercls,), class_vars)



