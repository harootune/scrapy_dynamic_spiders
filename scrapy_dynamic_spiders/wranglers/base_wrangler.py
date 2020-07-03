# third party
import crochet
from twisted.internet.defer import Deferred
from scrapy.crawler import CrawlerRunner


class SpiderWrangler:
    """Provides an API for the dynamic creation and/or sequential running of Scrapy Spiders, including basic, XMLFeed,
    CSVFeed, Sitemap, and CrawlSpiders"""

    def __init__(self, settings, spidercls = None, clsfactory = None, gen_spiders: bool = True):
        # setup crochet reactor thread if not already present#
        crochet.setup()

        # attributes #
        # private
        self._runner = CrawlerRunner(settings)

        # public
        self.clsfactory = clsfactory
        self.spidercls = spidercls
        self.gen_spiders = gen_spiders

    @crochet.wait_for(1800)
    def start_crawl(self, *args, **kwargs) -> Deferred:
        """Wraps _start_crawl and provides the necessary decorator"""
        return self._start_crawl(*args, **kwargs)

    def _start_crawl(self, *args, **kwargs) -> Deferred:
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

