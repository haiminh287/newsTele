import tradingview as tv
import client as c
from botTele import TelegramBot
import time
BOT_LUX = TelegramBot(
    "7554041257:AAFUAwMCoYs4491t6vDocZ1W9qBvbvjVzto", "BOT_LUX", "https://t.me/TNH9898")
if __name__ == "__main__":
    while True:
        tv.Scrap_community_idea(BOT_LUX=BOT_LUX, group_id='-1002406206404')
        time.sleep(30)
        c.bot_send_client(BOT_LUX=BOT_LUX, group_id='-1002406206404')
        time.sleep(120)
