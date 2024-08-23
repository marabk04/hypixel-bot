import random
import discord
from discord.ext import commands
import discord.utils 
from discord import app_commands



class kiss_command(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot


    @app_commands.checks.has_permissions(send_messages = True)
    @app_commands.command(
        name = "kiss",
        description= "give a fat kiss to a special someone"
        )
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):
        kiss_messages = [
            "{interaction.user.mention} and {member.mention} share a tender kiss.",
            "{interaction.user.mention} leans in to kiss {member.mention} softly.",
            "As the moonlight bathes them, {interaction.user.mention} and {member.mention} steal a kiss.",
            "With a smile, {interaction.user.mention} presses their lips against {member.mention}'s cheek.",
            "In a moment of passion, {interaction.user.mention} and {member.mention} lock lips.",
            "{interaction.user.mention} gives {member.mention} a playful peck on the lips.",
            "A gentle breeze carries the whispers of {interaction.user.mention} and {member.mention}'s kiss.",
            "The world seems to fade away as {interaction.user.mention} and {member.mention} share a kiss.",
            "{interaction.user.mention} brushes their lips against {member.mention}'s, leaving them both wanting more.",
            "In a romantic embrace, {interaction.user.mention} and {member.mention} share a passionate kiss."
            ]

        message = random.choice(kiss_messages)
        await interaction.response.send_message(content=message.format(interaction=interaction, target=member))
        
async def setup(bot):
    await bot.add_cog(kiss_command(bot))
    