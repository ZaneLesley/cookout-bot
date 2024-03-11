import discord
from discord import Intents, Client, Message, TextChannel
import json
from main import update_point_message


async def add_points(user: str, bot):
    data = {}
    try:
        with open ("points.json", "r") as file:
            data = json.load(file)
    except Exception as e:
        print(e)

    if user in data:
        data[user]["points"] += 5

    with open("points.json", "w") as file:
        json.dump(data, file, indent=4)
    
    await update_point_message(bot)

async def remove_points(user: str, bot):
    data = {}
    try:
        with open ("points.json", "r") as file:
            data = json.load(file)
    except Exception as e:
        print(e)

    if user in data:
        data[user]["points"] -= 5

    with open("points.json", "w") as file:
        json.dump(data, file, indent=4)

    await update_point_message(bot)

async def json_init(user: discord.Member, bot):
    data = {}
    try:
        with open("points.json", "r") as file:
            data = json.load(file)
    except Exception as e:
        print(e)
    
    if str(user.name) not in data:
        data[str(user.name)] = {
            "id": user.id,
            "points": 0
            }
        
        with open("points.json", "w") as file:
            json.dump(data, file, indent=4)
    
    await update_point_message(bot)