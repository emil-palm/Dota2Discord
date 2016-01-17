from marshmallow import fields, pre_load
from dota.model import Model
from dota.schema import Schema
from dota.player import PlayerSchema
from dota.api import Api
from pprint import pprint
import datetime

class Match(Model):
    def __init__(self, *args, **kwargs):
        self._dire_team = None
        self._radiant_team = None
        super(Match,self).__init__(*args,**kwargs)

    def radiant_team(self):
        if self._radiant_team is None:
            self._split_teams()

        return self._radiant_team

    def dire_team(self):
        if self._dire_team is None:
            self._split_teams()
        return self._dire_team

    def _split_teams(self):
        self._radiant_team = []
        self._dire_team = []
        for player in self.players:
            if player.team == "radiant":
                self._radiant_team.append(player)
            else:
                self._dire_team.append(player)
    
    @classmethod
    def list(cls,*args,**kwargs):
        kwargs['account_id'] = args[0]
        if 'matches_requested' not in kwargs:
            kwargs['matches_requested'] = 5

        _data = Api().get_match_history(**kwargs)
        if _data['result']['status'] == 1:
            (errors,data) = cls.schema().load(_data,many=True)
            if errors:
                return errors
            else:
                return data
        else:
            return _data['result']['statusDetail']

    @classmethod
    def find(cls,match_id):
        return cls(match_id=match_id).load()


class MatchSchema(Schema):
    dire_team_id = fields.Integer()
    lobby_type = fields.Method("set_lobby_type")
    match_id = fields.Integer()
    match_seq_num = fields.Integer()
    players = fields.Nested(PlayerSchema, many=True)
    radiant_team_id = fields.Integer()
    start_time = fields.Function(lambda obj: datetime.datetime.fromtimestamp(int(obj.get('start_time'))).isoformat())
    end_time = fields.Function(lambda obj: (datetime.datetime.fromtimestamp(int(obj.get('start_time'))) + datetime.timedelta(seconds=obj.get('duration'))).isoformat(),dump_only=True)


    @pre_load(pass_many=True)
    def remove_matches_env(self, data, many):
        if data.get("matches"):
            return data.get("matches")
        else:
            return data

    def set_loby_type(self, obj):
        _type = obj.get('lobby_type')
        if _type == -1:
            return "invalid"
        elif _type == 0:
            return "public match making"
        elif _type == 1:
            return "practice"
        elif _type == 2:
            return "tournament"
        elif _type == 3:
            return "tutorial"
        elif _type == 4:
            return "co-op with bots"
        elif _type == 5:
            return "team match-making"
        elif _type == 6:
            return "solo queue"


