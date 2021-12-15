# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import dateparser
from itemloaders.processors import Join, MapCompose, Compose
from w3lib.html import remove_tags


def filter_price(value):
    # Example strings:
    #   "2\xa0800 kr"
    #   "300 kr"
    value = value[:-3]
    value = value.replace('\xa0', '')
    return int(value)


def extract_date(date):
    return dateparser.parse(date, languages=["nb"])


class LaptopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    _id = scrapy.Field(output_processor=Compose(lambda v: int(v[0])))
    _url = scrapy.Field(output_processor=Compose(lambda v: v[0]))
    last_changed = scrapy.Field(output_processor=MapCompose(extract_date))
    title = scrapy.Field()
    price = scrapy.Field(output_processor=MapCompose(filter_price))
    body = scrapy.Field()
    brand = scrapy.Field()
    condition = scrapy.Field()
    address = scrapy.Field()
    images = scrapy.Field()
    meta = scrapy.Field()

    pass



