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



class unmute(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()


    @commands.has_permissions(moderate_members= True )
    @app_commands.command(
        name = "unmute",
        description= "unmute a member"
    )
    async def unmute(self, interaction: discord.Interaction, member: discord.Member = None, *, reason: str = (f"No reason provided")):
            try: 
                if member == None:
                    embed = discord.Embed(description = f"❌ No user selected" , color = discord.Color.purple())
                    await interaction.response.send_message(embed=embed)
                elif member.guild_permissions.moderate_members :
                    embed = discord.Embed(description = f"❌ Insufficient permissions" , color = discord.Color.purple())
                    await interaction.response.send_message(embed=embed)
                elif member.is_timed_out() == False:
                    embed = discord.Embed(description = f"❌ User has no time out" , color = discord.Color.purple())
                    await interaction.response.send_message(embed=embed)
                else:
                    if member.is_timed_out():
                        await member.timeout(None, reason = reason)
                        embed = discord.Embed(description = f"✔️ Timeout successfully removed from user" , color = discord.Color.purple())
            except Exception as e:
                embed = discord.Embed(description = f"❌ {e}" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(unmute(bot))