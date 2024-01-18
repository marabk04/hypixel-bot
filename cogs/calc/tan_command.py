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


class tan_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot






    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "tan",
        description= "Ban a member from the server"
    )
    async def tan_command(self, interaction: discord.Interaction, x:float):
        try:
            tan_result = math.tan(x)
            embed = discord.Embed(description = f"✔️ The tan of {x} is {tan_result}" , color = discord.Color.green())
            await interaction.response.send_message(embed=embed)
        except:
            embed = discord.Embed(description = f"❌ Please input valid a number" , color = discord.Color.red())
            await interaction.response.send_message(embed=embed)
    

async def setup(bot):
    await bot.add_cog(tan_command(bot))