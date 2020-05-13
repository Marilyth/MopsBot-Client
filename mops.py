import discord
import commandHandler
from trackerHandler import startTrackerHandler
import threading
import json

class MopsClient(discord.AutoShardedClient):
    def __init__(self, **kwargs):
        self.messageHandler = []
        self.reactionHandler = []
        super(MopsClient, self).__init__(**kwargs)

    def addMessageHandler(self, handler):
        self.messageHandler.append(handler)
    
    def addReactionHandler(self, handler):
        self.reactionHandler.append(handler)

    async def on_shard_ready(self, shard_id):
        print('Mopsbot ready shard id {0} total shards: {1} ready'.format(shard_id, self.shard_count))

    async def on_message(self, message):
        for handler in self.messageHandler:
            await handler.on_message(self,message)

    async def on_reaction_add(self, reaction, user):
        for handler in self.messageHandler:
            await handler.on_reaction_add(self, reaction, user)
    
    async def on_reaction_remove(self, reaction, user):
        for handler in self.messageHandler:
            await handler.on_reaction_remove(self, reaction, user)

with open("./mopsdata/Config.json", mode="r") as file:
    data = file.read()
config = json.loads(data)

client = MopsClient(fetch_offline_members=False, guild_subscriptions=False)
client.addMessageHandler(commandHandler.commandHandler())

trackerHandlerThread = threading.Thread(target = startTrackerHandler)
trackerHandlerThread.start()

client.run(config["Discord"])