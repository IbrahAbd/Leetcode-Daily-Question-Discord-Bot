from typing import Final
from discord import Intents, Client, Message
from discord.ext import tasks, commands
from dotenv import load_dotenv
import asyncio
import os
import requests
import math
import discord
from questionInfo import *
from datetime import datetime, time

load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

global id

def difficultychecker(difficulty):
    if difficulty == "Hard":
        return 0xff0000  
    elif difficulty == "Medium":
        return 0xFFFF00
    elif difficulty == "Easy":
        return 0x008000
    
async def returnInfo(channel):
    global id 
    try:
        daily_problem = fetch_daily_leetcode_problem()
        today = datetime.now()
        embed = discord.Embed(
            title=f"{today.strftime('%d/%m/%Y')}'s Daily LeetCode Problem",
            color=difficultychecker(daily_problem['difficulty'])
        )
        id = daily_problem['id']

        if daily_problem:
            embed.add_field(name="Problem", value=f"`{daily_problem['title']}`", inline=False)
            embed.add_field(name="Difficulty", value=f"`{daily_problem['difficulty']}`", inline=False)
            embed.add_field(name="Topics", value=f"`{daily_problem['Topics']}`", inline=False)
            embed.add_field(name="Link", value=f"[Click here to solve the problem]({daily_problem['link']})", inline=False)

            description = daily_problem['description']
            if len(description) > 1023:
                description = description[:1000] + "...etc"
            
            embed.add_field(
                name="Description",
                value=f"```python\n{description}\n```",
                inline=False
            )
        else:
            embed.description = "Big yikers! An error has occurred."

        await channel.send(embed=embed)

    except discord.HTTPException as e:
        print(f"HTTP Exception: {e.status} - {e.text}")
    except Exception as e:
        print(f"Unexpected error: {e}")


@tasks.loop(minutes=1)  
async def check_time():
    target_time = time(8, 00)  
    now = datetime.now().time()

    if now.hour == target_time.hour and now.minute == target_time.minute:
        print("ok")
        await send_daily_message()

async def send_daily_message():
    channel = client.get_channel(1276260038754963497) 
    if channel is not None:
        await returnInfo(channel)  
        print("Daily problem message sent to channel!")
    else:
        print("Channel not found!")

@client.event
async def on_ready():
    print(f'{client.user} is now running!')
    check_time.start()

async def main():
    await client.start(TOKEN)

asyncio.run(main())
