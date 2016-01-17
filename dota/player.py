from marshmallow import fields, pprint
from datetime import datetime
from dota.model import Model
from dota.schema import Schema
from dota.hero import Hero,HeroSchema
from bitstring import BitArray

_heroes = None
def heroes():
    global _heroes
    if _heroes is None:
        _heroes = {}
        for hero in Hero.list():
            _heroes[hero.id] = hero

    return _heroes


class Player(Model):
    @property
    def team(self):
        c = BitArray()
        c.append("uint:8=%s" % self.player_slot)
        if c[0] == 0:
            return "radiant"
        else:
            return "dire"
    @property
    def position(self):
        c = BitArray()
        c.append("uint:8=%s" % self.player_slot)
        return ((c[4:8].int)+1)

    @property
    def hero(self):
        return heroes()[self.hero_id]

class PlayerSchema(Schema):
    account_id = fields.Integer()

    assists = fields.Integer()
    deaths = fields.Integer()
    kills = fields.Integer()

    denies = fields.Integer()
    last_hits = fields.Integer()
    leaver_status = fields.Integer()

    player_slot = fields.Integer()
    team = fields.String(dump_only=True)
    position = fields.Integer(dump_only=True)

    gold = fields.Integer()
    gold_per_mind = fields.Integer()
    gold_spent = fields.Integer()

    tower_damage = fields.Integer()
    level = fields.Integer()
    xp_per_min = fields.Integer()

    hero_damage = fields.Integer()
    hero_healing = fields.Integer()
    hero_id = fields.Integer()
    hero = fields.Nested(HeroSchema)

    item_0 = fields.Integer()
    item_1 = fields.Integer()
    item_2 = fields.Integer()
    item_3 = fields.Integer()
    item_4 = fields.Integer()
    item_5 = fields.Integer()

