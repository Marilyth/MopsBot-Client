from discord.ext import commands
import typing
import discord
import mops

trackers = dict()

class Tracker(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        tracker_type = ctx.command.full_parent_name
        
        cur_trackers = trackers[tracker_type]
        if argument in cur_trackers:
            return cur_trackers[argument]
        else:
            raise Exception("Could not find tracker")

class Tracking(commands.Cog):
    def __init__(self, bot: mops.MopsClient):
        global trackers
        self.bot = bot
        trackers = self.bot.trackers
        print("tracking init")

    @commands.group("Twitch", invoke_without_command=True, case_insensitive=True)
    async def Twitch(self):
        print("I don't know why modules must be a command themselves ¯\_(ツ)_/¯")

    @Twitch.command(help = "Testing type reader")
    async def Test(self, ctx, Tracker: Tracker):
        await ctx.send(Tracker["_id"])