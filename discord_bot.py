from bot.config import JSONConfig,Config,config
from bot.bot import Bot

import plugins.steam
import plugins.match_history

Config(cls=JSONConfig,filename="evilbot.json")
bot = Bot()
bot.client.run()
