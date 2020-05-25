#from mops import MopsClient
from enum import Enum, auto

class TrackerType(Enum):
    Twitch = auto()
    TwitchGroup = auto()
    TwitchClip = auto()
    Mixer = auto()
    Twitter = auto()
    Youtube = auto()
    YoutubeLive = auto()
    Reddit = auto()
    Steam = auto()
    Osu = auto()
    Overwatch = auto()
    OSRS = auto()
    JSON = auto()
    HTML = auto()
    RSS = auto()

class Trackers:
    def __init__(self, bot):
        self.trackers = dict()
        self.bot = bot
        for name, member in TrackerType.__members__.items():
            self.trackers[name] = dict()

            for doc in self.bot.database[name + "Tracker"].find():
                self.trackers[name][doc["_id"]] = doc

    def __getitem__(self, item):
        return self.trackers[item]
        