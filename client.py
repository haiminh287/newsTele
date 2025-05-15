import cutImageMain as c
import os
import time
import re
import json
from telethon.sync import TelegramClient


def get_user_groups(api_id, api_hash):
    client = TelegramClient('+84925519377', api_id, api_hash)

    try:
        client.connect()
        groups = []
        for dialog in client.iter_dialogs():
            if dialog.is_group:
                groups.append(dialog)
        client.disconnect()

        return groups
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
# api_id = 28452544
# api_hash = "17161fcd2a9f644f0116a0f0b347c56d"


def get_user_channel_ids(api_id, api_hash):
    client = TelegramClient('+84925519377', api_id, api_hash)
    try:
        client.connect()
        channels = []
        for dialog in client.iter_dialogs():
            if dialog.is_channel:
                channels.append((dialog.title, dialog.id))
        client.disconnect()
        return channels
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
# Gọi hàm để lấy danh sách tất cả các nhóm mà người dùng đang tham gia
# user_groups = get_user_groups(api_id, api_hash)
# if user_groups:
#     print("User groups:")
#     for group in user_groups:
#         print(group.name, group.id)
# user_channel_ids = get_user_channel_ids(api_id, api_hash)


def get_channel_messages(api_id, api_hash, channel_id, limit=1):
    client = TelegramClient('+84925519377', api_id, api_hash)
    try:
        client.connect()
        channel = client.get_entity(channel_id)
        messages = client.get_messages(channel, limit=limit)
        client.disconnect()

        return messages
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# if user_channel_ids:
#     print("User channel IDs:")
#     for channel_id in user_channel_ids:
#         print(channel_id)


def txtOldData(text):
    account = [{"Content": text}]
    try:
        with open("Article_Trading.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        flag = True
        for index, user in enumerate(data):
            if user["Content"] == text:
                # if user["newOrder"] == newOrder and user["entryLevel"] == entryLevel:
                flag = False
                data[index] = account[0]
        if flag == True:
            data.extend(account)
        with open("Article_Trading.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=3)
    except FileNotFoundError:
        with open("Article_Trading.json", "w", encoding="utf-8") as file:
            json.dump(account, file, indent=3)


def get_content():
    arrs = []
    if os.path.exists("Article_Trading.json"):
        with open("Article_Trading.json", "r") as f:
            arr = json.load(f)
        for x in arr:
            arrs.append(x["Content"])
    return arrs


def read_and_write(filename, data) -> bool:
    with open(file=filename, mode='a+', encoding='utf-8') as f:
        f.seek(0)
        datas = f.read()
        if data not in datas:
            f.write(data + '\n')
            return True
        return False


def changeText(text):
    parts = text.split("\n\n", 1)
    title = parts[0]
    content = parts[1]
    return f'<b>{title}</b>' + '\n\n' + content+'\n\n'+'#LuxNews #Forex'


def bot_send_client(BOT_LUX, group_id):
    api_idAnna = 18353013
    api_hashAnna = "e39976efc4e58975354ca48914a2c48e"
    channel_messages = get_channel_messages(
        api_idAnna, api_hashAnna, -1001250805787, 1)
    if channel_messages:
        for message in channel_messages:
            if (read_and_write("client.txt", message.message)) and "The S" not in message.message:
                translateText = c.translate_text(message.message)
                translateText = changeText(translateText)
                BOT_LUX.sendMessage(
                    group_id, translateText)
