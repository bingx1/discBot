import mongoengine
import json
from connection import Connection


class Item(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    price = mongoengine.IntField()
    inStock = mongoengine.BooleanField(required=True)
    url = mongoengine.URLField(required=True)
    meta = {'collection': 'rogue'}


class DbHandler():

    def __init__(self):
        self.db = "items"

    def put_item(self, item_data):
        json = item_data.to_json()
        new_item = Item.from_json(json)
        with Connection():
            if not self.exists(item_data.name):
                new_item.save()
                print("{} succesfully added. Now tracking {}".format(
                    item_data.name, item_data.name))
            else:
                print("Item already exists in the database. {} is already being tracked by the stock bot".format(
                    item_data.name))
        return

    def exists(self, item_name):
        for item in Item.objects:
            if item.name == item_name:
                return True
        return False

    def list_tracked_items(self):
        output = ""
        with Connection():
            for index, item in enumerate(Item.objects):
                s = '{}. {} \n'.format(index + 1, item.name)
                output += s
                print(s)
        return output

    def fetch_items_json(self):
        with Connection():
            return [json.loads(item.to_json()) for item in Item.objects]

    def get_items(self):
        with Connection():
            return Item.objects


if __name__ == "__main__":
    db = DbHandler()
    # db.list_tracked_items()
    x = db.fetch_items_json()
    print(x)
