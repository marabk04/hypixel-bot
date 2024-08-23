from database import married_log
import random
import discord
from discord.ext import commands
import discord.utils 
from discord import app_commands


class divorce_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.checks.has_permissions(send_messages = True )
    @app_commands.command(
        name = "divorce",
            description= "removes two souls together"
        )
    async def divorce(self, interaction: discord.Interaction, target: discord.Member):
        if not married_log.find_one({"married": interaction.user.id}):
            return await interaction.response.send_message(f"You aren't even married......")
        
        
        married_log.delete_one({"married": interaction.user.id})
        divorce_messages = [
            "The union of {interaction.user.mention} and {target.mention} has come to an end.",
            "The sacred bond between {interaction.user.mention} and {target.mention} has been dissolved.",
            "After careful consideration, {interaction.user.mention} and {target.mention} have decided to part ways.",
            "{interaction.user.mention} and {target.mention} are no longer united in wedded bliss.",
            "{interaction.user.mention} and {target.mention} have chosen to end their journey together as spouses.",
            "{interaction.user.mention} and {target.mention} have decided to go their separate ways.",
            "{interaction.user.mention} and {target.mention} are divorcing. Let us offer them support during this transition.",
            "With heavy hearts, we announce the end of {interaction.user.mention} and {target.mention}'s marriage.",
            "{interaction.user.mention} and {target.mention} have exchanged vows no more.",
            "Announcing the dissolution of the marriage between {interaction.user.mention} and {target.mention}.",
        ]
        message = random.choice(divorce_messages)
        await interaction.response.send_message(content=message.format(interaction=interaction, target=target))



async def setup(bot):
    await bot.add_cog(divorce_command(bot))
    