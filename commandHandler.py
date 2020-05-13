import discord

class commandHandler():
    async def on_message(self, client: discord.Client, message: discord.Message):
        print('{0.author} send a message in {0.channel}'.format(message))