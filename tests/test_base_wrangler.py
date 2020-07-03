# stdlib
import unittest

# local
from scrapy_dynamic_spiders.wranglers import SpiderWrangler
from scrapy.utils.project import get_project_settings


class TestSpiderWrangler(unittest.TestCase):
    # will generate a dummy settings object
    settings = get_project_settings()

    def setUp(self):
        self.wrangler = SpiderWrangler(self.settings)

    def tearDown(self):
        self.settings = get_project_settings()
        self.wrangler = None

    def test_runner_init(self):
        self.settings.set('BOT_NAME', 'foo')

        self.assertEqual(self.wrangler._runner.settings.get('BOT_NAME'), 'foo')
        self.assertEqual(
            self.settings.get('BOT_NAME'),
            self.wrangler._runner.settings.get('BOT_NAME')
        )


if __name__ == '__main__':
    unittest.main()
