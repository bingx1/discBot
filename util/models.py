import mongoengine

class Item(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    price = mongoengine.IntField()
    inStock = mongoengine.BooleanField(required=True)
    url = mongoengine.URLField(required=True)
    lastStocked = mongoengine.DateTimeField()
    img_url = mongoengine.URLField(required=True)
    meta = {'collection': 'rogue'}

    def __str__(self) -> str:
        if self.inStock:
            stock_msg = "# **In stock**"
        else:
            stock_msg = '> Out of stock'
        return "{}\n[${}]({})\n{}\n < Last in stock: {} >\n".format(
            self.name, self.price, self.url, stock_msg, self.lastStocked)

class Change(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    restock = mongoengine.URLField(required=True)
    other = mongoengine.BooleanField()