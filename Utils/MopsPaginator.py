import discord
import typing
import mops
from typing import *
import math
import discord

class MopsPaginator:
    def __init__(self, bot: mops.MopsClient):
        self.bot: mops.MopsClient = bot
        self.pages: List[discord.Embed] = []
        self.curPage: int = 0
        self.message: discord.Message

    async def create_paged_message(self, channel_id: int, pages: List[discord.Embed]):
        self.pages = pages
        for index, page in enumerate(self.pages):
            page.set_footer(text = f"Page: {index + 1} / {len(pages)}")

        self.message = await self.bot.get_channel(channel_id).send(embed=self.pages[0])

        await self.bot.reactionHandler.add_function(self.message, True, discord.PartialEmoji(name="◀"), self.previous_page)
        await self.bot.reactionHandler.add_function(self.message, False, discord.PartialEmoji(name="◀"), self.previous_page)
        await self.bot.reactionHandler.add_function(self.message, True, discord.PartialEmoji(name="▶"), self.next_page)
        await self.bot.reactionHandler.add_function(self.message, False, discord.PartialEmoji(name="▶"), self.next_page)

    async def create_paged_message_str(self, channel_id: int, pages: List[str]):
        e_pages = []

        for page in pages:
            current_embed = discord.Embed()
            current_embed.description = page[:min(2000, len(page))]
            e_pages.append(current_embed)

        await self.create_paged_message(channel_id, e_pages)

    async def previous_page(self, context: discord.RawReactionActionEvent):
        if self.curPage > 0:
            self.curPage -= 1
            await self.message.edit(embed = self.pages[self.curPage])

    async def next_page(self, context: discord.RawReactionActionEvent):
        if self.curPage < len(self.pages) - 1:
            self.curPage += 1
            await self.message.edit(embed = self.pages[self.curPage])

    
        

