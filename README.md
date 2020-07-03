Scrapy Dynamic Spiders
---

Scrapy configures its Crawler objects using class variables associated with each Spider class. Most of these can be
meaningfully changed using the Spider's constructor, or even with other Spider class methods. However, some class
variables, most notably custom_settings, are accessed *before* Spider instantiation. Crawl rules are similarly accessed
before spider instantiation, though a protected method does allow for rule re-compilation with somewhat unpredictable
results. In certain cases, this can lead to the creation of large numbers of subclasses made solely to handle slightly 
different websites or use cases.

Dynamic Spiders offers a simple, extensible API for generating spider subclasses based on existing ones, as well as 
an API for running crawls in a synchronous environment (using [Crochet](https://github.com/itamarst/crochet)).

### Use Cases

- Mutate your pipeline without putting a million boolean flags in your code
- Rapidly generate large numbers of spider subclasses based on external data
- Run crawls from within a blocking event loop
- Run crawls tailored to user input

### The APIs

What follows is a brief overview of the provided APIs.

#### SpiderClsFactory
```python3
class scrapy_dynamic_spiders.factories.SpiderClsFactory(custom_settings=None, settings_ow=False)
```
This is the basic SpiderClsFactory, which can handle Spider, XmlFeedSpider, CsvFeedSpider, and SitemapSpider subclasses.
It allows for dynamic definition of custom_settings, which is the only thing in these generic spider classes which
have effects before instantiation.

*Attributes*

``custom_settings`` - a custom_settings dictionary.  
``settings_ow`` - determines how custom_settings are handled. If ``True``, the provided settings overwrite any other
custom settings native to the template class. If ``False``, the provided settings are merged with a copy of the native 
settings, with preference for provided settings.

*Methods*

``construct_spiderself, (spidercls) -> type`` - construct_spider returns a subclass of the template ``spidercls`` with 
its ``custom settings`` class variable customized based on the Factory's current attributes.

*Extension*

You should subclass SpiderFactory if you wish to customize class variables besides ``custom_settings``. This is done in
the ``construct_spider`` method, which you will thus need to overwrite. There is one relevant private method which you
may wish to use.

``_construct_custom_settings(self, spidercls) -> dict`` - returns a new ``custom_settings`` dictionary based off of
existing ``custom_settings`` and the Factory's current attributes.

<br>  

#### CrawlSpiderClsFactory
Inherits from SpiderClsFactory.
```python3
class scrapy_dynamic_spiders.factories.CrawlSpiderClsFactory(custom_settings=None, settings_ow=False,
                                         extractor_configs=None, rule_configs=None, rule_ow:=False)
```
This subclass handles rule construction for CrawlSpiders and CrawlSpider subclasses. It uses two lists of dictionaries,
``extractor_configs`` and ``rule_configs`` to create rules dynamically. Each ``extractor_config`` dictionary provides
kwargs to a LinkExtractor, whose corresponding Rule is provided keyword arguments by the dictionary at the matching
index position in ``rule_configs``. If there are fewer  ``extractor_configs`` than ``rule_configs``, the last
``extractor_config`` is used for all extra ``rule_configs``.

*Attributes*

``extractor_configs`` - a list of dictionaries. Each dictionary should contain kwargs for a LinkExtractor object.
``rule_configs`` - a list of dictionaries. Each dictionary should contain kwargs for a Rule object.
``rule_ow`` - if ``True``, any exiting rules are replaced by the dynamically generated rules. If ``false``, new rules
are appended to a copy of the existing rule list.

*Extension*

Extending this subclass should be similar to extending SpiderFactory. There is one private method which you may wish
to use.

``_construct_rule_list(self, spidercls) -> List[Rule]`` - returns a new list of Rule objects based on those in the
template spidercls and the Factory's current attributes.

<br>

#### SpiderWrangler
```python3
class scrapy_dynamic_spiders.wranglers.SpiderWrangler(settings, spidercls = None, clsfactory = None, gen_spiders = True)
```

This class allows you to run scrapy crawls sequentially, within a synchronous context. It does this through a crochet-
managed Twisted Reactor. Because of this, it executes crawls using a composited CrawlerRunner object, rather than a 
CrawlerProcess object. SpiderWranglers offer built-in support for generating spider subclasses using a SpiderClsFactory,
though this behavior is optional.

*Parameters*

``settings`` - a Scrapy Settings object. Required to initialize the composited CrawlerRunner.

*Attributes*

``gen_spiders`` - If ``True``, crawls made using the ``start_crawl`` method will use a spider subclass generated using
the composited SpiderClsFactory. If ``False``, crawls will use the Spider class referenced in the Wrangler's ``spidercls``
attribute. Attempting to crawl with ``gen_spiders=True`` without a ``clsfactory`` raises an error.

``spidercls`` - The Spider class which will be used for crawling or generating subclasses for crawling.

``clsfactory`` - A SpiderClsFactory or subclass instance.

*Methods*

``start_crawl(self, *args, **kwargs) -> Deferred`` - Initiates a crawl which blocks in a synchronous context. Unlike
Scrapy's Core API, this allows you to perform multiple crawls in sequence without having to manually manipulate your
Reactor. ``*args`` and ``**kwargs`` are passed to the Spider's constructor. The Spider class used is either ``spidercls``
or a dynamically-generated subclass of it.

*Extension*

Extension of SpiderWrangler is generally straightforward. However, modifying the behavior of ``start_crawl`` requires
extra attention. ``start_crawl`` is decorated using crochet's ``wait_for`` decorator. To modify the timeout specified by
this decorator, you will need to override the existing ``start_crawl`` method. To simplify this, the primary functionality
of ``start_crawl`` is encapusalated in the private method ``_start_crawl``. Changing the behavior of the decorator thus
requires overriding ``start_crawl`` with a new instance of the ``wait_for`` decorator, and calling ``_start_crawl`` in
the body of the function.

``_start_crawl(self, *args, **kwargs) -> Deferred`` - Wraps the actual functionality of ``start_crawl``. Return the value
return by this function, or a mutation of it, when overriding ``start_crawl``.

<br>

### Tests
Run tests like so.
```bash
python -m unittests tests
```

<br>

### Known Issues
- Running tests results in unclosed sockets. Currently investigating.

<br>

### Changelog

**v1.0.0a1**
- Initial alpha release



