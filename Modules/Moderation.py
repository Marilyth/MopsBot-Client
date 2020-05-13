from discord.ext import commands
import typing
import discord
import mops

class Moderation(commands.Cog):
    def __init__(self, bot: mops.MopsClient):
        self.bot = bot
        print("moderation init")

    @commands.command(help = "it pongs")
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(help = "Changes the prefix of Mops in the current Guild")
    @commands.has_permissions(manage_channel=True)
    async def SetPrefix(self, ctx: commands.Context, prefix):
        ctx.channel().trigger_typing()
        oldPrefix = self.bot.get_prefix(ctx.guild())
        self.bot.insert_or_update_prefix(ctx.guild(), prefix)
        ctx.send("Changed prefix from `{0}` to `{1}".format(oldPrefix, prefix))
