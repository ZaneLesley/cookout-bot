import discord
from discord import Intents, Client, Message, TextChannel
import json
from main import update_point_message


async def change_points(user: str, react_user: str, bot, value: int, react_value: int):
    data = {}
    try:
        with open ("points.json", "r") as file:
            data = json.load(file)
    except Exception as e:
        print(e)

    print(react_user, flush=True)
    
    if user in data:
        data[user]["points"] += value

    if react_user in data:
        print("hit")
        data[react_user]["points"] += react_value

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