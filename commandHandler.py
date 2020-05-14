import discord
from discord.ext import commands
import pkgutil
import sys
import inspect
import typing

class commandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixList = dict()
        for doc in self.bot.database["GuildPrefixes"].find():
            self.prefixList[doc["_id"]] = doc["Value"]
        
        bot.command_prefix = prefix
        self.loadModules()

    def get_prefix(self, guild):
        if guild.id in self.prefixList:
            return self.prefixList[guild.id]
        else:
            return '!'

    def insert_or_update_prefix(self, guild: discord.Guild, prefix: str):
        self.prefixList[guild.id] = prefix
        self.bot.database["GuildPrefixes"].update_one({'_id':guild.id},{"_id": guild.id, "Value": prefix}, True)


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
                                self.bot.add_cog(obj(self.bot))

def prefix(bot, message):
    return commands.when_mentioned_or(bot.commandHandler.get_prefix(message.guild))(bot, message)
