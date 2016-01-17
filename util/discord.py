import discord as _dis
_discord = None
from pprint import pprint
from dota.model import Model
from dota.player import Player as DotaPlayer

def property_discord(self):
    return discord()

setattr(Model, 'discord', property(property_discord))

class __Discord(_dis.Client):

    @property
    def metadata(self):
        if "metadata" not in self.__dict__.keys():
            self.__dict__['metadata'] = {}

        return self.__dict__['metadata']

    def __getattr__(self,key):
        try:
           _attr = super().__getattr__(key)
           return _attr
        except Exception as e:
            if key in self.metadata.keys():
                return self.metadata[key]
            else:
                raise e

def discord(username=None,password=None):
    global _discord
    if _discord is None and (username is not None and password is not None):
        _discord = __Discord()
        _discord.login(username,password)

    return _discord


