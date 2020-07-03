# stdlib
import unittest

# local
from tests.testing_spiders import TestCrawlSpider
from scrapy_dynamic_spiders.factories import CrawlSpiderClsFactory


class TestCrawlFactory(unittest.TestCase):

    def setUp(self):
        custom_settings = {
            'test_setting_3': 3
        }
        extractor_configs = [{}, {}]
        rule_configs = [{}, {}]

        self.factory = CrawlSpiderClsFactory(custom_settings=custom_settings,
                                             extractor_configs=extractor_configs,
                                             rule_configs=rule_configs)

    def test_rule_concat(self):
        test_class = self.factory.construct_spider(TestCrawlSpider)

        self.assertEqual(len(test_class.rules), 3)
        self.assertEqual(test_class.rules[-1].callback, None)

    def test_rule_ow(self):
        self.factory.rule_ow = True
        test_class = self.factory.construct_spider(TestCrawlSpider)

        self.assertEqual(len(test_class.rules), 2)
        self.assertEqual(test_class.rules[-1].callback, None)


if __name__ == '__main__':
    unittest.main()
