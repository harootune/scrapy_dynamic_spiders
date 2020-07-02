# stdlib
import unittest

# local
from tests.testing_spiders import TestSpider
from scrapy_spider_wranglers.wranglers import SpiderWrangler


class TestBaseWrangler(unittest.TestCase):

    def setUp(self):
        self.custom_settings = {
            'test_setting_3': 3
        }
        self.wrangler = SpiderWrangler(spidercls=TestSpider, reactor=False)

    def test_settings_concat(self):
        self.wrangler.custom_settings = self.custom_settings

        test_class = self.wrangler.construct_temp_spider()
        self.assertEqual(len(test_class.custom_settings.keys()), 3)

    def test_settings_ow(self):
        self.wrangler.settings_ow = True
        self.wrangler.custom_settings = self.custom_settings

        test_class = self.wrangler.construct_temp_spider()
        self.wrangler.settings_ow = False
        self.assertEqual(len(test_class.custom_settings.keys()), 1)


if __name__ == '__main__':
    unittest.main()


