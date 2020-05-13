from discord.ext import commands
import typing

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("moderation init")

    @commands.command()
    async def ping(self, ctx):
        """it pongs"""
        await ctx.send('pong')