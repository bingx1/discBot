import mongoengine
import json

mongoengine.connect(db="items", host="localhost", port=27017)


class Item(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    price = mongoengine.IntField()
    inStock = mongoengine.BooleanField(required=True)
    url = mongoengine.URLField(required=True)
    meta = {'collection': 'rogue'}


'''
Function to put the item at the following url in the database 
'''


def put_item(item_data):
    json = item_data.to_json()
    new_item = Item.from_json(json)
    if not exists(item_data.name):
        new_item.save()
        print("{} succesfully added. Now tracking {}".format(item_data.name, item_data.name))
    else:
        print("Item already exists in the database. {} is already being tracked by the stock bot".format(
            item_data.name))
    return


def exists(item_name):
    for item in Item.objects:
        if item.name == item_name:
            return True
    return False


'''
Function to list all currently tracked items
'''


def list_tracked_items():
    output = ""
    for index, item in enumerate(Item.objects):
        s = '{}. {} \n'.format(index + 1, item.name)
        output += s
        print(s)
    return output


def fetch_items_json():
    return [json.loads(item.to_json()) for item in Item.objects]

def get_items():
    return Item.objects

if __name__ == "__main__":
    mongoengine.connect(db="items", host="localhost", port=27017)
    list_tracked_items()
    x = fetch_items_json()
    print(x)
