import discord
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def echo(self, ctx, arg):
        await ctx.send("{}".format(arg))

def setup(bot):
    bot.add_cog(Basic(bot)) 