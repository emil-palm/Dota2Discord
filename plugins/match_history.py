from bot.bot import command, event, Bot
from bot.config import config,Config
from bot.models.match import Match as Match
from bot.models.result import BotResult,BotResultSchema
from util.dota_watch import DotaWatch
from discord.utils import find
from dota.api import Api as DotaApi

# Commands
@command(pattern="!g")
def last_game(client, arguments, message):
    if arguments and len(arguments) == 1:
        name = arguments[0]
        member = list(map(lambda server: find(lambda m: m.name == name, server.members), client.servers))
        if len(member) > 0 and member[0] is not None:
            player = member[0]
        elif len(message.mentions) > 0:
            player = message.mentions[0]
        else:
            client.send_message(message.channel, "Could not find %s" % (name))
    else:
        player = message.author

    if player.id not in Bot().dota_accounts.keys():
        client.send_message(message.channel, "%s not registered" % (player.name))
        return
        
    account_id = Bot().dota_accounts[player.id].id64()
    matches = Match.list(account_id)
    if not isinstance(matches,list):
        client.send_message(message.channel, matches)
        return 
    last_match = matches[0]


    if last_match.match_id not in Bot().match_cache.keys():
        client.send_typing(message.channel)
        result = BotResult.find(last_match.match_id)
        Bot().match_cache[last_match.match_id] = BotResult.schema().dump(result).data
        Bot().save_metadata()
    
    client.send_message(message.channel, Bot().renderer.render_name("match_result_short", {'result':Bot().match_cache[last_match.match_id]}))

@command(pattern="!clear")
def clear(client, arguments, message):
    if message.author.name == 'science':
        print("Clearing cache for game %s" % arguments[0])
        del(Bot().match_cache[int(arguments[0])])
        Bot().save_metadata()


# Auto watcher
_thread = None
@event("ready")
def match_watcher(**args):
    global _thread

    def watcher_callback(match):
        channels = []
        for server in set(map(lambda mention: mention.server, match.mentions())):
            channels.append(find(lambda channel: channel.name == "dotastats",server.channels))
    
        for channel in channels:
            Bot().client.send_typing(channel)
    
        result = BotResult.find(match.match_id)
        Bot().match_cache[match.match_id] = BotResult.schema().dump(result).data
        Bot().save_metadata()
        for channel in channels:
            Bot().client.send_message(channel, Bot().renderer.render_name("match_result_short", {'result':Bot().match_cache[match.match_id]}))

    if not _thread:
        _thread = DotaWatch()
        _thread.client = Bot().client
        _thread.callback = watcher_callback
        _thread.setDaemon(True)
        _thread.start()
        print("Setting up dota game watcher")
 
# Bootstrapping
def bootstrap():
    DotaApi(Config().steam.apikey)
    if not hasattr(Bot(),"match_cache"):
        Bot().metadata['match_cache'] = {}

@config(prefix="steam",cb=bootstrap,override=True)
def _config():
    return {"apikey":None}


