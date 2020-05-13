import discord
import socket
import json
import time
import asyncio
from dateutil import parser

class TrackerClient:
    def __init__(self, bot, ip: str, port: int):
        self.HOST = '127.0.0.1'
        self.PORT = 11000
        self.server: socket = None
        self.bot = bot

    async def send_message(self, message: str):
        self.server.send(str.encode(message))

    async def received_message(self, message: str):
        try:
            print("data recieved: {0}".format(message))

            data = message.split("STARTEVENT ")[1].split(sep="\n", maxsplit=1)
            event_id = int(data[0])
            eventMessage = json.loads(data[1].split("ENDEVENT " + str(event_id))[0])

            channel = self.bot.get_channel(eventMessage["ChannelId"])
            embed = self.dnet_embed_to_py(eventMessage["Embed"])

            await channel.send(eventMessage["Notification"], embed=embed)
        except:
            pass

    async def start_connection_loop(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    self.server = s
                    self.server.connect((self.HOST, self.PORT))
                    while True:
                            data = self.server.recv(8192)
                            await self.received_message(data.decode())
                            await self.send_message("Received data")
                except Exception as e:
                    print(e)
                    print("Connection was interrupted, trying again in 10 seconds.")
                    await asyncio.sleep(10)

    def dnet_embed_to_py(self, json_dict) -> discord.Embed:
        embed = discord.Embed()
        embed.title = json_dict["Title"]
        embed.description = json_dict["Description"]
        embed.url = json_dict["Url"]
        embed.timestamp = parser.parse(json_dict["Timestamp"])
        embed.colour = discord.colour.Colour(json_dict["Color"]["RawValue"])
        embed.set_image(url=json_dict["Image"]["Url"])
        embed.set_author(name=json_dict["Author"]["Name"], url=json_dict["Author"]["Url"], icon_url=json_dict["Author"]["IconUrl"])
        embed.set_footer(text=json_dict["Footer"]["Text"], icon_url=json_dict["Footer"]["IconUrl"])
        embed.set_thumbnail(url=json_dict["Thumbnail"]["Url"])
        #ToDo: Handle fields

        return embed
    