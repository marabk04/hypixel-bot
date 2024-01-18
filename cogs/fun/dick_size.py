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
import eight_ball


class dick_size(commands.Cog):
    def __init__(self, bot: commands.bot):
        super().__init__()
        self.bot = bot
        self.leaderboard = {}






    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "penislength",
        description= "check penislength"
    )
    async def dick_size3(self, interaction: discord.Interaction):



        random.seed(interaction.user.id)
        number = random.randint(0, 30)
        p = "8" + "=" * number + "D"
        size_in_inches = float(number) * 0.5
        size_in_cm = float(number) * 2.54
        self.leaderboard[interaction.user.id] = size_in_inches


        await interaction.response.send_message(f"{interaction.user.mention}'s penis length is: {size_in_inches} inches! ({size_in_cm} cm)\n{p}")



    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "penisleaderboard",
        description= "check penislength leaderboard"
    )
    async def dick_size2(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"penis", type = 'rich', colour=0x00b0f4)

        leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
    
        for index, (user_id, size_in_inches) in enumerate(leaderboard, start=1):
                    member = interaction.guild.get_member(user_id)
                    username = member.name if member else f"Unknown User ({user_id})"
                    
                    embed.add_field(name=f"{index}. {username}", value=f"{size_in_inches} inches ({float(size_in_inches) * 2.54}cm)" , inline=False)


        await interaction.response.send_message(embed=embed)


        

async def setup(bot):
    await bot.add_cog(dick_size(bot))
    