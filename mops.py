import discord
from discord.ext import commands
from TrackerClient import TrackerClient
import threading
import json
import time
import asyncio
import pymongo
import pkgutil
import sys
import inspect

class MopsClient(commands.AutoShardedBot):
    def __init__(self, config, **kwargs):
        self.config = config
        self.shards_ready = 0
        self.databaseClient = pymongo.MongoClient(config["DatabaseURL"])
        self.database = self.databaseClient["Mops"]

        self.prefixList = dict()
        for doc in self.database["GuildPrefixes"]:
            self.prefixList[doc["_id"]] = doc["Value"]

        self.loadModules()

        super(MopsClient, self).__init__(**kwargs, command_prefix=prefix)


    async def on_shard_ready(self, shard_id):
        print('Mopsbot ready shard id {0} total shards: {1} ready'.format(shard_id, self.shard_count))

        self.shards_ready += 1
        if self.shards_ready == self.shard_count:
            print("All shards ready, starting tracker client")
            tracker_client = TrackerClient(client, "127.0.0.1", 11000)
            asyncio.ensure_future(tracker_client.start_connection_loop())

    def get_prefix(self, guild):
        if guild.id in self.prefixList:
            return self.prefixList[guild.id]
        else:
            return '!'

    def insert_or_update_prefix(self, guild: discord.Guild, prefix: str):
        self.prefixList[guild.id] = prefix
        self.database["GuildPrefixes"].update_one({'_id':guild.id},{"_id": guild.id, "Value": prefix}, True)

    def loadModules(self):
        if("Modules" not in sys.modules):
            pkgutil.find_loader("Modules").load_module("Modules")
        for importer, package_name, _ in pkgutil.iter_modules(["Modules"]):
            full_package_name = '%s.%s' % ("Modules", package_name)
            if full_package_name not in sys.modules:
                    module = importer.find_module(full_package_name
                                ).load_module(full_package_name)
                    for name,obj in inspect.getmembers(module):
                        if inspect.isclass(obj):
                            if(issubclass(obj,commands.Cog)):
                                self.add_cog(obj(self))
    
def prefix(bot, message:discord.Message):
    return commands.when_mentioned_or(bot.get_prefix(message.guild()))(bot, message)

if __name__ == "__main__":
    with open("./mopsdata/Config.json", mode="r") as file:
        data = file.read()
    config = json.loads(data)

    client = MopsClient(config, fetch_offline_members=False, guild_subscriptions=False)

    client.run(config["Discord"])