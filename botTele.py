import os
from datetime import datetime
import numpy as np
import requests
import json
import os


class TelegramBot:
    def __init__(self, bot_token, name_bot, admin="https://t.me/Applehm"):
        self.bot_token = bot_token
        self.name_bot = name_bot
        self.url = "https://api.telegram.org/bot{}".format(bot_token)
        self.admin = admin

    def getUpdateBot(self):
        telegram_url = f'{self.url}/getUpdates'
        print(telegram_url)
        response = requests.get(telegram_url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            chat_ids = []
            for update in data['result']:
                print(update)
                if 'message' in update and 'chat' in update['message'] and update['message']['chat']['type'] == 'group':
                    chat_id = update['message']['chat']['id']
                    if chat_id not in chat_ids:
                        chat_ids.append(chat_id)
            print("Group Chat IDs:")
            for chat_id in chat_ids:
                print(chat_id)
        else:
            print("Failed to fetch updates. Status code:", response.status_code)
            print(response.text)

    def sendPhoto(self, group_id, file_name, text_new, text):
        telegram_url = f'{self.url}/sendPhoto'
        # reply_markup = {"inline_keyboard": [
        #     [{"text": f"Yêu Cầu Admin Giải Thích Thêm !!!", "url": self.admin}]]}
        textNew = '💬 <i>{}</i> 🔮🔮🔮'.format(text_new)
        with open(file_name, 'rb') as file:
            files = {'photo': file}
            params = {'chat_id': group_id, 'caption':  text + '\n\n' + textNew,
                      #   'parse_mode': 'HTML', 'reply_markup': json.dumps(reply_markup)}
                      'parse_mode': 'HTML'}
            response = requests.post(telegram_url, params=params, files=files)

        if response.status_code == 200:
            print("Photo sent successfully.")
        else:
            print("Failed to send photo. Status code:", response.status_code)
            print(response.text)

    def sendMessage(self, group_id, text, url_web=None):
        telegram_url = f'{self.url}/sendMessage'
        # reply_markup = {"inline_keyboard": [
        #     [{"text": f"💬 Liên Hệ Admin Để Biết Chi Tiết 🔮🔮🔮!!!", "url": self.admin}]]}
        if (url_web):
            text = '<a href="{}"><b>{}</b></a>'.format(url_web, text.title())
        # textNew = '<i>{}</i> '.format(textNew)
        data = {'text': text, 'chat_id': group_id,
                #   'parse_mode': 'HTML', 'reply_markup': json.dumps(reply_markup)}
                'parse_mode': 'HTML'}
        response = requests.post(telegram_url, json=data)

        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print("Failed to send message. Status code:", response.status_code)
            print(response.text)

    def sendMessageHasUrl(self, group_id, title, intro, url_web, **kwargs):
        telegram_url = f'{self.url}/sendMessage'
        # reply_markup = {"inline_keyboard": [
        #     [{"text": f"Yêu Cầu {name} Tư Vấn Ngay !!!", "url": url}]]}
        intro = '💬 <i>{}</i> 🔮🔮🔮'.format(intro)
        title = '<a href="{}"><b>{}</b></a>'.format(url_web, title.title())
        data = {'chat_id': group_id, 'text': title+'\n\n' + intro,
                # 'parse_mode': 'HTML', 'reply_markup': json.dumps(reply_markup)}
                'parse_mode': 'HTML'}
        response = requests.post(telegram_url, json=data)
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print("Failed to send message. Status code:", response.status_code)
            print(response.text)

    def sendFileGroup(self, group_id, file_path, file_url):
        telegram_url = f'{self.url}/sendDocument'
        reply_markup = {"inline_keyboard": [
            [{"text": "Nhắn Tin ", "url": file_url}]]}
        data = {'chat_id': group_id, 'reply_markup': json.dumps(reply_markup)}

        with open(file_path, 'rb') as file:
            files = {'document': file}
            response = requests.post(telegram_url, data=data, files=files)

        if response.status_code == 200:
            print("File sent successfully.")
        else:
            print("Failed to send file. Status code:", response.status_code)
            print(response.text)

    def sendVideoFromMessage(self, group_id, text, textNew, name, url, video):
        telegram_url = f'{self.url}/sendVideo'
        reply_markup = {"inline_keyboard": [
            [{"text": f"Yêu Cầu {name} Tư Vấn Ngay !!!", "url": url}]]}
        textNew = '💬 <i>{}</i> 🔮🔮🔮'.format(textNew)
        data = {'chat_id': group_id, 'caption': text+'\n\n' + textNew,
                'parse_mode': 'HTML', 'reply_markup': json.dumps(reply_markup)}
        with open(video, 'rb') as video_file:
            files = {'video': video_file}
            response = requests.post(telegram_url, data=data, files=files)

        if response.status_code == 200:
            print("Video sent successfully.")
        else:
            print("Failed to send video. Status code:", response.status_code)
            print(response.text)

# file = os.getcwd() + '\\Hướng dẫn giao dịch Forex.pdf'
# sendFileGroupTest(file,'https://drive.google.com/uc?export=download&id=1HwHrITLZMIh0OIMGmX0QSyETrx7H-3U4')
# file = os.getcwd() + '\\Sp_IQX\\Quỳnh Anh.pdf'
# sendFileGroupTest(file,'https://t.me/QuynhAnh_IQXsp')
# file = os.getcwd() + '\\Sp_IQX\\CPI Tháng 10102024.pdf'
# print(file)
# sendFileGroupTest(file,'https://t.me/JohnMrPips')

# TelegramBot("7554041257:AAFUAwMCoYs4491t6vDocZ1W9qBvbvjVzto", "Lux Thiens").getUpdateBot()
