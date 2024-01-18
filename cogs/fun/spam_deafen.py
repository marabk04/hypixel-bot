import settings
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from datetime import datetime



CHANNELS = []
USERS = []
class spam_deafen(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()



    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member in USERS and after.self_deaf:
            guild_id = member.guild.id
            channel_id = self.get_spam_channel(guild_id)
            if channel_id:
                channel = member.guild.get_channel(channel_id)
                if before.self_deaf is False and after.self_deaf is True:
                    try:
                        while member.voice.self_deaf is True:
                            await channel.send(f"{member.mention} is deafened, come back RIGHT NOW!")
                    except:
                        pass

    @app_commands.checks.has_permissions(ban_members = True )
    @app_commands.command(
        name = "spam",
        description= "Spams a speificed defeaned user" )
    async def spam_set(self, interaction: discord.Interaction, member: discord.Member):
        USERS.append(member)
        await interaction.response.send_message(f"Added {member}")


    @app_commands.checks.has_permissions(ban_members = True )
    @app_commands.command(
        name = "spam_channel",
        description= "Sets the channel per guild when the user is spammed" )
    async def spam_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        
        CHANNELS.append(channel.id)

        await interaction.response.send_message(f"Added {channel}")

    def get_spam_channel(self, guild_id):
        for channel_id in CHANNELS:
            if guild_id == self.bot.get_channel(channel_id).guild.id:
                return channel_id
        return None
    
    

async def setup(bot):
    await bot.add_cog(spam_deafen(bot))