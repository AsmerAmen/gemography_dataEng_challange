# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class NewsPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymongo.MongoClient(
            "mongodb+srv://asmer_amen:newpassword@cluster0.wjnt1.mongodb.net/news?retryWrites=true&w=majority")

    def create_table(self):
        db = self.conn['news']
        self.collection = db['news_data']

    def store_db(self, item):
        self.collection.insert(dict(item))

    def process_item(self, item, spider):
        self.store_db(item)
        return item
