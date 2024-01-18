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


class eightball_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot






    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "eightball",
        description= "Eightball"
    )
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        ball = eight_ball.ball()

        embed = discord.Embed(title = "The eightball has spoken",description = f"{(ball.response(question))} " , color = discord.Color.purple())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(eightball_command(bot))
    