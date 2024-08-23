import random
import discord
from discord.ext import commands
import discord.utils 
from discord import app_commands
from database import collection

hypixel_api_collection = collection["hypixelapi"]
fixed_id = 206512728993562624

class hypixel_api(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.hypixel_api_key = self.get_hypixel_api_key()  


    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "hypixel_api",
        description= "set hypixel api"
    )

    async def set_hypixel_api_key(self, interaction: discord.Interaction, api: str):
        hypixel_api_collection.update_one(
            {"id": fixed_id},
            {"$set": {"API_KEY": api}},
            upsert=True
        )
        self.hypixel_api_key = api  
        await interaction.response.send_message(f"Hypixel api key is set as {api}" )


    @app_commands.command(
        name="get_hypixel_api",
        description="Get the Hypixel API key"
    )
    async def get_api_key(self, interaction: discord.Interaction):
        api_key_doc = hypixel_api_collection.find_one({"id": fixed_id})
        if api_key_doc and "API_KEY" in api_key_doc:
            self.hypixel_api_key = api_key_doc['API_KEY'] 
            await interaction.response.send_message(f"The Hypixel API key is {self.hypixel_api_key}")
        else:
            await interaction.response.send_message("The Hypixel API key has not been set yet.")

    def get_hypixel_api_key(self):
        api_key_doc = hypixel_api_collection.find_one({"id": fixed_id})
        if api_key_doc and "API_KEY" in api_key_doc:
            return api_key_doc['API_KEY']
        return None


async def setup(bot):
    await bot.add_cog(hypixel_api(bot))
    