import discord
import commandHandler
from TrackerClient import TrackerClient
import threading
import json
import time
import asyncio

class MopsClient(discord.AutoShardedClient):
    def __init__(self, config, **kwargs):
        self.messageHandler = []
        self.reactionHandler = []
        self.config = config
        self.shards_ready = 0
        super(MopsClient, self).__init__(**kwargs)

    def addMessageHandler(self, handler):
        self.messageHandler.append(handler)
    
    def addReactionHandler(self, handler):
        self.reactionHandler.append(handler)

    async def on_shard_ready(self, shard_id):
        print('Mopsbot ready shard id {0} total shards: {1} ready'.format(shard_id, self.shard_count))

        self.shards_ready += 1
        if self.shards_ready == self.shard_count:
            print("All shards ready, starting tracker client")
            tracker_client = TrackerClient(client, "127.0.0.1", 11000)
            asyncio.ensure_future(tracker_client.start_connection_loop())

    async def on_message(self, message):
        for handler in self.messageHandler:
            await handler.on_message(self,message)

    async def on_reaction_add(self, reaction, user):
        for handler in self.messageHandler:
            await handler.on_reaction_add(self, reaction, user)
    
    async def on_reaction_remove(self, reaction, user):
        for handler in self.messageHandler:
            await handler.on_reaction_remove(self, reaction, user)


if __name__ == "__main__":
    with open("./mopsdata/Config.json", mode="r") as file:
        data = file.read()
    config = json.loads(data)

    client = MopsClient(config, fetch_offline_members=False, guild_subscriptions=False)
    client.addMessageHandler(commandHandler.commandHandler())

    client.run(config["Discord"])