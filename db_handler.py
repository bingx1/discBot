import mongoengine

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
    if not exists(item_json=json):
        new_item = Item(name=json['name'], price=json['price'],
                    inStock=json['inStock'], url=json['url'])
        new_item.save()
    return


def exists(item_json):
    for item in Item.objects:
        if item.name == item_json['name']:
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


# def update_items():
    # for item in Item.objects:

if __name__ == "__main__":
    mongoengine.connect(db="items", host="localhost", port=27017)
    list_tracked_items()
