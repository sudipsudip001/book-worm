# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookWormItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    scrape_date = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    upc = scrapy.Field()
    rating = scrapy.Field()
