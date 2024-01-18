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


class multiplication_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot






    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "multiply",
        description= "Ban a member from the server"
    )
    async def multiplication_command(self, interaction: discord.Interaction, x:float, y:float):
            try:
                result = x*y
                if result % 1 == 0:
                    embed = discord.Embed(description = f"✔️ The sum of {x} * {y} is {int(result)}" , color = discord.Color.green())
                    await interaction.response.send_message(embed=embed)
                    await interaction.response.send_message(int(result))
                else:
                    embed = discord.Embed(description = f"✔️ The sum of {x} * {y} is  {result}" , color = discord.Color.green())
                    await interaction.response.send_message(embed=embed)
            except:
                embed = discord.Embed(description = f"❌ Please input valid a number" , color = discord.Color.red())
                await interaction.response.send_message(embed=embed)
        


    

 


    
    

async def setup(bot):
    await bot.add_cog(multiplication_command(bot))