import mongoengine
import json
from connection import Connection


class Item(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    price = mongoengine.IntField()
    inStock = mongoengine.BooleanField(required=True)
    url = mongoengine.URLField(required=True)
    lastStocked = mongoengine.DateTimeField()
    img_url = mongoengine.URLField()
    meta = {'collection': 'rogue'}

    def __str__(self) -> str:
        if self.inStock:
            stock_msg = "# **In stock**"
        else:
            stock_msg = '> Out of stock'
        return "{}\n[${}]({})\n{}\n < Last in stock: {} >\n".format(
            self.name, self.price, self.url, stock_msg, self.lastStocked)


class DbHandler():

    def __init__(self):
        self.db = "items"

    def put_item(self, json_input):
        ''' Puts an item using the json data passed into the database''' 
        new_item = Item.from_json(json_input)
        with Connection():
            if not self.exists(new_item.name):
                new_item.save()
                print("{} succesfully added. Now tracking {}".format(
                    new_item.name, new_item.name))
            else:
                print("Item already exists in the database. {} is already being tracked by the stock bot".format(
                    new_item.name))
        return

    def exists(self, item_name):
        ''' Checks to see whether an item with the same name already exists in the database'''
        for item in Item.objects:
            if item.name == item_name:
                return True
        return False

    def list_tracked_items(self):
        ''' Returns a list of the items currently in the database as strings''' 
        output = ""
        with Connection():
            for index, item in enumerate(Item.objects):
                s = '{}. {} \n'.format(index + 1, item.name)
                output += s
                print(s)
        return output

    def fetch_items_json(self):
        ''' Returns a list of items as python dictionaries'''
        with Connection():
            return [json.loads(item.to_json()) for item in Item.objects]

    def get_items(self):
        ''' Returns a list of all the Item objects in the database'''
        with Connection():
            return Item.objects


if __name__ == "__main__":
    db = DbHandler()
    # db.list_tracked_items()
    x = db.fetch_items_json()
    print(x)
