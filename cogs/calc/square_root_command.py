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


class square_root_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot






    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "sqrt",
        description= "Ban a member from the server"
    )
    async def subtraction_command(self, interaction: discord.Interaction, x:float):
        try:
            sqrt_result = math.sqrt(x)
            embed = discord.Embed(description = f"✔️ The square root of {x} is {sqrt_result}" , color = discord.Color.green())
            await interaction.response.send_message(embed=embed)
        except:
            embed = discord.Embed(description = f"❌ Please input valid a number" , color = discord.Color.red())
            await interaction.response.send_message(embed=embed)



    

 


    
    

async def setup(bot):
    await bot.add_cog(square_root_command(bot))