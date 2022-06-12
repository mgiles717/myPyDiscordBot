import discord
import json
from discord.ext import commands

# Cogs
from modules import destiny2
from modules import audio
from modules import responses
from modules import gamba
from modules import currency

with open('config.json') as file:
    data = json.load(file)
    token = data.get('token')
    prefix = data.get('prefix')


class Bot:
    def __init__(self):
        cogs = [audio, destiny2, responses, currency, gamba]
        self.client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

        for i in range(len(cogs)):
            cogs[i].setup(self.client)

        print("Bot running")

if __name__ == "__main__":
    discord_bot = Bot()
    discord_bot.client.run(token)
