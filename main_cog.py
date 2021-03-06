import requests
from bs4 import BeautifulSoup
from db_handler import DbHandler
from discord.ext import commands
import json
import aiohttp
import re


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self.db_handler = DbHandler()

    @commands.Cog.listener()
    async def on_ready(self):
        print('MainCog is now ready!')
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)
        print('Active in the following guilds: ', self.bot.guilds)

    @commands.command(name='stock', help='Fetches the current status of stocked items')
    async def get_items(self, ctx):
        await ctx.send(self.format_items())

    @commands.command(name='list')
    async def list_items(self, ctx):
        tracked_items = self.db_handler.list_tracked_items()
        tracked_items = "Currently tracking the following items: \n" + tracked_items
        print(tracked_items)
        await ctx.send(tracked_items)

    @commands.command(name='add')
    async def add_items(self, ctx, *args):
        web_cog = self.bot.get_cog("WebCog")
        for arg in args:
            if is_valid_url(arg):
                json = await web_cog.fetch_item_data(arg)
                self.db_handler.put_item(json)
            else:
                print("URL provided is invalid")

    def format_items(self):
        ''' Returns a list of the items in the database with markdown formatting for printing in discord'''
        body = ''
        items = self.db_handler.get_items()
        for i, item in enumerate(items):
            print(item)
            body += ('\n' + str(i+1) + ". " + str(item))
        output = "```md\n{}```".format(body)
        return output


def setup(bot):
    bot.add_cog(MainCog(bot))
    return


def is_valid_url(url):
    pattern = re.compile(
        r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&=]*)")
    return re.match(pattern, url)


# if __name__ == "__main__":

    # print(out)
