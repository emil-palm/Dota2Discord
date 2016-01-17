import threading,time,datetime
from pprint import pprint
from bot.models.match import Match as Match
from bot.bot import Bot

class DotaWatch(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.client = None
        self.callback = None
        return super().__init__(*args,**kwargs)

    def run(self):
        while True:
            for k,v in iter(Bot().dota_accounts.items()):
                try:
                    match = Match.list(v.id32(), matches_requested=1, date_min=int((datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%s")))
                    if len(match) > 0:
                        match = match[0]
                        if isinstance(match,Match):
                            if match.match_id not in Bot().match_cache.keys():
                                #if (datetime.now() - match.end_time) =< 60*5:
                                    if callable(self.callback):
                                        self.callback(match)
                except Exception as e:
                    raise e
                    pass
            time.sleep(10)
