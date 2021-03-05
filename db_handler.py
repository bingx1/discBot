import mongoengine
import scraper


class Item(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    price = mongoengine.IntField()
    inStock = mongoengine.BooleanField(required=True)
    url = mongoengine.URLField(required=True)
    meta = {'collection': 'rogue'}


'''
Function to put the item at the following url in the database 
'''
def put_item(url):
    item_data = scraper.fetch_item(url)
    json = item_data.to_json()
    new_item = Item(name=json['name'], price=json['price'],
                   inStock=json['inStock'], url=json['url'])
    new_item.save()
    return


'''
Function to list all currently tracked items
'''
def list_tracked_items():
    for index, item in enumerate(Item.objects):
        print('{}. {} - Currently in stock: {}\n'.format(index + 1,item.name, item.inStock))
    return


# def update_items():
    # for item in Item.objects:

if __name__ == "__main__":
    mongoengine.connect(db="items", host="localhost", port=27017)
    for url in scraper.items:
        put_item(url)
    list_tracked_items()