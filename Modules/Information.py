from discord.ext import commands
import typing
import discord
import json
import mops
import requests
from Utils.MopsPaginator import MopsPaginator

class Information(commands.Cog):
    def __init__(self, bot: mops.MopsClient):
        self.bot = bot
        print("information init")

    @commands.command(help = "Returns the date you joined the guild")
    async def HowLong(self, ctx: commands.context.Context):
        await ctx.send(f"You joined this guild on {ctx.message.author.joined_at}")

    @commands.command(help = "Returns an invite link for the bot")
    async def Invite(self, ctx: commands.context.Context):
        await ctx.send(f"https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=271969344&scope=bot")

    @commands.command(help = "Returns a link to vote for the bot")
    async def Vote(self, ctx: commands.context.Context):
        await ctx.send(f"https://discordbots.org/bot/{self.bot.user.id}/vote")

    @commands.command(help = "Searches dictionaries for a definition of the specified word or expression")
    async def Define(self, ctx: commands.context.Context, *, text: str):
        results = json.loads(await Information.get_url_async(f"http://api.wordnik.com:80/v4/word.json/{text}/definitions?includeRelated=false&sourceDictionaries=all&useCanonical=true&includeTags=false&api_key={self.bot.config['Wordnik']}"))

        definitions = []
        for result in results:
            if 'text' in result:
                definitions.append(f"__**{result['word']}**__\n\n``{result['text']}``")
        
        paginator = MopsPaginator(self.bot)
        await paginator.create_paged_message_str(ctx.channel.id, definitions)

    @staticmethod
    async def get_url_async(url: str) -> str:
        return requests.get(url).content.decode()