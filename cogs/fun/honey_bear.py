import settings
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from datetime import datetime




channel = 1155374503564677204
class honey_bear(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.voice_client = None
        self.loop_task = None
        super().__init__()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel_id = 1155374503564677204

        if after.channel and after.channel.id == channel_id:
            self.voice_channel = after.channel

            if self.voice_client and self.voice_client.is_connected():
                if self.voice_client.channel == self.voice_channel:
                    return  

            if not self.loop_task:
                self.loop_task = asyncio.create_task(self.loop())



        if before.channel and before.channel.guild.voice_client:
            await before.channel.guild.voice_client.disconnect()

            if self.loop_task:
                self.loop_task.cancel()
                self.loop_task = None

    async def loop(self):
        self.voice_client = await self.voice_channel.connect()
        while True:
            audio_source = discord.FFmpegPCMAudio("honeybear.mp3")
            self.voice_client.play(audio_source, after=lambda e: None)
            await asyncio.sleep(90)


    

async def setup(bot):
    await bot.add_cog(honey_bear(bot))