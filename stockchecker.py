from bs4 import BeautifulSoup
import aiohttp
import asyncio
import db_handler
from discord.ext import commands, tasks
import datetime

class StockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.lock = asyncio.Lock()
        self.monitor_stock.start()

    def cog_unload(self):
        return self.monitor_stock.cancel()

    @tasks.loop(minutes=1.0)
    async def monitor_stock(self):
        async with self.lock:
            items = db_handler.get_items()
            return await asyncio.gather(*(self.fetch_and_parse(item) for item in items))
            # for item in items:
                # await self.fetch_and_parse(item)

    @monitor_stock.after_loop
    async def on_monitor_cancel(self):
        if self.monitor_stock.is_being_cancelled():
            print("Stopping stock monitoring.\n")
            self.session.close()
            print("Closing session.")

    async def fetch(self, url):
        async with self.session.get(url) as response:
            return await response.text()

    def parse(self, html, item):
        soup = BeautifulSoup(html, 'html.parser')
        stock = False
        if soup.find(class_="button btn-size-m red full"):
            stock = True
        if stock != item.inStock:
            print("The stock status of {} has changed!. Updating stock status in DB".format(
                item.name))
            item.inStock = stock
            item.save()
        else:
            print("The stock status of {} has not changed.".format(item.name))

    async def fetch_and_parse(self, item):
        html = await self.fetch(item.url)
        self.parse(html, item)


def setup(bot):
    bot.add_cog(StockCog(bot))
    return
