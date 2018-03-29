import json, difflib

import requests
from discord import Embed
from discord.utils import oauth_url
from discord.ext import commands

import helpers

bot = commands.Bot(command_prefix="/")
names = [x.get("name").lower() for x in requests.post("https://www.khuxbot.com/api/v2/get",
                      data=json.dumps({"filter":{"rarity":6},"format":["name"]}),
                      headers={"Content-Type":"application/json"}).json()]
# Very ugly, all it does is retrieves the names of all medals from the server (Run this on bot start for performance reasons
config = json.load(open("config.json", "r"))

@bot.command()
async def get(*args):
    medal_data = get_medal(args)
    if not medal_data.get("error"): # No errors here
        url = "https://www.khuxbot.com"+medal_data.get("image_link")
        embed = create_embed(medal_data, url)
        await bot.say("", embed=embed)
    else:
        await bot.say("Could not find medal **{}**\nDid you mean:\n{}".format(" ".join(args), "\n".join(medal_data.get("error"))))

def get_suggested_names(failed_name):
    return difflib.get_close_matches(failed_name.lower(), names, cutoff=config.get("medal_similarity_score"))

def create_embed(medal_data, url):
    embed = Embed(colour=helpers.map_element_to_colour(medal_data.get("element")))
    embed.add_field(name=medal_data.get("name"), value=medal_data.get("notes"), inline=False)
    emojis = {x.name: x for x in bot.get_all_emojis()}
    embed.set_image(url=url)
    embed.add_field(name=medal_data.get("element") + str(emojis.get(medal_data.get("element"))),
                    value=medal_data.get("direction"), inline=False)
    embed.add_field(name="", value="", inline=True)
    return embed


def get_medal(name):
    name = " ".join(name)
    url = "https://www.khuxbot.com/api/v2/get"
    data = json.dumps({"filter":{"name": name, "rarity":6}})
    data = requests.post(url, data=data,headers={"Content-Type":"application/json"}).json()
    if isinstance(data, list):
        return data[0]
    else:
        return {"error":get_suggested_names(name)}



if __name__ == "__main__":
    print("Use the following url to connect the bot to your server:")
    print(oauth_url(config.get("client_id")))
    bot.run(config.get("token_secret"))