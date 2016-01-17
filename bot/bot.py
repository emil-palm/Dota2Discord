import shlex,os,pickle
from util.discord import discord
from bot.config import config,Config
from pystache import Renderer

_bot_instance = None

def command(pattern):
    def wrap(function):
        _Bot.command(function, pattern)
    return wrap

def event(eventname):
    def wrap(function):
        _Bot.event(function, eventname)
    return wrap

def Bot(client=None):
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = _Bot()

    if client:
        _bot_instance.client = client
    
    return _bot_instance


class _Bot(object):
    commands = {}
    eventhandlers = {}

    def __init__(self):
        self.client = discord(self.config.discord_username,self.config.discord_password)
        self.renderer = Renderer(search_dirs=self.config.template_folders,file_extension="stash",escape=lambda u: u)

    # Bot metadata, this can be used for plugins who want to save state.
    # Its accessible through "bot.metadata['KEY']" or bot.KEY, eg: bot.steam.apikey

    @property
    def metadata(self):
        if "metadata" not in self.__dict__.keys():
            self.__dict__['metadata'] = {}

        return self.__dict__['metadata']

    def __getattr__(self,key):
        try:
           _attr = super().__getattribute__(key)
           return _attr
        except Exception as e:
            if key in self.metadata.keys():
                return self.metadata[key]
            else:
                raise e

    # Load pickled meta data
    def load_metadata(self):
        if os.path.isfile(Config().bot.metacache_data_file):
            try:
                with open(Config().bot.metacache_data_file, "rb") as input_file:
                    _data = pickle.load(input_file)
                    for k,v in _data.items():
                        self.metadata[k] = v
            except Exception as e :
                pass

    def save_metadata(self):
        with open(Config().bot.metacache_data_file, "wb") as output_file:
            pickle.dump(self.metadata, output_file)
 
        
    # Basic property for client
    @property
    def client(self):
        return self._client

    # Magic setter that will setup the event listener.
    @client.setter
    def client(self,client):
        self._client = client
        self.load_metadata()
        # This will handle all the incomming messages and handle the issue 
        @client.event
        def on_message(message):
            # Ignore own messages
            if message.author.id == self.client.user.id:
                return
                
            message_parts = shlex.split(message.content, 1)
            cmd,arguments = None,None
            if len(message_parts) == 1:
                (cmd) = message_parts[0]
            else:
                (cmd,arguments) = (message_parts[0], message_parts[1:])

            if cmd in self.__class__.commands.keys():
                for function in self.__class__.commands[cmd]:
                    function(client, arguments,message)

        @client.event
        def on_ready():
            self.send_event("ready")
    
    def send_event(self, event, **args):
        if event in self.__class__.eventhandlers.keys():
            for event_handler in self.__class__.eventhandlers[event]:
                event_handler(**args)

    @classmethod
    def event(cls, function, eventname):
        if eventname not in cls.eventhandlers.keys():
            cls.eventhandlers[eventname] = []
        
        cls.eventhandlers[eventname].append(function)
        
            
    @classmethod
    def command(cls, function, pattern):
        if not pattern:
            raise ArgumentError("Pattern cannot be none")
        
        if pattern not in cls.commands.keys():
            cls.commands[pattern] = []
        
        cls.commands[pattern].append(function)

#@config(prefix="discord",cls=_Bot)
#def _config():
#    return {"username":None,"password":None}

@config(prefix="bot",cls=_Bot)
def _config():
    return {
                "metacache_data_file": "bot.cache", 
                "discord_username" : None, 
                "discord_password": None,
                "template_folders": ["templates/"],
                "admins":[]
    } 


