""" Currency module to hold all methods for handling currency """

import discord
import json
import os

from discord.ext import commands

db_path = os.getcwd() + "\db.json"

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.save_flag = True
        with open(db_path, 'r') as f:
            self.db = json.loads(f.read())
        self.display_users()
        
    """
    Helper functions below, feel free to add more if necessary to perform operations on points, 
    however most functionality should be implace now.
    Due to the need to append to the database, accessing the database directly is needed. e.g
    self.db['users']['the users id here']['points']
    """
    
    def display_users(self):
        print(f"The current users and their respective points: ")
        for i in self.db['users']:
            print(f"ID: {i['id']}, Points: {i['points']}, Daily Counter: {i['daily']}, Items: {i['items']}")
    
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
    
    """ 
    --- Daily Functions ---
    """ 
    
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
        else: 
            await ctx.send("No need to save.")
    
    """
    Currency balancing methods below
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
        await ctx.send(f"You have {self.get_points(ctx)} points.")
    
def setup(client):
    client.add_cog(Currency(client))

if __name__ == "__main__":
    print("Hello, world!")
    Currency()