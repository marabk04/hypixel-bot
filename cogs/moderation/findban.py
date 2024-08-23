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




class findban(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()

    @app_commands.checks.has_permissions(ban_members = True )
    @app_commands.command(
        name = "findban",
        description= "Check if user is banned"
    )
    async def findban(self, interaction: discord.Interaction, member: discord.Member = None):
        try:
            if member is None:
                await interaction.response.send_message("Please provide a valid member.")

            ban_entry = await interaction.guild.fetch_ban(member)

            await interaction.response.send_message(f"{member} is banned. Reason: {ban_entry.reason}")
        except discord.NotFound:
            await interaction.response.send_message(f"{member} is not banned.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")



async def setup(bot):
    await bot.add_cog(findban(bot))