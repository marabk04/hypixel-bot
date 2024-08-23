import settings
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
import datetime
from datetime import datetime

permission_list = [
    "Administrator",
    "Manage Server",
    "Manage Roles",
    "Manage Channels",
    "Manage Messages",
    "Manage Webhooks",
    "Manage Nicknames",
    "Manage Emojis and Stickers",
    "Kick Members",
    "Ban Members",
    "Mention Everyone",
    "Timeout Members"
]

class whois_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot






    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "whois",
        description= "information about a member"
    )
    async def whois_command(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
            
            member_permissions = []


            roles = member.roles
            roles_str = ', '.join([role.mention for role in roles if role.name != "@everyone"])


            permissions = member.guild_permissions
            permissions_str = ', '.join([(perm.replace('_', " ")) for perm, value in permissions if value])
            for permission in permission_list:
                if permission in permissions_str:
                    member_permissions.append(permission)


            


            embed = discord.Embed(title = member.name ,description = member.mention , color = discord.Color.purple())

            format_joined_date = member.joined_at.strftime('%a, %b %d, %Y %I:%M %p').strip("()")
            embed.add_field(name = "Joined", value = format_joined_date)

            format_registered_date = member.created_at.strftime('%a, %b %d, %Y %I:%M %p').strip("()")
            embed.add_field(name="registered", value=format_registered_date, inline=True)

            if roles_str is not None:
                embed.add_field(name="Roles", value=f"{roles_str}", inline=False)
            else:
                embed.add_field(name="Roles", value=f"No roles", inline=False)    

            if member_permissions is not None:
                embed.add_field(name = "Permissions", value = str(member_permissions).replace("[", "").replace("]", "").replace("'", ""))

            if member.avatar is not None:
                embed.set_thumbnail(url=member.avatar.url)


            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(whois_command(bot))