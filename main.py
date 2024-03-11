from typing import Final
import os
import discord 
from dotenv import load_dotenv
from discord import Intents, Client, Message, TextChannel, app_commands, utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from responses import get_response
import points
import json

SERVER_ID = 1155965000255545384

#Load Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
activity = discord.Activity(type= discord.ActivityType.listening, name= "The Cookout. z!")
bot = commands.Bot(command_prefix="!", 
                    intents= discord.Intents.all(),
                    activity=activity)

@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is now running!", flush=True)
    
    try: 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)", flush=True)
    except Exception as e:
        print(e)

    channel_name = 'tribunal'
    channel = discord.utils.get(bot.get_all_channels(), name=channel_name)

    with open("last_message.txt", 'r') as file:
        last_id = int(file.read().strip())

        messages = await fetch_messages_after_id(channel, last_id)
        for message in messages:
           await tribunal(message)
           await points.update_point_message(message)

@bot.event
async def on_message(message: Message) -> None:
    #Message isnt from bot
    if message.author == bot.user:
        return 
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    
    print(f"[{channel} {username} '{user_message}']", flush=True)
    
    if(message.channel.name == 'tribunal'):
        await tribunal(message)

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    channel_id = payload.channel_id
    user = payload.user_id
    emoji = payload.emoji
    channel = bot.get_channel(1213003210416062484)
    message = await channel.fetch_message(message_id)
    username = message.author.name

    if (user == 767548847219408927) or (user == message.author.id):
        return

    if(channel_id == 1213003210416062484):          #ID for Tribunal
        if(str(emoji) == '\u2705'):
            await points.add_points(username, bot)
        
        if(str(emoji) == '\u274c'):
            await points.remove_points(username, bot)

@bot.tree.command(name="adduser", description="adds a user to the json")
@has_permissions(administrator=True)
async def adduser(interaction: discord.Interaction, user: discord.Member):
    await points.json_init(user=user, bot=bot)
    await interaction.response.send_message(f"user <@{user.id}> was added to json.")

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    channel_id = payload.channel_id
    user = payload.user_id
    emoji = payload.emoji
    channel = bot.get_channel(1213003210416062484)
    message = await channel.fetch_message(message_id)
    username = message.author.name
    
    if (user == 767548847219408927) or (user == message.author.id):
        return

    if(channel_id == 1213003210416062484):          #ID for Tribunal
        if(str(emoji) == '\u2705'):
            await points.remove_points(username, bot)
        
        if(str(emoji) == '\u274c'):
            await points.add_points(username, bot)

async def update_point_message(bot):
    channel = bot.get_channel(1215666835647631441)           #id for bank
    to_edit = await channel.fetch_message(1215669654048210974)
    data = {}
    message_lines = []
    with open("points.json", "r") as file:
        data = json.load(file)

    message_lines.append("# Bank:")
    message_lines.append("-------------------------")
    for user in data:   
        message_lines.append(f"{user}'s cash: {data[user]['points']}\n")
    
    message = "\n".join(message_lines)

    await to_edit.edit(content=message)

async def tribunal(message: Message):
    checkmark = '✅'
    x_mark =  '❌'
    
    with open("last_message.txt", 'w') as file:
        file.write(str(message.id))
    
    await message.add_reaction(checkmark)
    await message.add_reaction(x_mark)

async def fetch_messages_after_id(channel: TextChannel, last_id: int):
    last_message = await channel.fetch_message(last_id)

    messages = []
    async for message in channel.history(limit = None, after=last_message):
        messages.append(message)

    return messages

def main():
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()