from bot.bot import command, Bot
from bot.config import config,Config
from bot.models.match import Match as Match
from bot.models.result import BotResult,BotResultSchema
from util.steamid import Steamid
from dota.api import Api as DotaApi

# Private methods
def _register(client,message,disc_user,account):
    steamid = None
    if len(account) == 17:
        # We have a 64bit steamid already lets use it
        steamid = Steamid(steamid=account,success=1)
    else:
        steamid = Steamid(**DotaApi().get_steam_id(account).get('response'))

    if steamid.success == 1:
        client.send_message(message.channel, "Registered %s to %s" % (account, disc_user.mention()))
        Bot().dota_accounts[disc_user.id] = steamid
        Bot().save_metadata()
    else:
        client.send_message(message.channel, "Could not find %s" % (account))

# Commands
@command(pattern="!register")
def register(client, arguments, message):
    if len(arguments) != 1:
        client.send_message(message.channel, 'Invalid amount of arguments; !register STEAMACCOUNTNAME')
        return

    if arguments[0] in Bot().dota_accounts:
        client.send_message(message.channel, 'Account already registered')
        return

    _register(client,message,message.author,arguments[0])

@command(pattern="!ninja")
def ninja(client, arguments, message):
    (disc, steam) = arguments
    if disc and steam:
        member = list(map(lambda server: find(lambda m: m.name == disc, server.members), client.servers))
        player = None
        if len(member) > 0 and member[0] is not None:
            player = member[0]
        elif len(message.mentions) > 0:
            player = message.mentions[0]
        else:
            client.send_message(message.channel, "Could not find %s" % (disc))
    
        _register(client,message,player,steam)

@command(pattern="!unregister")
def unregister(client,arguments,message):
    if message.author.id in Bot().dota_accounts:
        del(Bot().dota_accounts[message.author.id])
        Bot().save_metadata()
        client.send_message(message.channel, "Unregistered %s" % message.author.mention())
    else:
        client.send_message(message.channel, "Couldnt find a registered user for your account %s" % message.author.mention())


# Bootstrapping
def bootstrap():
    DotaApi(Config().steam.apikey)
    if not hasattr(Bot(),"dota_accounts"):
        Bot().metadata['dota_accounts'] = {}

@config(prefix="steam",cb=bootstrap)
def _config():
    return {"apikey":None}


