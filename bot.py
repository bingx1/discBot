import discord
import os
import random
import scraper

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.presences = True 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('SERVER')
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    server = discord.utils.get(client.guilds, name=SERVER)
    print(
        f'{client.user} is connected to the following server:\n'
        f'{server.name}(id: {server.id})\n'
    )
    members = '\n - '.join([member.name for member in server.members])
    print(f'Server Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!stock':
        await message.channel.send(scraper.print_stock(scraper.items))
        

@client.event
async def on_voice_state_update(member, before, after):
    server = discord.utils.get(client.guilds, name=SERVER)
    channel = discord.utils.get(server.channels, name='general')
    if after.self_stream:
        print("{} is now streaming on {}".format(member.name, after.channel.name))
        await channel.send("{} is now streaming   :100: ! \nHop on {} to watch them :eyes: :eyes:".format(member.name, after.channel.name))

# @client.event
# async def on_member_uldate(before, after):
if __name__ == "__main__":
    client.run(TOKEN)