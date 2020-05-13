from discord.ext import commands
import typing

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("moderation init")

    @commands.command(help = "it pongs")
    async def ping(self, ctx):
        await ctx.send('pong')