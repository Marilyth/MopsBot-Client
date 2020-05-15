import discord
from discord.ext import commands
from TrackerClient import TrackerClient
from commandHandler import commandHandler
from ReactionHandler import ReactionHandler
import threading
import json
import time
import asyncio
import pymongo
import pkgutil
import sys
import inspect
import time
startTime = time.time()

class MopsClient(commands.AutoShardedBot):
    def __init__(self, config, **kwargs):
        super(MopsClient, self).__init__(**kwargs, command_prefix="!")
        self.config = config
        self.shards_ready = 0
        self.databaseClient = pymongo.MongoClient(config["DatabaseURL"])
        self.database = self.databaseClient["Mops"]
        self.commandHandler = commandHandler(self)
        self.reactionHandler: ReactionHandler = ReactionHandler(self)
        self.add_cog(self.commandHandler)
        self.add_cog(self.reactionHandler)

    async def on_shard_ready(self, shard_id):
        print('Mopsbot ready shard id {0} total shards: {1} ready'.format(shard_id, self.shard_count))

        self.shards_ready += 1
        if self.shards_ready == self.shard_count:
            print("All shards ready, starting tracker client")
            tracker_client = TrackerClient(client, "127.0.0.1", 11000)
            asyncio.ensure_future(tracker_client.start_connection_loop())


if __name__ == "__main__":
    with open("./mopsdata/Config.json", mode="r") as file:
        data = file.read()
    config = json.loads(data)

    client = MopsClient(config, fetch_offline_members=False, guild_subscriptions=False)


    client.run(config["Discord"])