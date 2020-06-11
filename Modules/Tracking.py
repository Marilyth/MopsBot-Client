from discord.ext import commands
import typing
import discord
import mops
from Utils.Trackers import case_sensitive_types
from discord.ext.commands import bot_has_permissions
from discord.permissions import Permissions
trackers = dict()

class Tracker(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        tracker_type = ctx.command.full_parent_name
        cur_trackers = trackers[tracker_type]
        if tracker_type not in case_sensitive_types:
            argument = argument.lower()

        if argument in cur_trackers:
            return cur_trackers[argument]
        else:
            raise Exception("Could not find the tracker")

class Tracking(commands.Cog):
    def __init__(self, bot: mops.MopsClient):
        global trackers
        self.bot = bot
        trackers = self.bot.trackers
        print("tracking init")

    @commands.group("Twitch", invoke_without_command=True, case_insensitive=True)
    async def Twitch(self, ctx):
        print("I don't know why modules must be a command themselves ¯\_(ツ)_/¯")

    @Twitch.command(name="Track", help = "Keeps track of the specified Streamer, in the Channel you are calling this command in.")
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.user)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    @commands.has_permissions(manage_channels=True)
    async def TwitchTrack(self, ctx, streamerName, *, notificationMessage = "Streamer went live"):
        async def callback(message, ctx):
            await ctx.send(f"Server responded with:\n{message.content}")
        await self.bot.trackers.add(ctx.command.full_parent_name, streamerName, ctx.channel.id, notificationMessage, callback, ctx)

    @Twitch.command(name="UnTrack", help = "Stops tracking the specified streamer.")
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def TwitchUnTrack(self, ctx, Streamer: str):
        async def callback(message):
            await ctx.send(f"Server responded with:\n{message.content}")
        await self.bot.trackers.remove(ctx.command.full_parent_name, Streamer, ctx.channel.id, callback)

    @Twitch.command(name="SetNotification", help = "Sets the notification text that is used each time a streamer goes live.")
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def TwitchSetNotification(self, ctx, Streamer: str, notificationMessage:str = ""):
        async def callback(message):
            await ctx.send(f"Server responded with:\n{message.content}")
        await self.bot.trackers.set_notification(ctx.command.full_parent_name, Streamer, ctx.channel.id, notificationMessage, callback)

    @Twitch.command(name="GetTrackers", help = "Returns the streamers that are tracked on this server.")
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def TwitchGetTrackers(self, ctx, Streamer: str, notificationMessage:str = ""):
        async def callback(message):
            await ctx.send(f"Server responded with:\n{message.content}")
        await self.bot.trackers.set_notification(ctx.command.full_parent_name, Streamer, ctx.channel.id, notificationMessage, callback)

    @Twitch.command(name="ChangeConfig", help = "Edit the Configuration for the tracker.")
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def TwitchChangeConfig(self, ctx, Streamer: Tracker):
        async def callback(message):
            await ctx.send(f"Server responded with:\n{message.content}")

        await ctx.send(f"Current config:\n{trackers.get_config_str(Streamer, ctx.channel.id)}\n\nPlease reply with one or more changed lines.")

        def check(m):
            return m.channel == ctx.channel and m.author.id == ctx.author.id

        message = await self.bot.wait_for('message', check = check)

        await self.bot.trackers.change_config(ctx.command.full_parent_name, Streamer, ctx.channel.id, message.content, callback)