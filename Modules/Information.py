from discord.ext import commands
import typing
import discord
import json
import mops
import urllib
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
    @commands.cooldown(1, 10, discord.ext.commands.cooldowns.BucketType.guild)
    async def Define(self, ctx: commands.context.Context, *, text: str):
        results = json.loads(await Information.get_url_async(f"http://api.wordnik.com:80/v4/word.json/{text}/definitions?includeRelated=false&sourceDictionaries=all&useCanonical=true&includeTags=false&api_key={self.bot.config['Wordnik']}"))

        definitions = []
        for result in results:
            if 'text' in result:
                definitions.append(f"__**{result['word']}**__\n\n``{result['text']}``")
        
        await MopsPaginator(self.bot).create_paged_message_str(ctx.channel.id, definitions)

    @commands.command(help = "Translates your text from srcLanguage to tgtLanguage")
    @commands.cooldown(1, 10, discord.ext.commands.cooldowns.BucketType.guild)
    async def Translate(self, ctx: commands.context.Context, srcLanguage: str, tgtLanguage: str, *, text: str):
        await ctx.trigger_typing()
        result = json.loads(await self.get_url_async(f"https://translate.googleapis.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&sl={srcLanguage}&tl={tgtLanguage}&dt=t&q={text}"))
        await ctx.send(str(result[0][0][0]))

    @commands.command(help = "Sends a query to wolfram alpha, and returns the results")
    @commands.cooldown(1, 10, discord.ext.commands.cooldowns.BucketType.guild)
    async def Wolfram(self, ctx: commands.context.Context, *, query: str):
        await ctx.trigger_typing()
        result = json.loads(await self.get_url_async(f"https://api.wolframalpha.com/v2/query?input={urllib.parse.quote(query.encode('utf-8'))}&format=image,plaintext&podstate=Step-by-step%20solution&output=JSON&appid={self.bot.config['WolframAlpha']}"))
        
        embeds = []
        for pod in result["queryresult"]["pods"]:
            pod_embed = discord.Embed()
            image = next((x["img"]["src"] for x in pod["subpods"] if x["title"] == "Possible intermediate steps"), None)
            if image is None and len(pod["subpods"]) > 0:
                image = pod["subpods"][0]["img"]["src"]

            pod_embed.set_image(url=image).description = query
            pod_embed.title = pod["title"]
            embeds.append(pod_embed)

        await MopsPaginator(self.bot).create_paged_message(ctx.channel.id, embeds)

    @staticmethod
    async def get_url_async(url: str) -> str:
        return requests.get(url).content.decode()