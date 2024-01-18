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
import colour
import webcolors





class role_command(commands.GroupCog, name="role"):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()


    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(
        name="add",
        description="Add a role from a member"
    )
    async def role_add_command(self, interaction: discord.Interaction, member: discord.Member, *, role: discord.Role):
        try:
            role_to_edit = discord.utils.get(interaction.guild.roles, name=role.name)
            if role_to_edit is not None:
                if role_to_edit not in member.roles:
                    await member.add_roles(role_to_edit)
                    embed = discord.Embed(description=f"✅ Added '{role_to_edit.name}' role to {member.mention}", color=discord.Color.green())
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(description=f"❌ {member.mention} already has '{role_to_edit.name}' role", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(description=f"❌ '{role.name}' not found", color=discord.Color.red())
                await interaction.response.send_message(embed=embed)
        except AttributeError:
            embed = discord.Embed(description=f"❌ '{role.name}' not found", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)



    @app_commands.checks.has_permissions(manage_roles = True)
    @app_commands.command(
        name = "remove",
        description= "Remove a role from a member")
    async def role_remove_command(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        try:
            role_to_edit = discord.utils.get(interaction.guild.roles, name=role.name)
            if role_to_edit in member.roles:
                await member.remove_roles(role_to_edit)
                embed = discord.Embed(description = f"✔️ Removed '{role}' from {member.mention}" , color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(description = f"❌ {member.mention} did not have '{role}'" , color = discord.Color.red())
                await interaction.response.send_message(embed=embed)
        except AttributeError: 
            embed = discord.Embed(description = f"❌ '{role}' not found" , color = discord.Color.red())
            await interaction.response.send_message(embed=embed)



    @app_commands.checks.has_permissions(manage_roles = True)
    @app_commands.command(
        name = "all",
        description= "Add or Remove a role to all members")
    async def role_all_command(self, interaction: discord.Interaction, member: discord.Member, *, role: discord.Role):
        try:
            role_to_edit = discord.utils.get(interaction.guild.roles, name=role.name)
            if role_to_edit not in member.roles:
                await member.add_roles(role_to_edit)
                embed = discord.Embed(description = f" ✔️ Added {role_to_edit.name} role to {member.mention}" , color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
            if role_to_edit in member.roles:
                await member.remove_roles(role_to_edit)
                embed = discord.Embed(description = f"✔️ Removed '{role}' from {member.mention}" , color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
        except AttributeError: 
            embed = discord.Embed(description = f"❌ Role '{role}' not found" , color = discord.Color.red())
            await interaction.response.send_message(embed=embed)


    @app_commands.checks.has_permissions(manage_roles = True)
    @app_commands.command(
        name = "color",
        description= "Change the color of any role")
    async def role_color_command(self, interaction:discord.Interaction, role: discord.Role, color: str or int):
        try:
            if isinstance(color, str):
                try:
                    hex_color = webcolors.name_to_hex(color)
                except ValueError:
                    hex_color = colour.Color(color).hex_l
                new_color = discord.Color(int(hex_color.lstrip("#"), 16))
            elif isinstance(color, int):
                new_color = discord.Color(color)
            else:
                raise ValueError
            await role.edit(color=new_color)
            embed = discord.Embed(description = f"✔️ Updated {role.name} color to {color}", color = discord.Color.purple())
            await interaction.response.send_message(embed=embed)
        except ValueError:
            embed = discord.Embed(description="❌ Please enter a vaild color format", color=discord.Color.purple())
            await interaction.response.send_message(embed=embed)
        except Exception:
            embed = discord.Embed(description="❌ Please Enter a vaild color", color=discord.Color.purple())
            await interaction.response.send_message(embed=embed)


    @app_commands.checks.has_permissions(manage_roles = True)
    @app_commands.command(
        name = "hoist",
        description= "Change the color of any role")
    async def role_hoist_command(self, interaction: discord.Interaction, role: discord.Role):
        if role:
            if role.hoist:
                await role.edit(hoist=False)
                embed = discord.Embed(description = f"✔️ Updated {role} to not be shown separately ", color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
            else:
                await role.edit(hoist=True)
                embed = discord.Embed(description = f"✔️ Updated {role} to be shown separately", color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
        else:
            if role == None:
                embed = discord.Embed(description = f"❌ You need to select a role" , color = discord.Color.red())
                await interaction.response.send_message(embed=embed)

    @app_commands.checks.has_permissions(manage_roles = True)
    @app_commands.command(
        name = "mention",
        description= "Make any role mentionable or unmentionable")
    async def role_mention_command(self, interaction: discord.Interaction, role: discord.Role):
        if role:
            if role.mentionable:
                await role.edit(mentionable=False)
                embed = discord.Embed(description = f"✔️ Updated {role} to not be mentionable", color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
            else:
                await role.edit(mentionable=True)
                embed = discord.Embed(description = f"✔️ Updated {role} to be mentionable", color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
        else:
            if role == None:
                embed = discord.Embed(description = f"❌ You need to select a role" , color = discord.Color.red())
                await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name = "position",
        description= "Make any role mentionable or unmentionable")
    async def role_position_command(self, interaction: discord.Interaction, role: discord.Role, pos: int):
        if role:
                await role.edit(position=pos)
                embed = discord.Embed(description = f"✔️ Updated {role} to the position {pos}", color = discord.Color.green())
                await interaction.response.send_message(embed=embed)
        else:
            if role == None:
                embed = discord.Embed(description = f"❌ You need to select a role" , color = discord.Color.red())
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(description = f"❌ Insufficient permissions", color = discord.Color.red())
                await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(role_command(bot))