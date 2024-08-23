import settings
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from discord import Guild
from datetime import timedelta
import datetime



class unban(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()

    @commands.has_permissions(ban_members = True)
    @app_commands.command(
        name = "unban",
        description= "unban a member"
    )
    async def unban(self, interaction: discord.Interaction, member: discord.User = None, *, reason: str = (f"No reason provided")):
        try:
            if member == None:
                embed = discord.Embed(description = f"❌ You need to select a member" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(description = f"✔️ Unbanned {member.mention} for {reason} by {interaction.user.mention}" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
                await interaction.guild.fetch_ban(member)
                await interaction.guild.unban(member, reason = reason)
        except Exception as e:
            embed = discord.Embed(description = f"❌ An error has occured {e}" , color = discord.Color.purple())
            await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(unban(bot))