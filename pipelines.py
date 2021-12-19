# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.utils.project import get_project_settings
from .items import LaptopItem
import datetime

settings = get_project_settings()


class AddMeta:
    def __init__(self, time_git_commit):
        self.time_git_commit = time_git_commit

    @classmethod
    def from_crawler(cls, crawler):
        return cls(time_git_commit = crawler.settings.get('GIT_COMMIT_DATE'))
    
    def process_item(self, item, spider):
        item['meta'] = {'time_parsed': datetime.datetime.now(),
                        'time_git_commit': self.time_git_commit}

        return item


class MongoDBPipeline:
    def open_spider(self, spider):
        self.conn = pymongo.MongoClient(settings.get('MONGO_URI'))
        self.db = self.conn[settings.get('MONGO_DB_NAME')]
        self.collection = self.db[spider.name]
        
        # Create a dictionary of currently parsed items
        self.parsed = {x["_id"]: x["last_changed"] for x in self.collection.find({},{ "_id": 1, "last_changed": 1})}

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if not isinstance(item, LaptopItem):
            return item

        # When item is previously parsed:
        if item["_id"] in self.parsed:
            if item["last_changed"] == self.parsed.get(item["_id"]):
                print(f"Skipping item:  {item['last_changed']} & {self.parsed.get(item['_id'])}")
                return item
            else:
                query = {"_id": item["_id"]}
                print(f"Deleting old item {query}, and inserting new with old values appended.")

                # TODO: Store previous values of ["price", "last_changed"]
                # previously_stored = self.collection.find_one(query)
                # item[k].append(previously_stored[k].pop())
                
                self.collection.delete_one(query)
        
        
        # Insert item to database
        self.collection.insert_one(dict(item))

        return item