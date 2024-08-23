import random
import discord
from discord.ext import commands
import discord.utils 
from discord import app_commands
from database import collection

married_log = collection["married"]

class marry_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot


    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "marry",
        description= "joins two souls together"
    )

    async def marry(self, interaction: discord.Interaction, crush: discord.Member):
        if interaction.user == crush:
            return await interaction.response.send_message(f"You cannot marry yourself, please try to get some bitches.")
        if married_log.find_one({"married": interaction.user.id}):
            return await interaction.response.send_message(f"You are already married to {crush.mention}. Stop trying to cheat you fucking cheating whore")

        married_log.insert_one({"married": interaction.user.id, "married_to": crush.id})
        married_messages = [
            "Behold the union of {interaction.user.mention} and {crush.mention} in holy matrimony!",
            "Witness the sacred bond formed between {interaction.user.mention} and {crush.mention} as they enter the bliss of marriage!",
            "Hark! {interaction.user.mention} and {crush.mention} have joined hands in the covenant of marriage!",
            "Celebrate the nuptials of {interaction.user.mention} and {crush.mention}, united in wedded bliss!",
            "Announcing the marriage of {interaction.user.mention} and {crush.mention}! Let joy resound!",
            "It is with great joy that we announce the union of {interaction.user.mention} and {crush.mention} in marriage!",
            "Ringing bells of love for {interaction.user.mention} and {crush.mention} as they embark on their journey together as spouses!",
            "In the book of love, a new chapter begins for {interaction.user.mention} and {crush.mention}, bound together in marriage!",
            "With hearts intertwined, {interaction.user.mention} and {crush.mention} now stand as one in the sacred vows of marriage!",
            "Let the world know that {interaction.user.mention} and {crush.mention} have exchanged vows and become one in marriage's embrace!"
        ]
  
        message = random.choice(married_messages)
        await interaction.response.send_message(content=message.format(interaction=interaction, target=crush))



async def setup(bot):
    await bot.add_cog(marry_command(bot))
    