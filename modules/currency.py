"""
Currency module for the bot. All currency handling methods are 
to be placed in this module.
"""

import discord
import os
import json
# Creating random numbers using random is only psuedo random, 
# important to note that the random number is not truly random
import random

from discord.ext import commands

# When the bot initalises, it will create a currency object.
# When that object is initialised, os.getcwd() will get the directory of
# the bot.py file, therefore you can use this to access the config file.
db_path = os.getcwd() + "./config/db.json"
items_path = os.getcwd() + "./config/shop.json"

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.seed = random.seed()
        self.save_flag = True
        with open(db_path, 'r') as f:
            self.db = json.loads(f.read())
        with open(items_path, 'r') as f:
            self.shop_items = json.loads(f.read())
            
        print(f"The current users: ")
        for i in self.db['users']:
            print(f"ID: {i['id']}, Points: {i['points']}, Daily counter: {i['daily']}, Items: {i['items']}")
        
    """
    Helper functions below:
    
    Feel free to add more if necessary to perform operations on points, 
    however most functionality should be implace now.
    
    Due to the need to append to the database, accessing the database directly is needed. e.g
    self.db['users']['the users id here']['points']
    """
    
    def fetch_user_index(self, ctx):
        for i, val in enumerate(self.db['users']):
            if val['id'] == ctx.author.id:
                return i
        return False
    
    def get_points(self, ctx):
        return self.db['users'][self.fetch_user_index(ctx)]['points']
    
    # Not enough points flag, used to determine if the user has enough points to perform an action
    def check_points(self, ctx, amount):
        if self.get_points(ctx) >= amount:
            return True
        else: return False
    
    def change_points(self, ctx, amount):
        self.db['users'][self.fetch_user_index(ctx)]['points'] += amount
        self.save_flag = False
        
    def change_daily(self, ctx, reset: bool):
        self.db['users'][self.fetch_user_index(ctx)]['daily'] = int(reset)
        self.save_flag = False
        
    def reset_dailies(self):
        for i in self.db['users']:
            i['daily'] = 0
        self.save_flag = False
    
    @commands.command()
    async def create(self, ctx):
        self.db['users'].append({'id': ctx.author.id, 'points': 0, 'daily': 0, 'items': []})  
        await ctx.send(f"User created!")
    
    @commands.command()
    async def save(self, ctx):
        if self.save_flag == False:
            with open(db_path, 'w') as f:
                f.write(json.dumps(self.db))
                self.save_flag = True
                await ctx.send("Saved!")
    
    """
    Economy balancing methods below:
    """
    
    @commands.command()
    async def daily(self, ctx):
        if self.db['users'][self.fetch_user_index(ctx)]['daily'] == 0:
            self.change_points(ctx, 100)
            self.change_daily(ctx, 1)
            await ctx.send(f"You have received 100 points!")
        else:
            await ctx.send(f"You've already received your daily today.")
        
    @commands.command()
    async def balance(self, ctx):
        await ctx.send(f"You have {self.db['users'][self.fetch_user_index(ctx)]['points']} points.")
    
    """
    Gambling below:
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
    
    """
    Shop below:
    """
    @commands.command()
    async def shopitems(self, ctx):
        items_embed = discord.Embed(title="Shop Items", description="All available items in the shop")
        for i in self.shop_items["items"]:
            items_embed.add_field(name=f'{i["name"]}', value=f'{i["price"]}')
        await ctx.send(embed=items_embed)
    
"""
Leave these alone
"""
       
def setup(client):
    client.add_cog(Currency(client))
    
if __name__ == "__main__":
    with open('C:\ProgrammingProjects\discordpy\db.json', 'r') as f:
        tDatabase = json.loads(f.read())