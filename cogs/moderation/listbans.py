import settings
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from discord import Guild
from datetime import datetime


class listbans(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()

    @commands.has_permissions(ban_members = True)
    @app_commands.command(
        name = "listbans",
        description= "List all current bans"
    )
    async def listbans(self, interaction: discord.Interaction):
        if interaction.guild.bans is not None:
            embed = discord.Embed(title = f"Displaying active bans" ,description = "" , color = discord.Color.purple(), timestamp=datetime.now())
            async for entry in interaction.guild.bans(limit=150):
                user = entry.user
                reason = entry.reason
                await interaction.channel.send(embed=embed)
                embed.add_field(name = f"{user} was banned", value = f"Reason: {reason}")
        else: 
            embed = discord.Embed(title = f"Command Failure " ,description = f"There are no active bans" , color = discord.Color.purple(), timestamp=datetime.now())

async def setup(bot):
    await bot.add_cog(listbans(bot))

