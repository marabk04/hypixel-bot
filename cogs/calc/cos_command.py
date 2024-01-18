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


class cos_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot






    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "cos",
        description= "Ban a member from the server"
    )
    async def cos_command(self, interaction: discord.Interaction, x:float):
        try:
            cos_result = math.cos(x)
            embed = discord.Embed(description = f"✔️ The cos of {x} is {cos_result}" , color = discord.Color.purple())
            await interaction.response.send_message(embed=embed)       
        except:
            embed = discord.Embed(description = f"❌ Please input valid a number" , color = discord.Color.red())
            await interaction.response.send_message(embed=embed)
    

    

 


    
    

async def setup(bot):
    await bot.add_cog(cos_command(bot))