import json
from discord.ext import commands


class ValorantHandler:
    def __init__(self):
        # Path to config file
        path = "C:/ProgrammingProjects/Repositories/myPyDiscordBot/api_keys.json"
        with open(path) as file:
            data = json.load(file)
            self.key = data.get('valorant_api_key')

if __name__ == "__main__":
    print(ValorantHandler().key)