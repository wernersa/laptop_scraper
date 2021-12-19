import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, Compose, MapCompose, TakeFirst
from laptop_scraper.items import LaptopItem

class FinnLaptopSpider(CrawlSpider):
    name = 'FinnLaptop'
    allowed_domains = ['finn.no']
    start_urls = ['https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&product_category=2.93.3215.43&search_type=SEARCH_ID_BAP_ALL&sort=PUBLISHED_DESC']

    rules = (
        # Next page:
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="__next"]/main/div[2]/div/div/nav/a', )), follow=True),
        
        # Ad postings:
        Rule(LinkExtractor(restrict_xpaths=('//*[@class="ads__unit__link"]'), allow=r'\/bap\/forsale\/ad.html\?finnkode=\d?'), callback='parse_item'),
    )

    def parse_item(self, response):

        item = LaptopItem()
        selector = scrapy.Selector(response)
        loader = ItemLoader(item, selector=selector)

        loader.default_input_processor = Compose()
        loader.default_output_processor = Compose(TakeFirst())

        loader.add_value('url', response.url)

        # Select content scope of the page that is relevant
        content_loader = loader.nested_xpath(item.content_body)

        # iterate over fields and add xpaths to the loader
        for key, field in item.fields.items():
            if field.get('xpath'):
                if field.get('xpath')[0] != "/":
                    # Use content scope xpath when relative xpaths
                    content_loader.add_xpath(key, field.get('xpath'))
                else:
                    # Use top level scope xpath when absolute xpaths
                    loader.add_xpath(key, field.get('xpath'))

        yield loader.load_item()

