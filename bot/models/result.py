from marshmallow import fields
from dota.result import DotaResultSchema
from dota.result import DotaResult
from dota.schema import Schema
from discord.utils import find
from bot.bot import Bot
from .player import PlayerSchema

class BotResult(DotaResult):

    def mentions(self):
        mentions = []
        for player in self.players:
            for k,v in Bot().dota_accounts.items():
                if player.account_id == v.id32():
                    mentions.append(list(map(lambda server: find(lambda m: m.id == k, server.members), self.discord.servers))[0])

        return mentions

    def outcome(self):
        discord_members_dire = list(filter(lambda player: player.is_discord_member(), self.dire_team()))
        discord_members_radiant = list(filter(lambda player: player.is_discord_member(), self.radiant_team()))
        discord_dire_mentions = ",".join(list(map(lambda member: member.is_discord_member().mention(), discord_members_dire)))
        discord_radiant_mentions = ",".join(list(map(lambda member: member.is_discord_member().mention(), discord_members_radiant)))


        if len(discord_members_radiant) > len(discord_members_dire):
            result = None
            if self.radiant_win:
                result = "won"
            else:
                result = "lost"
            return "Radient %s (%s)" % (result, discord_radiant_mentions)

        elif len(discord_members_radiant) < len(discord_members_dire):
            result = None
            if self.radiant_win:
                result = "lost"
            else:
                result = "won"
            return "Dire %s (%s)" % (result, discord_dire_mentions)

        else:
            team = None
            winners = None
            loosers = None
            if self.radiant_win == True:
                team = "Radient"
                loosers = discord_radiant_mentions
            else:
                team = "Dire won"
                winners = discord_dire_mentions

            return "%s (%s) won vs %s" % (team,winners,loosers)
    
    def mvp(self):
        team = None
        if self.radiant_win:
            team = self.radiant_team()
        else:
            team = self.dire_team()

        return sorted(team, key=lambda player: player.impact(),reverse=True)[0]

        
            

class BotResultSchema(DotaResultSchema):
    players = fields.Nested(PlayerSchema, many=True)
    mentions = fields.List(fields.String(),dump_only=True)
    radiant_team = fields.Nested(PlayerSchema,many=True,dump_only=True)
    dire_team = fields.Nested(PlayerSchema,many=True,dump_only=True)
    outcome = fields.String(dump_only=True)
    mvp = fields.Nested(PlayerSchema,many=False,dump_only=True)
