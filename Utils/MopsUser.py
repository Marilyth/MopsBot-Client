from __future__ import annotations

import discord
import typing
import mops
from typing import *
import math
import json
import discord

class MopsUser:
    def __init__(self, data: Dict[str, int]):
        self._id = data["_id"]
        self.Money = data["Money"]
        self.Experience = data["Experience"]
        self.CharactersSent = data["CharactersSent"]
        self.Punched = data["Punched"]
        self.Hugged = data["Hugged"]
        self.Kissed = data["Kissed"]

    @staticmethod
    async def get_user(bot: mops.MopsClient, user_id: int) -> MopsUser:
        user = bot.database["Users"].find_one({"_id": user_id})
        if user is None:
            user = {
                "_id": user_id,
                "Money": 0,
                "Experience": 0,
                "CharactersSent": 0,
                "Punched": 0,
                "Hugged": 0,
                "Kissed": 0
            }
            bot.database["Users"].insert_one(user)

        return MopsUser(user)

    @staticmethod
    async def modify_user(bot: mops.MopsClient, user: 'MopsUser', action: Callable[['MopsUser'], Any]):
        action(user)
        bot.database["Users"].replace_one({"_id": user._id}, user.__dict__)

    
        

