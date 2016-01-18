from bot.config import JSONConfig,Config,config
from bot.bot import Bot

import plugins.steam
import plugins.match_history
import plugins.stats

Config(cls=JSONConfig,filename="evilbot.json")
bot = Bot()
try:
    bot.client.run()
except Exception:
    pass
