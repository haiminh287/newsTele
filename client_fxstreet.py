# refactored_client_fxstreet.py

import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from telethon.sync import TelegramClient
from utils import read_and_write
from botTele import TelegramBot
import cutImageMain as c
import instantview as iv


class FXStreetBot:
    def __init__(self, api_id, api_hash, bots, group_ids, users, intros):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bots = bots
        self.group_ids = group_ids
        self.users = users
        self.intros = intros

    def get_channel_messages(self, channel_id, limit=1):
        with TelegramClient('+84925519377', self.api_id, self.api_hash) as client:
            channel = client.get_entity(channel_id)
            return client.get_messages(channel, limit=limit)

    def is_new_message(self, message):
        if os.path.exists("message.json"):
            with open("message.json", "r", encoding="utf-8") as f:
                old_messages = json.load(f)
            return all(msg["message"] != message for msg in old_messages)
        return True

    def save_message(self, message, url):
        new_entry = {"message": message, "url": url}
        try:
            with open("message.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        for idx, msg in enumerate(data):
            if msg["message"] == message:
                data[idx] = new_entry
                break
        else:
            data.append(new_entry)

        with open("message.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def parse_title(self, message):
        title = re.split(r'\n+', message)[0]
        title = re.sub(r'\[.*?\]', '', title)
        return c.translate_text(title)

    def scrap_url(self, url):
        contents = []
        res = requests.get(url)
        if res.status_code != 200:
            return contents

        soup = BeautifulSoup(res.text, 'lxml')
        article = soup.find(id="fxs_article_content")
        if not article:
            return contents

        for element in article.children:
            if element.name == "ul":
                ul_content = {"tag": "ul", "children": []}
                for li in element.find_all('li'):
                    ul_content["children"].append(
                        {"tag": "li", "children": [c.translate_text(li.text.strip())]})
                contents.append(ul_content)
            elif element.name == "p":
                if element.text.strip():
                    contents.append(
                        {"tag": "p", "children": [c.translate_text(element.text.strip())]})
                    if (img := element.find("img")) and 'src' in img.attrs:
                        contents.append(
                            {"tag": "img", "attrs": {"src": img['src'], "caption": "Image Caption"}})
            elif element.name in ["h2", "h3"]:
                contents.append({"tag": "strong", "children": [
                                c.translate_text(element.text.strip())]})
                if (img := element.find("img")) and 'src' in img.attrs:
                    contents.append(
                        {"tag": "img", "attrs": {"src": img['src'], "caption": "Image Caption"}})
        return contents

    def run(self, channel_id):
        index_user = 0
        index_intro = 0
        account = iv.createAcount()
        access_token, auth_url = account[0], account[1]
        messages = self.get_channel_messages(channel_id)
        for msg in messages:
            if not self.is_new_message(msg.message):
                continue
            title = self.parse_title(msg.message)
            print(f"Processing message: {title}")
            url = None
            if hasattr(msg, 'entities') and msg.entities and hasattr(msg.entities[0], 'url'):
                url = msg.entities[0].url
            elif hasattr(msg.media, 'webpage'):
                url = msg.media.webpage.url
            if url:
                content = self.scrap_url(url)
                # user_name = list(self.users[index_user].keys())[0]
                # user_url = list(self.users[index_user].values())[0]
                page_url = iv.createPage(
                    "John Trần", access_token, title, content, auth_url)
                self.bots[0].sendMessageHasUrl(
                    self.group_ids[0], title, self.intros[index_intro], page_url
                )
                self.bots[1].sendMessageHasUrl(
                    self.group_ids[1], title, self.intros[index_intro], page_url, topic_id=4294999733
                )
                self.save_message(msg.message, url)
                index_user = (index_user + 1) % len(self.users)
                index_intro = (index_intro + 1) % len(self.intros)
