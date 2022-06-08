import json
import requests
import discord
from discord.ext import commands


class Destiny2Handler(commands.Cog):
    def __init__(self, client=None):
        self.client = client
        #! DELETE WHEN SOLVED
        self.item = {}
        # Path to config file
        path = "C:/ProgrammingProjects/discordpy/api_keys.json"
        with open(path) as file:
            data = json.load(file)
            self.key = data.get('destiny_2_api_key')

        oauth_session = requests.Session()
        oauth_session.headers["X-API-Key"] = self.key

    def get_item(self, item):
        import fuzzywuzzy.fuzz as fuzz
        max_ratio = 0
        response = requests.get(
            f"https://www.bungie.net/Platform/Destiny2/Armory/Search/DestinyInventoryItemDefinition/{item.lower()}/",
            headers={"X-API-KEY": self.key})
        if not response.json()['Response']['suggestedWords']:
            return False
        elif not response.json()['Response']['results']['results']:
            self.get_item(response.json()['Response']['suggestedWords'][0])
        else:
            for i in response.json()['Response']['results']['results']:
                ratio = fuzz.ratio(item, i)
                if ratio > max_ratio:
                    query = i
                    max_ratio = ratio
            item_id = query['hash']

            # change item id from id to {item_id} when fixed
            # item = Gjallarhorn
            r = requests.get(f"https://www.bungie.net/platform/Destiny2/Manifest/DestinyInventoryItemDefinition/{item_id}/",
                             headers={"X-API-KEY": self.key})
            inventory_item = r.json()

            # Uncomment to show all properties displayed for the item
            # Useful for adding fields
            # print("inventory", inventory_item)
            item_vals = {"name": inventory_item['Response']['displayProperties']['name'],
                         "desc": inventory_item['Response']['flavorText'],
                         "icon": "https://www.bungie.net" + inventory_item['Response']['displayProperties']['icon'],
                         "tierTypeName": inventory_item['Response']['inventory']['tierTypeName'],
                         "itemTypeName": inventory_item['Response']['itemTypeDisplayName'],
                         "itemHash": item_id
                         }
            # Print statement shows all
            # print("get_item vals", item_vals)
            #! DELETE BELOW WHEN SOLVED
            self.item = item_vals
            # return item_vals

    def embed_d2item(self, item):
        if not item:
            return False
        else:
            try:
                #* WORKING BELOW
                self.get_item(item)
                info_dict = self.item
                if not info_dict:
                    return False
                else:
                    embed = discord.Embed(title=info_dict.get('name'), description=info_dict.get('desc'),
                                          url=f"https://www.light.gg/db/items/{info_dict.get('itemHash')}")
                    embed.add_field(name='Tier', value=info_dict.get('tierTypeName'))
                    embed.add_field(name='Item Type', value=info_dict.get('itemTypeName'))
                    embed.set_image(url=info_dict.get('icon'))
                    return embed
            except:
                print(f"INCORRECT ITEM NAME {item}")
                return False

    def get_user_id(self, user):
        r = requests.get(f"https://www.bungie.net/Platform/User/Search/Prefix/{user}/0/",
                         headers={"X-API-KEY": self.key})
        user_id = r.json()['Response']['searchResults'][0]['bungieNetMembershipId']
        return user_id

    def get_user(self, user):
        user_id = Destiny2Handler().get_user_id(user)
        print(user_id)
        r = requests.get(f"https://www.bungie.net/Platform/Destiny2/254/Profile/{user_id}/?components=Profiles",
                         headers={"X-API-KEY": self.key})
        print(r.json())

    @commands.command()
    async def d2item(self, ctx, item: str = None):
        if item is None:
            await ctx.send("No item inputted")
        else:
            content = Destiny2Handler().embed_d2item(item)
            if content is False:
                await ctx.send("Your item does not exist")
            else:
                await ctx.send(embed=Destiny2Handler().embed_d2item(item))


def setup(client):
    client.add_cog(Destiny2Handler(client))

if __name__ == "__main__":
    test = Destiny2Handler()
    print("test", test.embed_d2item("Gjallahorn"))
