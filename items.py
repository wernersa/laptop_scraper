# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from email.policy import default
import scrapy
import dateparser
from itemloaders.processors import MapCompose, Compose, TakeFirst
from w3lib.html import strip_html5_whitespace, replace_escape_chars


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
    content_body = '/html/body/main/div/div[3]/div[1]'


    _id             = scrapy.Field(xpath='//tr[th="FINN-kode"]/th/following-sibling::td[1]/span/text()',
                                    output_processor=Compose(lambda v: int(v[0])))

    url             = scrapy.Field() #Set by spider

    last_changed    = scrapy.Field(xpath='//tr[th="Sist endret"]/th/following-sibling::td[1]/text()',
                                    output_processor=Compose(TakeFirst(), extract_date))

    title           = scrapy.Field(xpath='article/section[1]/h1/text()',)

    price           = scrapy.Field(xpath='article/section[1]/div[2]/text()',
                                    output_processor=Compose(TakeFirst(), filter_price))
    
    body            = scrapy.Field(xpath='article/section[2]/div/div/div/div/text()',
                                    output_processor=Compose(TakeFirst(), strip_html5_whitespace, replace_escape_chars))

    brand           = scrapy.Field(xpath='.//tr[th="Merke"]/th/following-sibling::td[1]/text()',)

    condition       = scrapy.Field(xpath='.//tr[th="Tilstand"]/th/following-sibling::td[1]/text()',)

    address         = scrapy.Field(xpath='div/h3/text()',
                                    output_processor=Compose(TakeFirst(), strip_html5_whitespace))

    meta            = scrapy.Field()

    pass



