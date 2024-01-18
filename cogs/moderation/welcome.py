
import math
import random
import discord
from discord.ext import commands
import discord.utils 
import asyncio
from discord import app_commands
from datetime import timedelta
from datetime import datetime

from database import welcome_channel


#this was just a test to see if I was able to store and output an embed. I wanted to make it so the user would have the option to customize the embed using buttons but I've scrapped this idea.
"""
def embed_to_dict(embed, thumbnail=None):
    embed_dict = {
        "title": embed.title,
        "description": embed.description,
        "url": embed.url,
        "color": embed.color.value if embed.color else None,
        "thumbnail": {"url": thumbnail} if thumbnail else None,
    }

    return embed_dict


class welcome_embed(discord.ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.member_avatar = True
        self.ember_title = False
        self.interaction = interaction


    async def send(self, interaction: discord.Interaction):
        embed = self.create_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    def create_embed(self, interaction):
        embed = discord.Embed(title="Museum", description="The username does not exist.", color=0x00b0f4, timestamp=datetime.now())
        if self.member_avatar:
            embed.set_thumbnail(url="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx154214-Uf9x7mY4IJJr.jpg")


        return embed
    


    @discord.ui.button(label="Member Avatar", style=discord.ButtonStyle.primary)
    async def display_member_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.member_avatar = not self.member_avatar
        embed = self.send(interaction)
        await interaction.edit_original_response(embed=embed, view=self)


    @discord.ui.button(label="Save Embed", style=discord.ButtonStyle.primary)
    async def save_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        embed_data = self.create_embed(interaction).to_dict()
        welcome_channel.update_one({"_id": str(interaction.guild_id)}, {"$set": {"message": embed_data}})
        await interaction.followup.send("x")

"""
#end


class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = {}  

    async def display_embed(self, member):
        result = welcome_channel.find_one({"_id": str(member.guild.id)})

        

        embed = discord.Embed(
            title=f"Welcome to {member.guild}",
            description="",
            timestamp=datetime.now()
        )

        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text="Example Footer", icon_url="https://slate.dan.onl/slate.png")


            
        return embed
                

    def get_channel(self, channel_id):
        return self.bot.get_channel(channel_id)




    @commands.Cog.listener()
    async def on_member_join(self, member: discord.member):
        if not (find:= welcome_channel.find_one({"_id": str(member.guild.id)})):
            return 
        
        channel = self.get_channel(find['channel'])
        message = await self.display_embed(member)
        if channel:
            await channel.send(embed=message)






    @app_commands.command()
    async def set_welcome_channel2(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if(find:= welcome_channel.find_one({"_id": str(interaction.guild.id)})):
            return await interaction.response.send_message(f"Welcome module already enabled at #{self.get_channel(find['channel'])}")
        


        welcome_channel.insert_one({"_id": str(interaction.guild.id), "channel": channel.id})
        await interaction.response.send_message(f"Welcome module enabled")



    @app_commands.command()
    async def disable_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not (find:= welcome_channel.find_one({"_id": str(interaction.guild_id)})):
            return await interaction.response.send_message(f"Welcome module is not enabled ")
        
        welcome_channel.delete_one({ "_id": str(interaction.guild_id)})
        await interaction.response.send_message(f"Welcome module disabled")


    @app_commands.command()
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not (find:= welcome_channel.find_one({"_id": str(interaction.guild_id)})):
            return await interaction.response.send_message(f"Welcome module is not enabled ")
        
        welcome_channel.update_one({"_id": str(interaction.guild_id)}, {"$set": {"channel": channel.id}})
        await interaction.response.send_message(f"welcome channel updated")


async def setup(bot):
    await bot.add_cog(welcome(bot))
