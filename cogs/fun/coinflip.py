import settings
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from datetime import timedelta
import datetime


class coinflip_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot






    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "coinflip",
        description= "Ban a member from the server"
    )
    async def coinflip_command(self, interaction: discord.Interaction):
        result = random.choice(['tails', 'heads'])
        embed = discord.Embed(description = f"✔️ The coin landed on {result}" , color = discord.Color.green())
        await interaction.response.send_message(embed=embed)
        

async def setup(bot):
    await bot.add_cog(coinflip_command(bot))