"""
Gambling module for the bot. 
Note to future self, refactor the database aspect of this module to another module.
"""

import discord
# Creating random numbers using random is only psuedo random, 
# important to note that the random number is not truly random
import random
import json
import os
from modules.currency import Currency
from discord.ext import commands


class Gamba(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.seed = random.seed()
        # Currently creates 2 currency objects, 
        # however need access to the currency object in bot.py
        self.currency = Currency(client)
    """
    Gambling games below
    """
    
    @commands.command()
    async def HorL(self, ctx, bet: int, arg):
        if not self.check_points(ctx, bet):
            await ctx.send(f"You do not have enough points for this bet, current balance: {self.get_points(ctx)}")
            return
        roll = random.randint(0, 100)
        if roll>50:
            if arg == 'h':
                self.change_points(ctx, bet)
                await ctx.send(f"You have won {bet} points! The roll was {roll}.")
            else:
                self.change_points(ctx, -bet)
                await ctx.send(f"You have lost {bet} points! The roll was {roll}.")
        if roll<=50:
            if arg == 'l':
                self.change_points(ctx, bet)
                await ctx.send(f"You have won {bet} points! The roll was {roll}.")
            else:
                self.change_points(ctx, -bet)
                await ctx.send(f"You have lost {bet} points! The roll was {roll}.")
    
    @commands.command()
    async def guessnumber(self, ctx, bet: int, arg: int):
        if not self.check_points(ctx, bet):
            await ctx.send(f"You do not have enough points for this bet, current balance: {self.get_points(ctx)}")
            return
        roll = random.randint(0,100)
        diff = abs(roll-arg)
        if diff == 0:
            self.change_points(ctx, bet*10)
            await ctx.send(f"The roll was {roll}. You have won {bet*10} points!")
        elif diff <= 5:
            self.change_points(ctx, bet*4)
            await ctx.send(f"The roll was {roll}. You have won {bet*4} points!")
        elif diff <= 10:
            self.change_points(ctx, bet*2)
            await ctx.send(f"The roll was {roll}. You have won {bet*2} points!")
        elif diff <= 30:
            await ctx.send(f"The roll was {roll}. You have not won or lost any points!")
        else: 
            self.change_points(ctx, -bet)
            await ctx.send(f"The roll was {roll}. You have lost {bet} points!")
        
def setup(client):
    client.add_cog(Gamba(client))
    
if __name__ == "__main__":
    g = Gamba()
    print(g.currency)