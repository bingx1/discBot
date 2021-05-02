from bs4 import BeautifulSoup
import asyncio
from util.db_handler import DbHandler 
from util.models import Item
from discord.ext import commands, tasks
import datetime
import discord


class StockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self.lock = asyncio.Lock()
        self.channel = None
        self.db_handler = DbHandler()

    def cog_unload(self):
        return self.monitor_stock.cancel()

    async def notify(self, msg: str):
        ''' Sends a message [msg] to the discord channel'''
        print(msg)
        await self.channel.send(msg)

    @commands.Cog.listener()
    async def on_ready(self):
        print('StockCog is now ready!')
        server = self.bot.guilds[0]
        self.channel = discord.utils.get(
            server.channels, name='bot-notifications')
        self.monitor_stock.start()

    @tasks.loop(minutes=1.0)
    async def monitor_stock(self):
        ''' Refreshes the status of all items every minute '''
        async with self.lock:
            items = self.db_handler.get_items()
            time = datetime.datetime.now()
            time_formatted = time.strftime(r"%A, %b %d %I:%M%p")
            msg = "```asciidoc\n{} :: Updating the status of tracked items```".format(
                time_formatted)
            await self.notify(msg)
            return await asyncio.gather(*(self.fetch_and_parse(item) for item in items))

    @monitor_stock.after_loop
    async def on_monitor_cancel(self):
        ''' Closes the aiohttp connection '''
        if self.monitor_stock.is_being_cancelled():
            print("\nStopping stock monitoring.")
            await self.session.close()
            print("Closing session.")

    async def parse(self, html: str, item: Item) -> None:
        '''Function to process the html and update the matching item in the DB accordingly '''
        soup = BeautifulSoup(html, 'html.parser')
        stock = False
        if soup.find(class_="button btn-size-m red full"):
            stock = True
            item.lastStocked = datetime.datetime.now()
        if stock != item.inStock:
            msg = "{} is now back in stock!".format(
                item.name)
            item.inStock = stock
            await self.notify(msg)
            await self.announce_restock(item)
        else:
            msg = "The stock status of {} has not changed.".format(item.name)
            print(msg)
        item.save()

    async def fetch_and_parse(self, item):
        ''' Calls the webCog to perform a GET request for the item and processes the payload '''
        webCog = self.bot.get_cog('WebCog')
        if not self.session:
            self.session = webCog.get_session()
        html = await webCog.fetch(item.url)
        await self.parse(html, item)

    async def announce_restock(self, item):
        ''' Sends an embed to the bot-notifications channel containing a description of the restocked item and a link to purchase '''
        embed = discord.Embed(title=item.name, url=item.url,
                              color=discord.Color.green())
        embed.set_thumbnail(url= item.img_url)
        embed.set_author(name="StockBot")
        embed.description = "{} is now back in stock! Visit the link to purchase.".format(
            item.name)
        embed.add_field(name="Price", value="A${}".format(
            item.price), inline=False)
        await self.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(StockCog(bot))
    return
