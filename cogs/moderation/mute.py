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



class mute(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()

    @commands.has_permissions(moderate_members = True)
    @app_commands.command(
        name = "mute",
        description= "Temporarily mute a member"
    )
    async def mute(self, interaction: discord.Interaction, member: discord.Member = None, *, time: str = None, reason: str = "no reason provided"):
        try:
            if member == None:
                embed = discord.Embed(description = f"❌ You need to select a member" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
            elif member == interaction.user:
                embed = discord.Embed(description = f"❌ You cannot kick yourself" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
            elif member.guild_permissions.administrator:
                embed = discord.Embed(description = f"❌ You cannot kick an administrator" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
            elif member.is_timed_out() == True:
                embed = discord.Embed(description = f"❌ User is already muted" , color = discord.Color.purple())
                await interaction.response.send_message(embed=embed)
            else: 
                if "s" in time:
                    new_time= time.strip("s")
                    if int(new_time) > 2419000:
                        embed = discord.Embed(description = f"**❌The mute time cannot be longer than 28 days**" , color = discord.Color.purple())
                        await interaction.response.send_message(embed=embed)      
                    else:
                        time_value = datetime.timedelta(seconds=int(new_time))
                        await member.edit(timed_out_until=discord.utils.utcnow() + time_value)
                        embed = discord.Embed(title = f"{member.mention} muted for {new_time} second(s)",description = f"Reason: {reason}" , color = discord.Color.purple())
                        await interaction.response.send_message(embed=embed)
                if "m" in time:
                    new_time= time.strip("m")
                    if int(new_time) > 40320:
                        embed = discord.Embed(description = f"❌ The mute time cannot be longer than 28 days" , color = discord.Color.purple())
                        await interaction.response.send_message(embed=embed)                    
                    else:
                        time_value = datetime.timedelta(minutes=int(new_time))
                        await member.edit(timed_out_until=discord.utils.utcnow() + time_value)
                        embed = discord.Embed(title = f"{member.mention} muted for {new_time} minute(s)",description = f"Reason: {reason}" , color = discord.Color.purple())
                        await interaction.response.send_message(embed=embed)
                if "h" in time:
                    new_time= time.strip("h")
                    if int(new_time) > 672:
                        embed = discord.Embed(description = f"❌ The mute time cannot be longer than 28 days" , color = discord.Color.purple())
                        await interaction.response.send_message(embed=embed)
                    else:
                        time_value = datetime.timedelta(hours=int(new_time))
                        await member.edit(timed_out_until=discord.utils.utcnow() + time_value)
                        embed = discord.Embed(title = f"{member.mention} muted for {new_time} hour(s)",description = f"Reason: {reason}" , color = discord.Color.purple())
                        await interaction.response.send_message(embed=embed)
                if "d" in time:
                    new_time= time.strip("d")
                    if int(new_time) > 2419000:
                        embed = discord.Embed(title = "Command Failure",description = f"The mute time cannot be longer than 28 days" , color = discord.Color.purple())
                        await interaction.response.send_message(embed=embed)
                    else:
                        time_value = datetime.timedelta(days=int(new_time))
                        await member.edit(timed_out_until=discord.utils.utcnow() + time_value)
                        embed = discord.Embed(title = f"{member.mention} muted for {new_time} day(s)",description = f"Reason: {reason}" , color = discord.Color.purple())
                        await interaction.response.send_message(embed=embed)
                else:
                    print("kyu")
        except:
            await interaction.response.send_message(f"there was an error")


async def setup(bot):
    await bot.add_cog(mute(bot))