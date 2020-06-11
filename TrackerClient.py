import discord
import socket
import json
import time
import typing
from typing import *
from Utils.Trackers import case_sensitive_types
import asyncio
from dateutil import parser

class TrackerClient:
    def __init__(self, bot, ip: str, port: int):
        self.HOST = '127.0.0.1'
        self.PORT = 11000
        self.server: socket = None
        self.bot = bot
        self.connected = False
        self.ticket_id = 0
        self.waiting_for_ack: Dict[int, TrackerMessage] = dict()

    async def resend_ack_loop(self):
        while True:
            try:
                for key, value in list(self.waiting_for_ack.items()):
                    seconds_since = time.time() - value.time
                    ticket: TrackerMessage = value

                    #Server took over 10 minutes, remove ticket
                    if seconds_since >= 600:
                        ticket = self.waiting_for_ack.pop(key)
                        if ticket.function != None:
                            await ticket.function(TrackerMessage(-1, "Server did not respond, please try again later."), ticket.callback_args)
                    #Resend ticket
                    elif seconds_since >= 60:
                        if ticket.function != None:
                            await ticket.function(TrackerMessage(-1, f"Server did not respond, trying again in a minute. ({int(seconds_since / 60)}/10)"), ticket.callback_args)
                        await self.send_ticket(value)
            except Exception as e:
                print(e)

            await asyncio.sleep(60)

    async def send_message(self, message: str, wait_for_ack: bool = False, execute_after_ack: callable = None, callback_args = None):
        ticket = TrackerMessage(self.ticket_id, message, execute_after_ack, callback_args)
        self.ticket_id += 1

        if wait_for_ack:
            self.waiting_for_ack[ticket.id] = ticket

        await self.send_ticket(ticket)

    async def send_ticket(self, ticket: 'TrackerMessage'):
        if self.connected:
            self.server.send(ticket.full_encoded_message)
        else:
            if ticket.function != None:
                await ticket.function(TrackerMessage(-1, f"Server is offline, trying again in a minute."), ticket.callback_args)

    async def received_message(self, message: 'TrackerMessage'):
        try:
            print("data received: {0}".format(message.content))

            if message.is_ack:
                if message.ack_id in self.waiting_for_ack:
                    ticket = self.waiting_for_ack.pop(message.ack_id)
                    if ticket.function != None:
                        await ticket.function(message, ticket.callback_args)

                return

            await self.send_message(f"ACKNOWLEDGED REQUEST {message.id}")
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
                    self.server.setblocking(False)
                    self.connected = True
                    data: str = ""
                    while True:
                        try:
                            data += self.server.recv(8192).decode()
                        except BlockingIOError as e:
                            await asyncio.sleep(1)
                            continue
                        data, message_list = self.find_messages(data)
                        for message in message_list:
                            await self.received_message(message)
                except Exception as e:
                    self.connected = False
                    print(e)
                    print("Connection was interrupted, trying again in 10 seconds.")
                    await asyncio.sleep(10)

    def dnet_embed_to_py(self, json_dict) -> discord.Embed:
        embed = discord.Embed()
        if "Title" in json_dict:
            embed.title = json_dict["Title"]
        if "Description" in json_dict:
            embed.description = json_dict["Description"]
        if "Url" in json_dict:
            embed.url = json_dict["Url"]
        if "Timestamp" in json_dict:
            embed.timestamp = parser.parse(json_dict["Timestamp"])
        if "Color" in json_dict:
            embed.colour = discord.colour.Colour(json_dict["Color"]["RawValue"])
        if "Image" in json_dict:
            embed.set_image(url=json_dict["Image"]["Url"])
        if "Author" in json_dict:
            embed.set_author(name=json_dict["Author"]["Name"], url=json_dict["Author"]["Url"], icon_url=json_dict["Author"]["IconUrl"])
        if "Footer" in json_dict:
            embed.set_footer(text=json_dict["Footer"]["Text"], icon_url=json_dict["Footer"]["IconUrl"])
        if "Thumbnail" in json_dict:
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
    def __init__(self, id: int, data: str, execute_after_ack: Callable[['TrackerMessage'], Any] = None, callback_args = None):
        self.id = id
        self.content = data
        self.embed = None
        self.time = time.time()
        self.function = execute_after_ack
        self.callback_args = callback_args
        self.is_ack = "ACKNOWLEDGED REQUEST " in self.content
        self.full_message = f"STARTEVENT {self.id}\n{self.content}\nENDEVENT {self.id}"
        self.full_encoded_message = str.encode(self.full_message)
    
        if self.is_ack:
            self.ack_id = int(self.content.split("ACKNOWLEDGED REQUEST ")[1].split("\n")[0])
            self.content = self.content.split(f"ACKNOWLEDGED REQUEST {self.ack_id}\n")[-1]