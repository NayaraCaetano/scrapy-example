# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import date
from datetime import datetime

class ForeignPrincipalsPipeline(object):
    def process_item(self, item, spider):
        d = dict(item)
        
        # Serialize the date in the ISO 8601 format and
        # replace the field 'date' to '$date' to be compatible with the MongoDB's Extended JSON format in the strict mode:
        # https://docs.mongodb.com/manual/reference/mongodb-extended-json/#data_date
        d['$date'] = item['date'].isoformat() + 'Z'
        del d['date']
        
        return d
