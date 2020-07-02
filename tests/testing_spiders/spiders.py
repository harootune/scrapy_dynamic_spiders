# third_party
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class TestSpider(Spider):
    def __init__(self):
        super().__init__()

    custom_settings = {
        'test_setting_1': 1,
        'test_setting_2': 2,
    }


class TestCrawlSpider(CrawlSpider):
    def __init__(self):
        super().__init__()

    custom_settings = {
        'test_setting_1': 1,
        'test_setting_2': 2,
    }

    rules = [
        Rule(LinkExtractor())
    ]
