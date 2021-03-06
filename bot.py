import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Set-up intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set-up bot and load cogs
bot = commands.Bot(command_prefix='!',intents=intents)
bot.load_extension("main_cog")
bot.load_extension("stockchecker")
bot.load_extension("web_cog")

if __name__ == "__main__":
    bot.run(TOKEN)
