import discord
from discord.ext import commands
import pkgutil
import sys
import inspect
from typing import *

class ReactionHandler(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot: commands.AutoShardedBot = bot

        #key: message, value: v.key: Emoji, v.value: async Function(reaction_context)
        self.on_removed: Dict[int, Dict[discord.PartialEmoji, Callable[[discord.RawReactionActionEvent], Any]]] = dict()
        self.on_added: Dict[int, Dict[discord.PartialEmoji, Callable[[discord.RawReactionActionEvent], Any]]] = dict()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id != self.bot.user.id:
            if payload.message_id in self.on_added and payload.emoji in self.on_added[payload.message_id]:
                await self.on_added[payload.message_id][payload.emoji](payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.user_id != self.bot.user.id:
            if payload.message_id in self.on_removed and payload.emoji in self.on_removed[payload.message_id]:
                await self.on_removed[payload.message_id][payload.emoji](payload)
    
    async def add_function(self, message: discord.Message, on_added: bool, emoji: discord.PartialEmoji, function: Callable[[discord.RawReactionActionEvent], Any]):
        await message.add_reaction(emoji)
        if on_added:
            if message.id not in self.on_added:
                self.on_added[message.id] = dict()
            self.on_added[message.id][emoji] = function
            print(f"{len(self.on_added[message.id])}")
        else:
            if message.id not in self.on_removed:
                self.on_removed[message.id] = dict()
            self.on_removed[message.id][emoji] = function
            print(f"{len(self.on_removed[message.id])}")

            