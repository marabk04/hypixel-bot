
import settings
import math
import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import MissingPermissions
import webcolors
import colour
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi





def is_administrator():
    def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

"""

def permission_pass():
    async def predicate(interaction: discord.Interaction):
        if interaction.user is None:
            return True
        if (
            interaction.user == interaction.user.guild.owner or
            interaction.user.guild_permissions.administrator or
            interaction.user.guild_permissions.manage_roles or
        ):   # Return False if neither condition is met
            return True
        else:
            embed = discord.Embed(title = "Command Failure",description = f"NO PERMISSIONS" , color = discord.Color.purple())
            await interaction.response.send_message(embed=embed)
    return app_commands.check(predicate)
"""

setting = {}


logger = settings.logging.getLogger("bot")
target_guild_id = 1011269469034790913
#cogs_to_add = [Greetings]
#import cmds.Calculator as Calculator
#from cmds.Calculator import *
class Slapper(commands.Converter):
    use_nicknames : bool
    def __init__(self, *, use_nicknames) -> None:
        self.use_nicknames = use_nicknames

    async def convert(self, ctx, argument):
        person = random.choice(ctx.guild.members)
        nickname = ctx.author
        if self.use_nicknames:
            nickname = ctx.author.nick

        return f"{nickname} slaps {person} with {argument}"

  

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True
    intents.members = True
    setting = {}

    
    #guild = discord.Object(id=...)  
    #Bot.tree.copy_global_to(guild=guild)

    bot = commands.Bot(command_prefix = "!", intents=intents)


    async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            return await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
        elif isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(description = f"❌ You lack the sufficient permissions to do this." , color = discord.Color.purple())
            return await interaction.response.send_message(embed=embed)
        else:
            raise error
        
        


        
    bot.tree.on_error = on_tree_error








    








    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
        for cmd_file in settings.CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":
                await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")

        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")  

        for moderation_file in settings.MODERATION_DIR.glob("*.py"):
            if moderation_file.name != "__init__.py":
                await bot.load_extension(f"cogs.moderation.{moderation_file.name[:-3]}")  


        for fun_file in settings.FUN_DIR.glob("*.py"):
            if fun_file.name != "__init__.py":
                await bot.load_extension(f"cogs.fun.{fun_file.name[:-3]}")  


        for skyblock_file in settings.SKYBLOCK_DIR.glob("*.py"):
            if skyblock_file.name != "__init__.py":
                await bot.load_extension(f"cogs.skyblock.{skyblock_file.name[:-3]}")  


    @bot.command()
    async def load(ctx, cog: str):
        await bot.load_extension(f"cogs.{cog.lower()}")
        print("cog loaded")


    @bot.command()
    async def reload_skyblock(ctx, cog: str):
        await bot.reload_extension(f"cogs.skyblock.{cog.lower()}")
        print("cog reloaded")

    @bot.command()
    async def reload_moderation(ctx, cog: str):
        await bot.reload_extension(f"cogs.skyblock.{cog.lower()}")
        print("cog reloaded")
        
    @bot.command()
    async def unload(ctx, cog: str):
        await bot.unload_extension(f"cogs.{cog.lower()}.{cog.lower()}")
        print("cog unloaded")

    
    






    @is_administrator()  
    @bot.command()
    async def sync(ctx):
        if ctx.guild.id == target_guild_id:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        else:
            print("error syncing")



    
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
