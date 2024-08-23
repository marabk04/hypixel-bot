import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
import requests
import io
from datetime import datetime, timedelta
import re
import json
from discord.ext import tasks
from database import collection



class StalkingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_channel_task = None
        self.spam_task = None
        self.monitor_message_id = None
        self.HYPIXEL_API_KEY = None
        self.get_hypixel_api_key()


    def get_hypixel_api_key(self):
        hypixel_api_collection = collection["hypixelapi"]
        fixed_id = 206512728993562624
        hypixel_api_doc = hypixel_api_collection.find_one({"id": fixed_id})
        if hypixel_api_doc and "API_KEY" in hypixel_api_doc:
            self.HYPIXEL_API_KEY = hypixel_api_doc["API_KEY"]
            print(self.HYPIXEL_API_KEY)
        else:
            self.HYPIXEL_API_KEY = None

    def get_info(self, url):
        response = requests.get(url)
        return response.json()

    def username_data(self, username):
        mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        uuid_data = self.get_info(mojang_url)
        return uuid_data['id'], uuid_data['name']
    
    def get_player_minecraft_skin(self, uuid):
        skin_url = f"https://starlightskins.lunareclipse.studio/render/ultimate/{uuid}/full"
        return skin_url

    @app_commands.command(name="stalk", description="Start stalking username.")
    async def start_checking(self, interaction: discord.Interaction, username: str):
        self.uuid, self.username = self.username_data(username)
        self.player_skin = self.get_player_minecraft_skin(self.uuid)
        self.channel_id = interaction.channel_id
        self.user_id = interaction.user.id
        self.update_channel_task = self.update_channel.start()
        self.interaction_user = interaction.user.name
        self.interaction_avatar = interaction.user.avatar.url
        self.get_hypixel_api_key()
        await interaction.response.send_message(f"starting key={self.HYPIXEL_API_KEY}", ephemeral=True)
	
        channel = self.bot.get_channel(self.channel_id)
        embed = discord.Embed(title=f"Status: [Beginning to stalk {self.username}]", color=discord.Color.blue())
        embed.set_thumbnail(url=self.player_skin)
        message = await channel.send(embed=embed)
        self.monitor_message_id = message.id


    @app_commands.command(name="stop", description="Stop stalking.")
    async def stop_checking(self, interaction: discord.Interaction):
        self.update_channel_task = self.update_channel.cancel()
        self.spam_task = self.start_spam_loop.cancel()
        await interaction.response.send_message(f"No longer stalking {self.username}.")



    @tasks.loop(minutes=1)
    async def update_channel(self):
        await asyncio.sleep(3)
        channel = self.bot.get_channel(self.channel_id)
        value = await self.check_afk_status()


        
        if value == 1:
            if self.monitor_message_id:
                try:
                    message = await channel.fetch_message(self.monitor_message_id)
                    embed = discord.Embed(title=f"Status: [OFFLINE]", color=discord.Color.blue())
                    embed.add_field(name="Next Update", value=f"{(datetime.now() + timedelta(minutes=1)).strftime('%I:%M %p')}")

                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="Last Update", value=f"{datetime.now().strftime('%I:%M %p')}")
                    embed.set_thumbnail(url=self.player_skin)
                    embed.set_footer(text=f"Stalking {self.username}")
                    await message.edit(embed=embed)
                except discord.NotFound:
                    embed = discord.Embed(title=f"Status: [OFFLINE]", color=discord.Color.blue())
                    embed.add_field(name="Next Update", value=f"{(datetime.now() + timedelta(minutes=1)).strftime('%I:%M %p')}")

                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="\u200b", value="\u200b")
                    embed.add_field(name="Last Update", value=f"{datetime.now().strftime('%I:%M %p')}")
                    embed.set_thumbnail(url=self.player_skin)
                    embed.set_footer(text=f"Stalking {self.username}")
                    message = await channel.send(embed=embed)
                    self.monitor_message_id = message.id
            else:
                embed = discord.Embed(title=f"Status: [OFFLINE]", color=discord.Color.blue())
                embed.add_field(name="Next Update", value=f"{(datetime.now() + timedelta(minutes=1)).strftime('%I:%M %p')}")

                embed.add_field(name="\u200b", value="\u200b")
                embed.add_field(name="\u200b", value="\u200b")
                embed.add_field(name="Last Update", value=f"{datetime.now().strftime('%I:%M %p')}")
                embed.set_thumbnail(url=self.player_skin)
                embed.set_footer(text=f"Stalking {self.username}")
                message = await channel.send(embed=embed)
                self.monitor_message_id = message.id
        else:
            embed = discord.Embed(title=f"Status: [ONLINE]", description=f"Starting to spam tag <@{self.user_id}> ", color=discord.Color.blue())
            embed.set_thumbnail(url=self.player_skin)
            embed.set_footer(text=f"Stalking {self.username}")
            message = await channel.fetch_message(self.monitor_message_id)

            await message.edit(embed=embed)
            self.update_channel.cancel()
            self.spam_task = self.start_spam_loop.start()

    

    async def check_afk_status(self):
        url = f"https://api.hypixel.net/status?key={self.HYPIXEL_API_KEY}&uuid={self.uuid}"
        print(url)
        data = self.get_info(url)
        gameType = data.get("session", {}).get("gameType")
        return 2 if gameType == "SKYBLOCK" else 1



    @tasks.loop(minutes=1)
    async def start_spam_loop(self):
        channel = self.bot.get_channel(self.channel_id)
        spam_message_content = f"<@{self.user_id}> \n Your account is logged on to SkyBlock! Type `/stop` to stop the notifications!"
        for i in range(5):
            await channel.send(content=spam_message_content)
            await channel.send(content="https://tenor.com/view/spongebob-squarepants-spongebob-panic-chaos-fire-gif-4920941")




    def cog_unload(self):
        self.update_channel_task.cancel()
        self.spam_task.cancel()

async def setup(bot):
    await bot.add_cog(StalkingCommand(bot))
