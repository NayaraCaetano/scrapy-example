# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ForeignPrincipal(Item):
    url = Field()
    country = Field()
    state = Field()
    reg_num = Field()
    address = Field()
    foreign_principal = Field()
    date = Field()
    registrant = Field()
    exhibit_url = Field()
    