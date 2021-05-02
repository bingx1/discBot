import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
# Set-up intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Load environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Set-up bot and load cogs
bot = commands.Bot(command_prefix='!',intents=intents)
bot.load_extension("cogs.main_cog")
bot.load_extension("cogs.stockchecker")
bot.load_extension("cogs.web_cog")

if __name__ == "__main__":
    bot.run(TOKEN)
