# third party
import crochet
from twisted.internet.defer import Deferred
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

# local
from scrapy_spider_wranglers.factories import SpiderClsFactory


class SpiderWrangler:
    """Provides an API for the dynamic creation and/or sequential running of Scrapy Spiders, including basic, XMLFeed,
    CSVFeed, and Sitemap spiders."""
    _settings = get_project_settings()

    def __init__(self, spidercls = None, gen_spiders: bool = True,
                 custom_settings: dict = None, settings_ow: bool = False):

        # setup crochet reactor thread if not already present#
        crochet.setup()

        # attributes #
        # private
        self._runner = CrawlerRunner(get_project_settings())
        self._clsfactory = SpiderClsFactory(custom_settings=custom_settings, settings_ow=settings_ow)

        # public
        self.spidercls = spidercls
        self.gen_spiders = gen_spiders

    @crochet.wait_for(_settings.getint('WRANGLER_MAX_CRAWL_TIME', 1800))
    def start_crawl(self, *args, **kwargs) -> Deferred:
        """
        Initiates a crawl. If gen_spider=True, creates a temporary spider class based on factory settings

        :return: A Deferred object passed to the crochet reactor thread
        """
        if self.gen_spiders:
            TempSpider = self._clsfactory.construct_spider(self.spidercls)
            return self._runner.crawl(TempSpider, *args, **kwargs)

        else:
            return self._runner.crawl(self.spidercls, *args, **kwargs)

    @property
    def custom_settings(self):
        return self._clsfactory.custom_settings

    @custom_settings.setter
    def custom_settings(self, value):
        self._clsfactory.custom_settings = value

    @property
    def settings_ow(self):
        return self._clsfactory.settings_ow

    @settings_ow.setter
    def settings_ow(self, value):
        self._clsfactory.settings_ow = value

