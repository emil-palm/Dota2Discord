from bot.bot import Bot,command
from bot.config import config
from bot.models.result import BotResultSchema
from collections import OrderedDict
import operator

#from dota.hero import Hero

@command(pattern="!top5")
def top5(client,argument,message):
    if len(argument) > 0:
        _type = argument[0]
        toplist = {}
        for match in BotResultSchema().load(list(Bot().match_cache.values()),many=True).data:
            if _type == "hero":
                for player in match.players:
                    if player.is_discord_member():
                        if player.hero.localized_name not in toplist.keys():
                            toplist[player.hero.localized_name] = 0

                        toplist[player.hero.localized_name] += 1
            if _type == "player":
                for player in match.players:
                    discord_member = player.is_discord_member()
                    if discord_member:
                        if discord_member.name not in toplist.keys():
                            toplist[discord_member.name] = 0

                        toplist[discord_member.name] += 1

        if _type == "hero":
            index=0
            def _objectify(tu):
                nonlocal index
                index += 1
                return {'name':tu[0], 'count':tu[1], 'index':index} 

            sorted_toplist = sorted(toplist.items(), key=operator.itemgetter(1), reverse=True)
            results = list(map(_objectify, sorted_toplist))
            client.send_message(message.channel,Bot().renderer.render_name("top_list_hero", results[:5]))
        if _type == "player":
            index=0
            def _objectify(tu):
                nonlocal index
                index += 1
                return {'name':tu[0], 'count':tu[1], 'index':index} 

            sorted_toplist = sorted(toplist.items(), key=operator.itemgetter(1), reverse=True)
            results = list(map(_objectify, sorted_toplist))
            client.send_message(message.channel,Bot().renderer.render_name("top_list_player", results[:5]))
