# third party
import crochet
from twisted.internet.defer import Deferred
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings


class SpiderWrangler:
    """Provides an API for the dynamic creation and/or sequential running of Scrapy Spiders, including basic, XMLFeed,
    CSVFeed, and Sitemap spiders."""
    _settings = get_project_settings()

    def __init__(self, spidercls = None, clsfactory = None, gen_spiders: bool = True, **kwargs):
        # setup crochet reactor thread if not already present#
        crochet.setup()

        # attributes #
        # private
        self._runner = CrawlerRunner(get_project_settings())
        self._clsfactory = clsfactory(**kwargs) if clsfactory else None

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
            if not self.clsfactory:
                raise AttributeError('gen_spider set to True, but no SpiderClsFactory set.')
            else:
                TempSpider = self.clsfactory.construct_spider(self.spidercls)
                return self._runner.crawl(TempSpider, *args, **kwargs)
        else:
            return self._runner.crawl(self.spidercls, *args, **kwargs)

    @property
    def clsfactory(self):
        return self._clsfactory

    @clsfactory.setter
    def clsfactory(self, clsfactory, **kwargs):
        self._clsfactory = clsfactory(**kwargs)
