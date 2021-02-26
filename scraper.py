import requests
from bs4 import BeautifulSoup

items = ["https://www.rogueaustralia.com.au/monster-rhino-belt-squat-stand-alone-mg-black-au",
         'https://www.rogueaustralia.com.au/the-ohio-bar-black-zinc-au',
         'https://www.rogueaustralia.com.au/rogue-tb-2-trap-bar-au',
         'https://www.rogueaustralia.com.au/rogue-mg-3-knurled-multi-grip-bar-au',
         'https://www.rogueaustralia.com.au/earthquake-bar-au',
         'https://www.rogueaustralia.com.au/rogue-ohio-deadlift-bar-black-zinc-au',
         'https://www.rogueaustralia.com.au/rogue-stubby-axle-au']

class Item:
    def __init__(self, name, price, inStock, link, itemNo):
        self.name = name
        self.price = price
        self.inStock = inStock
        self.link = link
        self.itemNo = itemNo
    
    def __str__(self):
        if self.inStock:
            stock_msg = "# **In stock**"
        else:
            stock_msg = '> Out of stock'
        output = "\n{}. {}\n[${}]({})\n{}\n".format(self.itemNo, self.name, self.price, self.link, stock_msg)
        return output


def scrape_item(link, itemNo):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    inStock = False

    if soup.find(class_="button btn-size-m red full"):
        inStock = True
    price = soup.find(class_="main-price").contents[0]
    name = soup.find(class_='name').contents[0]
    # print(name, price, inStock, link)
    return Item(name, price, inStock, link, itemNo)


def print_stock(links):
    body = ''
    for i in range(len(links)):
        item = scrape_item(links[i], i + 1)
        print(item)
        body += str(item)
    output = "```md\n{}```".format(body)
    print(output)
    return output
