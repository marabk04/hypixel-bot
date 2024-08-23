import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from datetime import datetime


class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = {}  # Initialize settings within the cog
    
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(
        name="logs",
        description="set mod channel"
    )
    async def set_mod_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.settings[interaction.guild_id] = channel.id
        await interaction.response.send_message(f'Moderation channel set to {channel.mention}')


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild:
            return
        mod_channel_id = self.settings.get(message.guild.id) 
        if mod_channel_id:
            mod_channel = self.bot.get_channel(mod_channel_id) 
            if mod_channel:
                embed = discord.Embed(title="Deleted Message", description=message.content, color=discord.Color.purple())
                await mod_channel.send(embed=embed)
            else:
                pass
        else:
            pass


    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if not message_before.guild:
            return
        
        mod_channel_id = self.settings.get(message_before.guild.id)  
        if mod_channel_id:
            mod_channel = self.bot.get_channel(mod_channel_id) 
            if mod_channel:
                embed = discord.Embed(title="Deleted Message", description=f"{message_after.content} and f{message_before}", color=discord.Color.purple())
                await mod_channel.send(embed=embed)
            else:
                pass
        else:
            pass


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.guild:
            return
        mod_channel_id = self.settings.get(member.guild.id) 
        if mod_channel_id:
            mod_channel = self.bot.get_channel(mod_channel_id)
            if mod_channel:
                embed = discord.Embed(title="Deleted Message", description=f"{member} and", color=discord.Color.purple())
                await mod_channel.send(embed=embed)
            else:
                pass
        else:
            pass


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.guild:
            return
        mod_channel_id = self.settings.get(member.guild.id)  # Use self.settings
        if mod_channel_id:
            mod_channel = self.bot.get_channel(mod_channel_id)  # Use self.bot
            if mod_channel:
                embed = discord.Embed(title="Deleted Message", description=f"{member} and", color=discord.Color.purple())
                await mod_channel.send(embed=embed)
            else:
                pass
        else:
            pass

    @commands.Cog.listener()
    async def on_member_ban(self, member):
        if not member.guild:
            return
        mod_channel_id = self.settings.get(member.guild.id)  # Use self.settings
        if mod_channel_id:
            mod_channel = self.bot.get_channel(mod_channel_id)  # Use self.bot
            if mod_channel:
                embed = discord.Embed(title="Deleted Message", description=f"{member} and", color=discord.Color.purple())
                await mod_channel.send(embed=embed)
            else:
                pass
        else:
            pass


async def setup(bot):
   await bot.add_cog(logging(bot))
