from marshmallow import fields
from dota.match import MatchSchema as DotaMatchSchema
from dota.match import Match as DotaMatch
from util.discord import discord
from discord.utils import find
from bot.bot import Bot
from .player import PlayerSchema

class Match(DotaMatch):
    def mentions(self):
        mentions = []
        for player in self.players:
            for k,v in Bot().dota_accounts.items():
                if player.account_id == v.id32():
                    mentions.append(list(map(lambda server: find(lambda m: m.id == k, server.members), self.discord.servers))[0])

        return mentions


    pass
    

class MatchSchema(DotaMatchSchema):
    players = fields.Nested(PlayerSchema, many=True)



