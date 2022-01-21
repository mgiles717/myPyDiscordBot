import discord
from discord.ext import commands


class Responses(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello <@{ctx.author.id}>")


def setup(client):
    client.add_cog(Responses(client))
