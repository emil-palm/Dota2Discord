from marshmallow import post_load,fields
from dota.player import PlayerSchema as DotaPlayerSchema
from dota.player import Player as DotaPlayer
from util.discord import discord as _discord
from discord.utils import find
from bot.bot import Bot
import util.dotabuff

class Player(DotaPlayer):
    def player_name(self):
        member = self.is_discord_member()
        dbuff_name = util.dotabuff.get_username_from_uid(self.account_id)
        if dbuff_name:
            return (member.mention() if member else False,dbuff_name)
            
        return (False,"Anonymous")

    def is_discord_member(self):
        if self.account_id != 4294967295:
            for k,v in Bot().dota_accounts.items():
                if self.account_id == v.id32():
                    member = list(map(lambda server: find(lambda m: m.id == k, server.members), self.discord.servers))
                    if len(member) > 0:
                        return member[0]
        
        return False

    def impact(self):
        return (self.tower_damage + 
                self.hero_damage + 
                self.hero_healing + 
                self.gold_spent + 
                self.last_hits + 
                self.denies +
                self.level +
                self.kills -
                self.deaths +
                self.assists) if self.leaver_status == 0 else 0

        




class PlayerSchema(DotaPlayerSchema):
    player_name = fields.Function(lambda player: player.player_name()[1], dump_only=True)
    is_discord = fields.Function(lambda player: True if player.is_discord_member() else False, dump_only=True)
    discord_mention = fields.Function(lambda player: player.player_name()[0] if player.is_discord_member() else False, dump_only=True)
    impact = fields.Integer()
