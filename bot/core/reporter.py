from time import sleep
from pyrogram.errors import FloodWait
from bot import Var, LOGS, bot

class Reporter:
    def __init__(self, client, chat_id, log):
        self.__client = client
        self.__cid = chat_id
        self.__logger = log

    async def report(self, msg, log_type, log=True):
        txt = [f"[{log_type.upper()}] {msg}", log_type.lower()]
        if txt[1] == "error":
            self.__logger.error(txt[0])
        elif txt[1] == "warning":
            self.__logger.warning(txt[0])
        elif txt[1] == "critical":
            self.__logger.critical(txt[0])
        else:
            self.__logger.info(txt[0])
        if log and self.__cid != 0:
            try:
                await self.__client.send_message(self.__cid, f"{txt[0][:4096]}")
            except FloodWait as f:
                self.__logger.warning(str(f))
                sleep(f.value * 1.5)
            except Exception as err:
                self.__logger.error(str(err))

rep = Reporter(bot, Var.LOG_CHANNEL, LOGS)
