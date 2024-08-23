import random
import discord
from discord.ext import commands
import discord.utils 
from discord import app_commands


class hug_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.checks.has_permissions(send_messages = True)
    @app_commands.command(
        name = "hug",
        description= "give a fat hug to a special someone"
        )
    async def hug(self, interaction: discord.Interaction):
        hug_gifs = [
            "https://tenor.com/view/hug-warm-hug-depressed-hug-gif-4585064738068342394",
            "https://tenor.com/view/laverne-and-shirley-funny-cool-gif-27491810",
            "https://tenor.com/view/milk-and-mocha-milk-mocha-milk-mocha-bear-milk-bear-mocha-bear-gif-1899012525858648612"
            ]

        message = random.choice(hug_gifs)
        await interaction.channel.send(content=message)

async def setup(bot):
    await bot.add_cog(hug_command(bot))
    