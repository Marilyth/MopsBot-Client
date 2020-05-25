#from mops import MopsClient
from enum import Enum, auto
from typing import *

tracker_types = ["Twitch",
    "TwitchGroup",
    "TwitchClip",
    "Mixer",
    "Twitter",
    "Youtube",
    "YoutubeLive",
    "Reddit",
    "Steam",
    "Osu",
    "Overwatch",
    "OSRS",
    "JSON",
    "HTML",
    "RSS"]

case_sensitive_types = ["Youtube",
    "YoutubeLive",
    "Reddit",
    "Overwatch",
    "JSON",
    "HTML",
    "RSS"]

class Trackers:
    def __init__(self, bot):
        self.trackers = dict()
        self.bot = bot
        for name in tracker_types:
            self.trackers[name] = dict()

            for doc in self.bot.database[name + "Tracker"].find():
                self.trackers[name][doc["_id"]] = doc

    def __getitem__(self, item):
        return self.trackers[item]
        
    async def add(self, type: str, name: str, channel_id: int, notification: str, callback = None, callback_args = None):
        if type not in case_sensitive_types:
            name = name.lower()
        await self.bot.tracker_client.send_message(f"ADD|||{type}|||{channel_id}|||{name}|||{notification}", wait_for_ack=True, execute_after_ack=callback, callback_args = callback_args)

    async def set_notification(self, type: str, name: str, channel_id: int, callback = None):
        await self.bot.tracker_client.send_message(f"SETNOTIFICATION|||{type}|||{channel_id}|||{name}", wait_for_ack=True, execute_after_ack=callback)

    async def remove(self, type: str, name: str, channel_id: int, callback = None):
        await self.bot.tracker_client.send_message(f"REMOVE|||{type}|||{channel_id}|||{name}", wait_for_ack=True, execute_after_ack=callback)

    async def change_config(self, type: str, name: str, channel_id: int, config: Dict[str, object], callback = None):
        await self.bot.tracker_client.send_message(f"CHANGECONFIG|||{type}|||{channel_id}|||{name}|||{config}", wait_for_ack=True, execute_after_ack=callback)

    async def change_channel(self, type: str, name: str, from_channel_id: int, to_channel_id: int, callback = None):
        await self.bot.tracker_client.send_message(f"CHANGECHANNEL|||{type}|||{from_channel_id}|||{name}|||{to_channel_id}", wait_for_ack=True, execute_after_ack=callback)