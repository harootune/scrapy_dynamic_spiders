# stdlib
import unittest

# local
from tests.testing_spiders import TestCrawlSpider
from scrapy_spider_wranglers.wranglers import CrawlSpiderWrangler


class TestCrawlWrangler(unittest.TestCase):

    def setUp(self):
        self.custom_settings = {
            'test_setting_3': 3
        }
        self.extractor_configs = [{}, {}]
        self.rule_configs = [{}, {}]
        self.wrangler = CrawlSpiderWrangler(spidercls=TestCrawlSpider, reactor=False)

    def test_rule_concat(self):
        self.wrangler.custom_settings = self.custom_settings
        self.wrangler.rule_ow = False
        self.wrangler.extractor_configs = self.extractor_configs
        self.wrangler.rule_configs = self.rule_configs

        test_class = self.wrangler.construct_temp_spider()
        self.wrangler.rule_ow = True
        self.assertEqual(len(test_class.rules), 3)

    def test_rule_ow(self):
        self.wrangler.custom_settings = self.custom_settings
        self.wrangler.extractor_configs = self.extractor_configs
        self.wrangler.rule_configs = self.rule_configs

        test_class = self.wrangler.construct_temp_spider()
        self.assertEqual(len(test_class.rules), 2)


if __name__ == '__main__':
    unittest.main()