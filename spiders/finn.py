import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from laptop_scraper.items import LaptopItem

class FinnSpider(CrawlSpider):
    name = 'finn'
    allowed_domains = ['finn.no']
    start_urls = ['https://www.finn.no/bap/forsale/search.html?abTestKey=suggestions&product_category=2.93.3215.43&search_type=SEARCH_ID_BAP_ALL&sort=PUBLISHED_DESC']

    rules = (
        # Next page:
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="__next"]/main/div[2]/div/div/nav/a', )), follow=True),
        
        # Ad postings:
        Rule(LinkExtractor(restrict_xpaths=('//*[@class="ads__unit__link"]'), allow=r'\/bap\/forsale\/ad.html\?finnkode=\d?'), callback='parse_item'),
    )

    def parse_item(self, response):
        article_body = response.xpath('/html/body/main/div/div[3]/div[1]')

        item = LaptopItem()
        item['_id'] = response.xpath('//tr[th="FINN-kode"]/th/following-sibling::td[1]/span/text()').get()
        item['_url'] = response.url
        item['last_changed'] = response.xpath('//tr[th="Sist endret"]/th/following-sibling::td[1]/text()').get()
        item['title'] = article_body.xpath('article/section[1]/h1/text()').get()
        item['price'] = article_body.xpath('article/section[1]/div[2]/text()').get()
        item['body'] = article_body.xpath('article/section[2]/div/div/div/div/text()').get()
        item['brand'] = article_body.xpath('.//tr[th="Merke"]/th/following-sibling::td[1]/text()').get()
        item['condition'] = article_body.xpath('.//tr[th="Tilstand"]/th/following-sibling::td[1]/text()').get()
        item['address'] = article_body.xpath('div/h3/text()').get()
        item['images'] = article_body.xpath('.//img[@alt="Galleribilde"]').xpath('@src').getall()

        return ItemLoader(item=item, response=response).load_item()
