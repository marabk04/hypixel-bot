import settings
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from datetime import datetime



class ban(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()







    @app_commands.checks.has_permissions(ban_members = True )
    @app_commands.command(
        name = "ban",
        description= "Ban a member from the server"
    )
    async def ban_command(self, interaction: discord.Interaction, member: discord.Member = None, *, reason: str = (f"No reason provided")):
        if member == None:
            embed = discord.Embed(description = f"❌ You need to select a member" , color = discord.Color.purple())
            await interaction.response.send_message(embed=embed)
        elif member == interaction.user:
            embed = discord.Embed(description = f"❌ You cannot ban yourself" , color = discord.Color.purple())
            await interaction.response.send_message(embed=embed)
        elif member.guild_permissions.administrator:
            embed = discord.Embed(description = f"❌ You cannot ban an administrator" , color = discord.Color.purple())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(description = f"✔️ {member.mention} was banned for {reason} by {interaction.user.mention}")
            await interaction.response.send_message(embed=embed)
            await member.ban(reason=reason)



    

 


    
    

async def setup(bot):
    await bot.add_cog(ban(bot))