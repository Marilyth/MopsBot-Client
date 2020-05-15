from discord.ext import commands
import typing
import discord
import json
import mops
import urllib
import datetime
import requests
import time
from Utils.MopsUser import MopsUser

class Information(commands.Cog):
    def __init__(self, bot: mops.MopsClient):
        self.bot = bot
        print("Database init")

    @commands.command(help = "Hugs the specified person")
    @commands.cooldown(5, 3600, commands.cooldowns.BucketType.user)
    async def Hug(self, ctx: commands.context.Context, *, member: discord.User):
        user = await MopsUser.get_user(self.bot, member.id)

        def modify(mops_user: MopsUser):
            mops_user.Hugged += 1

        await MopsUser.modify_user(self.bot, user, modify)

        await ctx.send(f"Aww, **{member.display_name}** got hugged by **{ctx.author.display_name}**.\n" +
                       f"They have already been hugged {user.Hugged} times!")

    @commands.command(help = "Smooches the specified person")
    @commands.cooldown(5, 3600, commands.cooldowns.BucketType.user)
    async def Kiss(self, ctx: commands.context.Context, *, member: discord.User):
        user = await MopsUser.get_user(self.bot, member.id)

        def modify(mops_user: MopsUser):
            mops_user.Kissed += 1

        await MopsUser.modify_user(self.bot, user, modify)

        await ctx.send(f"Mwaaah, **{member.display_name}** got kissed by **{ctx.author.display_name}**.\n" +
                       f"They have already been kissed {user.Kissed} times!")

    @commands.command(help = "Punches the specified person")
    @commands.cooldown(5, 3600, commands.cooldowns.BucketType.user)
    async def Punch(self, ctx: commands.context.Context, *, member: discord.User):
        user = await MopsUser.get_user(self.bot, member.id)

        def modify(mops_user: MopsUser):
            mops_user.Punched += 1

        await MopsUser.modify_user(self.bot, user, modify)

        await ctx.send(f"DAAMN! **{member.display_name}** just got punched by **{ctx.author.display_name}**.\n" +
                       f"They have been punched {user.Kissed} times!")