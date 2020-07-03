# stdlib
import unittest

# local
from tests.testing_spiders import TestSpider
from scrapy_dynamic_spiders.factories import SpiderClsFactory


class TestBaseFactory(unittest.TestCase):

    def setUp(self):
        custom_settings = {
            'test_setting_3': 3
        }
        self.factory = SpiderClsFactory(custom_settings=custom_settings)

    def test_settings_concat(self):
        test_class = self.factory.construct_spider(TestSpider)

        self.assertEqual(len(test_class.custom_settings.keys()), 3)
        self.assertEqual(test_class.custom_settings['test_setting_3'], 3)
        self.assertEqual(test_class.custom_settings['test_setting_1'], 1)

    def test_settings_ow(self):
        self.factory.settings_ow = True
        test_class = self.factory.construct_spider(TestSpider)

        self.assertEqual(len(test_class.custom_settings.keys()), 1)
        self.assertEqual(test_class.custom_settings['test_setting_3'], 3)
        self.assertNotIn('test_setting_1', test_class.custom_settings)


if __name__ == '__main__':
    unittest.main()


