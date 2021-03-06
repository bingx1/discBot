from bs4 import BeautifulSoup
import aiohttp
import asyncio
from db_handler import DbHandler
from discord.ext import commands, tasks
import datetime
import discord


class StockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.lock = asyncio.Lock()
        self.channel = None
        self.db_handler = DbHandler()

    def cog_unload(self):
        return self.monitor_stock.cancel()

    async def notify(self, msg):
        print(msg)
        await self.channel.send(msg)

    @commands.Cog.listener()
    async def on_ready(self):
        print('StockCog is now ready!')
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)
        print('Active in the following guilds: ', self.bot.guilds)
        server = self.bot.guilds[0]
        self.channel = discord.utils.get(server.channels, name='bot-notifications')
        self.monitor_stock.start()

    @tasks.loop(minutes=1.0)
    async def monitor_stock(self):
        async with self.lock:
            items = self.db_handler.get_items()
            time = datetime.datetime.now()
            time_formatted = time.strftime(r"%A, %d-%b %I:%M%p")
            msg = "{} : Currently refreshing the status of tracked items.".format(
                time_formatted)
            await self.notify(msg)
            return await asyncio.gather(*(self.fetch_and_parse(item) for item in items))

    @monitor_stock.after_loop
    async def on_monitor_cancel(self):
        if self.monitor_stock.is_being_cancelled():
            print("\nStopping stock monitoring.")
            await self.session.close()
            print("Closing session.")

    async def fetch(self, url):
        async with self.session.get(url) as response:
            return await response.text()

    async def parse(self, html, item):
        soup = BeautifulSoup(html, 'html.parser')
        stock = False
        if soup.find(class_="button btn-size-m red full"):
            stock = True
        if stock != item.inStock:
            msg = "The stock status of {} has changed!".format(
                item.name)
            item.inStock = stock
            item.save()
            await self.notify(msg)
            await self.announce_restock(item)
        else:
            msg = "The stock status of {} has not changed.".format(item.name)
            print(msg)


    async def fetch_and_parse(self, item):
        html = await self.fetch(item.url)
        await self.parse(html, item)

    async def announce_restock(self, item):
        embed = discord.Embed(title = item.name, url = item.url, color=discord.Color.green())
        embed.set_thumbnail(url = await self.get_thumbnail(item))
        embed.set_author(name="StockBot")
        embed.description = "{} is now back in stock! Visit the link to purchase.".format(item.name)
        embed.add_field(name="Price", value="A${}".format(item.price), inline=False)
        await self.channel.send(embed = embed)

    async def get_thumbnail(self, item):
        html = await self.fetch(item.url)
        soup = BeautifulSoup(html, 'html.parser')
        imgs = soup.find(class_="custom-scroll product-scroll")
        return imgs.find(class_="image aspect-169 active i-c").findChild("img")['src']

def setup(bot):
    bot.add_cog(StockCog(bot))
    return
