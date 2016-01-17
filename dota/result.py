from marshmallow import fields, pprint, pre_load
from dota.model import Model
from dota.schema import Schema
from dota.player import PlayerSchema
from dota.api import Api
import datetime

class DotaResult(Model):
    def __init__(self, *args, **kwargs):
        _me = super().__init__(*args,**kwargs)
        self._dire_team = None
        self._radiant_team = None
        return _me

    @classmethod
    def find(cls,match_id):
        return cls.schema().load(Api().get_match_details(match_id))[0]
    
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

    @property
    def game_mode(self):
        _gm = self._game_mode
        if _gm == 0:
            return "None"
        elif _gm == 1:
            return "All Pick"
        elif _gm == 2:
            return "Captain's Mode"
        elif _gm == 3:
            return "Random Draft"
        elif _gm == 4:
            return "Single Draft"
        elif _gm == 5:
            return "All Random"
        elif _gm == 6:
            return "Intro"
        elif _gm == 7:
            return "Diretide"
        elif _gm == 8:
            return "Reverse Captain's Mode"
        elif _gm == 9:
            return "The Greevliling"
        elif _gm == 10:
            return "Tutorial"
        elif _gm == 11:
            return "Mid Only"
        elif _gm == 12:
            return "Least Played"
        elif _gm == 13:
            return "New Player Pool"
        elif _gm == 14:
            return "Compendium Matchmaking"
        elif _gm == 15:
            return "Custom"
        elif _gm == 16:
            return "Captain's Draft"
        elif _gm == 17:
            return "Balanced Draft"
        elif _gm == 18:
            return "Ability Draft"
        elif _gm == 19:
            return "?? EVENT ??"
        elif _gm == 20:
            return "All Random Death Match"
        elif _gm == 21:
            return "1 vs 1 Solo Mid"
        elif _gm == 22:
            return "All Pick"
        else:
            return "Unknown"
    @property
    def lobby_type(self):
        _type = self._lobby_type
        if _type == -1:
            return "invalid"
        elif _type == 0:
            return "Public Match Making"
        elif _type == 1:
            return "Practice"
        elif _type == 2:
            return "Tournament"
        elif _type == 3:
            return "Tutorial"
        elif _type == 4:
            return "CO-OP with bots"
        elif _type == 5:
            return "Team Match Making"
        elif _type == 6:
            return "Solo Queue"
        elif _type == 7:
            return "Ranked"
        elif _type == 8:
            return "Solo Mid 1 vs 1"
        else:
            return "Unknown"

 
   
class DotaResultSchema(Schema):
    barracks_status_dire = fields.Integer()
    barracks_status_radiant = fields.Integer()
    cluster = fields.Integer()
    duration = fields.Integer()
    engine = fields.Integer()
    first_blood_time = fields.Integer()

    human_players = fields.Integer()
    leagueid = fields.Integer()

    match_id = fields.Integer()
    match_seq_num = fields.Integer()
    negative_votes = fields.Integer()
    players = fields.Nested(PlayerSchema, many=True)
    positive_votes = fields.Integer()
    radiant_win = fields.Boolean()
    start_time = fields.Function(lambda obj: datetime.datetime.fromtimestamp(int(obj.get('start_time'))).isoformat())
    end_time = fields.Function(lambda obj: (datetime.datetime.fromtimestamp(int(obj.get('start_time'))) + datetime.timedelta(seconds=obj.get('duration'))).isoformat(),dump_only=True)
    tower_status_dire = fields.Integer()
    tower_status_radiant = fields.Integer()


    lobby_type = fields.String(dump_only=True)
    _lobby_type = fields.Integer(load_only=True,load_from='lobby_type')

    _game_mode = fields.Integer(load_only=True,load_from='game_mode')
    game_mode = fields.String(dump_only=True)
    


    @pre_load
    def _test(self, obj, many=None):
        from pprint import pprint
        #pprint(obj)
        return obj


