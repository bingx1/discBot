import requests
from bs4 import BeautifulSoup


items = ["https://www.rogueaustralia.com.au/monster-rhino-belt-squat-stand-alone-mg-black-au",
         'https://www.rogueaustralia.com.au/rogue-tb-2-trap-bar-au',
         'https://www.rogueaustralia.com.au/rogue-mg-3-knurled-multi-grip-bar-au',
         'https://www.rogueaustralia.com.au/earthquake-bar-au',
         'https://www.rogueaustralia.com.au/rogue-ohio-deadlift-bar-black-zinc-au',
         'https://www.rogueaustralia.com.au/black-concept-2-model-d-rower-pm5-au',
         'https://www.rogueaustralia.com.au/rogue-stubby-axle-au']


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
        return {'name': self.name, 'price': self.price, 'inStock': self.in_stock, 'url': self.link}


def fetch_item(link):
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


def print_stock(links):
    """Returns a list of all items and their current stock status in markdown format for printing to discord"""
    body = ''
    for i in range(len(links)):
        item = fetch_item(links[i])
        print(item)
        body += (str(i+1) + ". " + str(item))
    output = "```md\n{}```".format(body)
    return output


if __name__ == "__main__":
    print_stock(items)
