# stdlib
from typing import List

# local
from .base_wrangler import SpiderWrangler
from scrapy_spider_wranglers.factories import CrawlSpiderClsFactory


class CrawlSpiderWrangler(SpiderWrangler):
    """Provides an API for the dynamic creation and/or sequential running of Scrapy CrawlSpiders"""
    def __init__(self, spidercls = None, gen_spiders: bool = True,
                 custom_settings: dict = None, settings_ow: bool = False,
                 extractor_configs: List[dict] = None, rule_configs: List[dict] = None, rule_ow: bool = False):

        # parent constructor #
        super().__init__(spidercls=spidercls, gen_spiders=gen_spiders)

        # attributes #
        # private
        self._clsfactory = CrawlSpiderClsFactory(custom_settings=custom_settings, settings_ow=settings_ow,
                                                 extractor_configs=extractor_configs, rule_configs=rule_configs, rule_ow=rule_ow)

    @property
    def extractor_configs(self):
        return self._clsfactory.extractor_configs

    @extractor_configs.setter
    def extractor_configs(self, value):
        self._clsfactory.extractor_configs = value

    @property
    def rule_configs(self):
        return self._clsfactory.rule_configs

    @rule_configs.setter
    def rule_configs(self, value):
        self._clsfactory.rule_configs = value

    @property
    def rule_ow(self):
        return self._clsfactory.rule_ow

    @rule_ow.setter
    def rule_ow(self, value):
        self._clsfactory.rule_ow = value




