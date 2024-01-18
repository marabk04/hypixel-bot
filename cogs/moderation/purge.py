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



class purge(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()



        
    @commands.has_permissions(kick_members = True)
    @app_commands.command()
    async def purge(self, interaction: discord.Interaction, member: discord.Member = None, *, reason: str = (f"No reason provided")):
        if member == None:
            await interaction.response.send_message(f"You need to select a member")
        elif member == interaction.message.author:
            await interaction.response.send_message(f"You cannot kick yourself")
        elif member.guild_permissions.administrator:
            await interaction.response.send_message(f"You cannot kick an administrator")
        else:
            await interaction.purge(limit = 100)

            
    @commands.has_permissions(manage_roles= True )
    @commands.command()
    async def purge3(self, ctx, member: discord.Member = None, *, limit: int):
        print(f"Requested by: {ctx.author}")
        print(f"Member: {member}")
        print(f"Amount: {limit}")

        def is_member_message(message):
            return message.author == member if member else False
        
        if member is not None:
            deleted = await ctx.channel.purge(limit=limit, check=is_member_message)
            await ctx.send(f"Deleted {len(deleted)} messages from {member.display_name}.")
        elif member == ctx.author:
            await ctx.send("You cannot kick yourself.")
        else:
            deleted = await ctx.channel.purge(limit= limit)
            await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=2)



async def setup(bot):
    await bot.add_cog(purge(bot))