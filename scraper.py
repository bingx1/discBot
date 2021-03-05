import requests
from bs4 import BeautifulSoup
import aiohttp
import db_handler
from discord.ext import commands
import json

class ItemData:
    def __init__(self, name, price, inStock, link):
        self.name = name
        self.price = price
        self.inStock = inStock
        self.link = link

    def __str__(self):
        if self.inStock:
            stock_msg = "# **In stock**"
        else:
            stock_msg = '> Out of stock'
        output = "{}\n[${}]({})\n{}\n".format(
            self.name, self.price, self.link, stock_msg)
        return output

    def to_json(self):
        return json.dumps({'name': self.name, 'price': self.price, 'inStock': self.inStock, 'url': self.link})


class ScraperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(name='stock', help='Fetches the current status of stocked items')
    async def get_items(self, ctx):
        await ctx.send(print_stock())

    @commands.command(name='list')
    async def list_items(self, ctx):
        tracked_items = db_handler.list_tracked_items()
        tracked_items = "Currently tracking the following items: \n" + tracked_items
        print(tracked_items)
        await ctx.send(tracked_items)    

def setup(bot):
    bot.add_cog(ScraperCog(bot))
    return


def fetch_new_item(link):
    """Takes a valid URL, scrapes it and returns the items data - name, price, and current stock status"""
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    in_stock = False
    if soup.find(class_="button btn-size-m red full"):
        in_stock = True
    price = extract_price(soup.find(class_="main-price").contents[0])
    name = soup.find(class_='name').contents[0]
    return ItemData(name, price, in_stock, link)


def extract_price(price_string):
    """Converts a string in the form 'A$1,595.00' to an integer 1595"""
    return int(price_string.split('.')[0].replace(',', '')[2:])


def get_stock_status(link):
    """Checks whether the item at the given URL is in stock"""
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    if soup.find(class_="button btn-size-m red full"):
        return True
    else:
        return False


def print_stock():
    """Returns a list of all items and their current stock status in markdown format for printing to discord"""
    body = ''
    items = db_handler.fetch_items_json()
    for i, item in enumerate(items):
        item_data = ItemData(item['name'],item['price'],item['inStock'],item['url'])
        print(item_data)
        body += ('\n' + str(i+1) + ". " + str(item_data))
    output = "```md\n{}```".format(body)
    return output


if __name__ == "__main__":
    out = print_stock()
    print(out)
