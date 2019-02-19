# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid

from models import init_db, Article


class RiaspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class PostgresPipeline(object):
    def __init__(self, dbname, host='localhost', port='5432', user='postgres', password='postgres'):
        self.student_id = init_db(dbname=dbname, host=host, port=port, user=user, password=password)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            **crawler.settings.get('POSTGRES_DB'),
            dbname=crawler.settings.get('POSTGRES_DB_NAME')
        )

    def process_item(self, item, spider):
        model = Article(id=uuid.uuid4(), student=self.student_id, **item)
        model.save(force_insert=True)
        return item
