import discord
import socket
import json
import time
import typing
from typing import List
from typing import Tuple
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

    async def received_message(self, message: 'TrackerMessage'):
        try:
            print("data recieved: {0}".format(message.content))
            eventMessage = json.loads(message.content)

            if "ChannelId" in eventMessage:
                channel = self.bot.get_channel(eventMessage["ChannelId"])
                embed = self.dnet_embed_to_py(eventMessage["Embed"])

                await channel.send(eventMessage["Notification"], embed=embed)

            else:
                print("Didn't know what to do")

        except:
            pass

    async def start_connection_loop(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    self.server = s
                    self.server.connect((self.HOST, self.PORT))
                    data: str = ""
                    while True:
                            data += self.server.recv(8192).decode()
                            data, message_list = self.find_messages(data)
                            for message in message_list:
                                await self.received_message(message)
                                await self.send_message(f"ACK {message.id}")
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
    
    def find_messages(self, data: str) -> Tuple[str, List['TrackerMessage']]:
        messages = []
        while True:
            start_index_a = data.find("STARTEVENT")
            start_index_b = data[start_index_a:].find("\n")
            if start_index_a >= 0 and start_index_b > 0:
                event_id = int(data[start_index_a + 11 : start_index_b])
                end_index = data.find("ENDEVENT " + str(event_id))
                if end_index >= 0:
                    messages.append(TrackerMessage(event_id, data[start_index_b + 1 : end_index - 1]))
                    data = data[end_index + len("ENDEVENT " + str(event_id)):]
                    continue

            return data, messages
                

class TrackerMessage:
    def __init__(self, id: int, data: str):
        self.id = id
        self.content = data