import json
import discord
import requests
from discord import Game
from discord.ext import commands

BOT = commands.Bot(command_prefix="$$")
with open('config.json') as configfile:
    configdata = json.load(configfile)

@BOT.event
async def on_ready():
    await BOT.change_presence(activity=Game(name="Minecraft"))
    print(f'bot online')

                                 
BOT.run(configdata["bot_token"])
