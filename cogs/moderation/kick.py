import settings
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from datetime import datetime




class kick(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()

    @app_commands.checks.has_permissions(kick_members = True )
    @app_commands.command(
        name = "kick",
        description= "kick a member from the server"
    )
    async def kick(self, interaction: discord.Interaction, member: discord.Member = None, *, reason: str = (f"No reason provided")):
        try:
            if member == None:
                embed = discord.Embed(description = f"❌ You cannot kick yourself" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
            elif member == interaction.user:
                embed = discord.Embed(description = f"❌ You cannot kick yourself" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
            elif member.guild_permissions.administrator:
                embed = discord.Embed(description = f" ❌ You cannot kick an administrator" , color = discord.Color.purple)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(description = f"✔️ {member.mention} was kicked for {reason} by {interaction.user.mention}" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
                await member.kick(reason=reason)
        except Exception:
            await interaction.response.send_message(content="There has been an error with this command. Please try again at another time.", ephemeral = True)


async def setup(bot):
    await bot.add_cog(kick(bot))