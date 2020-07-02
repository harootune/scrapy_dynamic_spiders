# stdlib
import warnings

# third party
import crochet
from twisted.internet.defer import Deferred
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

# local
import scrapy_spider_wranglers.utils.wrangler_utils as wu


class SpiderWrangler:
    """Provides an API for the dynamic creation and sequential running of Scrapy Spiders, including basic, XMLFeed,
    CSVFeed, and Sitemap spiders."""
    _settings = get_project_settings()

    def __init__(self, spidercls = None, custom_settings: dict = None, settings_ow: bool = False, reactor: bool = True):
        if reactor:
            crochet.setup()

        # attributes #
        # private
        self._runner = CrawlerRunner(get_project_settings())
        self._reactor = reactor

        # public
        self.spidercls = spidercls
        self.custom_settings = custom_settings
        self.settings_ow = settings_ow

    def construct_temp_spider(self) -> type:
        temp_settings = wu.construct_custom_settings(self.spidercls, self.custom_settings, self.settings_ow)
        class_vars = {
            'custom_settings': temp_settings
        }
        return type('temp_spider', (self.spidercls,), class_vars)

    @crochet.wait_for(_settings.getint('WRANGLER_MAX_CRAWL_TIME', 1800))
    def _start_crawl(self, *args, **kwargs) -> Deferred:
        """Initiates a crawl"""
        if not self.spidercls:
            warnings.warn('Crawl aborted: No spider class selected')
        else:
            TempSpider = self.construct_temp_spider()

            return self._runner.crawl(TempSpider, *args, **kwargs)

    def start_crawl(self, *args, **kwargs) -> Deferred:
        """A public wrapper for _start_crawl which aborts the crawl if the crochet reactor has not been activated"""
        if not self._reactor:
            warnings.warn('Crawl aborted: Reactor flag set to false, crawl potentially unsafe')
        else:
            return self._start_crawl(*args, **kwargs)