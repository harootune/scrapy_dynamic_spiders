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
    """Provides an interface for the dynamic creation and running of Scrapy Spiders"""
    _settings = get_project_settings()

    def __init__(self, spidercls = None, custom_settings: dict = None):
        # Set up crochet so Twisted's reactor doesn't explode
        crochet.setup()

        # attributes #
        # private
        self._runner = CrawlerRunner(get_project_settings())

        # public
        self.spidercls = spidercls
        self.custom_settings = custom_settings

    def construct_temp_spider(self) -> type:
        temp_settings = wu.construct_custom_settings(self.spidercls, self.custom_settings)
        class_vars = {
            'custom_settings': temp_settings
        }
        return type('temp_spider', (self.spidercls,), class_vars)

    @crochet.wait_for(_settings.getint('WRANGLER_MAX_CRAWL_TIME', 1800))
    def start_crawl(self, *args, **kwargs) -> Deferred:
        """Initiates a crawl"""
        if not self.spidercls:
            warnings.warn('Crawl aborted: No spider class selected')
        else:
            TempSpider = self.construct_temp_spider()

            return self._runner.crawl(TempSpider, *args, **kwargs)