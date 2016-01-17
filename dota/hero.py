from marshmallow import fields, post_load, pre_load
from dota.model import Model
from dota.schema import Schema
from dota.api import Api


class Hero(Model):
    @classmethod
    def list(cls):
        (data,errors) = cls.schema().load(Api().get_heroes(), many=True)
        return data

class HeroSchema(Schema):
    name = fields.String()
    id = fields.Integer()
    localized_name = fields.String()

    @pre_load(pass_many=True)
    def remove_hero_env(self, data, many=None):
        if many and isinstance(data,list):
            return data
        else:
            if data.get("heroes"):
                return data.get("heroes")
            else:
                return data
