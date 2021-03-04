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
    itemData = scraper.scrape_item(url)
    newItem = Item(name=itemData['name'], price=itemData['price'],
                   inStock=itemData['inStock'], url=itemData['url'])
    newItem.save()
    return


'''
Function to list all currently tracked items
'''
def list_tracked_items():
    for index, item in enumerate(Item.objects):
        print('{}. {} - Currently in stock: {}\n'.format(index + 1,item.name, item.inStock))
    return

if __name__ == "__main__":
    mongoengine.connect(db="items", host="localhost", port=27017)
    list_tracked_items()