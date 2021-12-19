import sys
import os

import pymongo
from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError


class Command(ScrapyCommand):
# Based on Scrapy commands:
# https://github.com/scrapy/scrapy/tree/master/scrapy/commands

    requires_project = True

    def syntax(self):
        return "<spider>"

    def short_desc(self):
        return "Reset the database of a spider. Deletes all data."

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError()

        conn = pymongo.MongoClient(self.settings['MONGO_URI'])
        db = conn[self.settings['MONGO_DB_NAME']]

        # Delete collection:
        result = db.drop_collection(args[0])
        print(f"Trying to drop collection '{args[0]}'. Results: \n{result}")
        if result["ok"] == 1.0:
            print(f"Dropped collection '{args[0]}' successfully.")

        conn.close()