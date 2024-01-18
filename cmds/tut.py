
import math
import random
import discord
from discord.ext import commands



@commands.group()
async def tut(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"no")

@tut.command()
async def add(ctx, one:int, two:int):
    await ctx.send(one + two)

async def setup(bot):
    bot.add_command(tut)
    bot.add_command(add)