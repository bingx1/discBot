from bs4 import BeautifulSoup
import aiohttp
from discord.ext import commands, tasks
import discord
import json


class WebCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.Cog.listener()
    async def on_ready(self):
        print('WebCog is now ready!')
        print('Initializing aiohttp session - requests are now ready')
        self.server = self.bot.guilds[0]
        self.channel = discord.utils.get(
            self.server.channels, name='bot-notifications')

    async def fetch(self, url: str):
        ''' Performs a get request to the passed URL and returns the html '''
        async with self.session.get(url) as response:
            return await response.text()

    async def fetch_item_data(self, url: str) -> str:
        ''' Takes a URL of an item and returns a json payload containing the items data'''
        page = await self.fetch(url)
        soup = BeautifulSoup(page, 'html.parser')
        in_stock = False
        if soup.find(class_="button btn-size-m red full"):
            in_stock = True
        price = extract_price(soup.find(class_="main-price").contents[0])
        name = soup.find(class_='name').contents[0]
        thumbnail = get_thumbnail(soup)
        result = {'name': name, 'price': price,
                  'inStock': in_stock, 'url': url, 'img_url': thumbnail}
        return to_json(result)

    async def close_session(self):
        ''' Closes the aiohttp client session '''
        self.session.close()

    def get_session(self):
        return self.session

def setup(bot):
    bot.add_cog(WebCog(bot))
    return


def to_json(dic: dict) -> str:
    ''' Converts a dictionary into a JSON string '''
    return json.dumps(dic)


def extract_price(price_string: str) -> int:
    """Helper function to convert a string in the form 'A$1,595.00' to an integer 1595"""
    return int(price_string.split('.')[0].replace(',', '')[2:])


def get_thumbnail(soup: BeautifulSoup) -> str: 
    '''Helper function to retrieve the url location of the items thumbnail from html'''
    imgs = soup.find(class_="custom-scroll product-scroll")
    return imgs.find(class_="image aspect-169 active i-c").findChild("img")['src']
