from discord.ext import commands
import pkgutil
import sys
import inspect
import typing

class commandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loadModules()

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


    
