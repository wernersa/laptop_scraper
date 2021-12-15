# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.utils.project import get_project_settings
from .items import LaptopItem
import datetime

settings = get_project_settings()

class PrintLaptop:
    def process_item(self, item, spider):
        print(item)
        return item


class AddMeta(object):
    def __init__(self, git_version):
        meta_data = {'time_parsed': datetime.datetime.now(),
                     'git_version': settings.get('GIT_COMMIT_DATE')}
    
    def process_item(self, item, spider):
        item['meta'] = self.meta_data
        return item


class MongoDBPipeline:
    def __init__(self):
        conn = pymongo.MongoClient(
            settings.get('MONGO_URI')
        )
        db = conn[settings.get('MONGO_DB_NAME')]
        self.collection = db[settings['MONGO_COLLECTION_NAME']]
        
        # Create a dictionary of currently parsed items
        self.parsed = {x["_id"]: x["last_changed"] for x in self.collection.find({},{ "_id": 1, "last_changed": 1})}

    def process_item(self, item, spider):
        if not isinstance(item, LaptopItem):
            return item

        # Already parsed:
        if item["_id"] in self.parsed:
            if item["last_changed"] == self.parsed.get(item["_id"]):
                print(f"Skipping item:  {item['last_changed']} & {self.parsed.get(item['_id'])}")
                return item
            else:
                query = {"_id": item["_id"]}
                print(f"Deleting old item {query}, and inserting new with old values appended.")
                previously_stored = self.collection.find_one(query)

                # for k in previously_stored.keys():
                for k in ["price", "last_changed"]:
                    if isinstance(previously_stored[k], list):
                        item[k].append(previously_stored[k].pop())
                
                self.collection.delete_one(query)
        
        # Insert new item, or item with old values appended
        self.collection.insert_one(dict(item))

        return item