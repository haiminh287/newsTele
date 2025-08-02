import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from telethon.sync import TelegramClient
import cutImageMain as c
import instantview as iv
import random


class ForexLiveBot:
    def __init__(self, api_id, api_hash, bots, group_ids, users, intros):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bots = bots
        self.group_ids = group_ids
        self.users = users
        self.intros = intros
        self.old_messages_file = "messageForexLive.json"

    def get_channel_messages(self, channel_id, limit=1):
        with TelegramClient('+84925519377', self.api_id, self.api_hash) as client:
            channel = client.get_entity(channel_id)
            return client.get_messages(channel, limit=limit)

    def is_new_url(self, url):
        if os.path.exists(self.old_messages_file):
            with open(self.old_messages_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return all(entry["url"] != url for entry in data)
        return True

    def get_slug_news(self):
        url = "https://api.investinglive.com/api/articles/get-all-news?take=1"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US",
            "deviceid": "fd3381bd-5fb2-41d2-ac30-1b5e4662d5b8-1753715474903",
            "page": "/Cryptocurrency/eth-futures-or-eth-spot-20250728/",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://investinglive.com/"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['Articles'][0]['Slug']
        return []

    def get_detail_news(self, article_slug):
        url = f"https://api.investinglive.com/api/articles/get-article-content-by-slug?articleSlug={article_slug}"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US",
            "deviceid": "fd3381bd-5fb2-41d2-ac30-1b5e4662d5b8-1753715474903",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://investinglive.com/"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(response.json())
            article_url = response.json()['ArticleUrl']
            article_response = requests.get(article_url)
            return article_response.json()

        return None

    def save_url(self, title, url):
        entry = {"title": title, "url": url}
        try:
            with open(self.old_messages_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(entry)
        with open(self.old_messages_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    from bs4 import BeautifulSoup

    def html_to_telegraph_json(self, html_str):
        soup = BeautifulSoup(html_str, "lxml")
        result = []

        for elem in soup.body or soup.contents:
            if isinstance(elem, str):
                continue
            if elem.name == "p":
                text = elem.get_text(strip=True)
                if text:
                    # Dịch văn bản trước khi thêm vào kết quả
                    translated_text = c.translate_text(text)
                    result.append({"tag": "p", "children": [translated_text]})

                # Xử lý ảnh trong thẻ p
                img = elem.find("img")
                if img and img.get("src"):
                    result.append({
                        "tag": "img",
                        "attrs": {"src": img["src"], "alt": img.get("alt", "Image")}
                    })

            elif elem.name == "ul":
                ul_obj = {"tag": "ul", "children": []}
                for li in elem.find_all("li"):
                    text = li.get_text(strip=True)
                    if text:
                        # Dịch văn bản trước khi thêm vào danh sách
                        translated_text = c.translate_text(text)
                        ul_obj["children"].append(
                            {"tag": "li", "children": [translated_text]})
                result.append(ul_obj)

            elif elem.name in ["h2", "h3", "strong"]:
                text = elem.get_text(strip=True)
                if text:
                    # Dịch văn bản trước khi thêm vào kết quả
                    translated_text = c.translate_text(text)
                    result.append(
                        {"tag": "strong", "children": [translated_text]})

            elif elem.name == "img":
                if elem.get("src"):
                    result.append({
                        "tag": "img",
                        "attrs": {"src": elem["src"], "alt": elem.get("alt", "Image")}
                    })

        return result

    def run(self):
        article = self.get_detail_news(self.get_slug_news())
        if (self.is_new_url(article['ArticleId'])):
            access_token, auth_url = iv.createAcount()
            title = article['Topic']
            html_content = article['Body']
            content = self.html_to_telegraph_json(html_content)
            # print(content)

            translated_title = c.translate_text(title)
            translated_title = re.sub(
                'ForexLive', '', translated_title)

            featured_image_url = None
            if article.get('FeaturedImage') and article['FeaturedImage'].get('URL'):
                featured_image_url = article['FeaturedImage']['URL']
                print(featured_image_url)

            web_url = iv.createPage(
                "John Trần", access_token, translated_title, content, auth_url, featured_image_url=featured_image_url
            )
            self.bots[0].sendMessageHasUrl(
                self.group_ids[0], translated_title, random.choice(
                    self.intros), web_url
            )
            self.bots[1].sendMessageHasUrl(
                self.group_ids[1], translated_title, random.choice(
                    self.intros), web_url, topic_id=4294999733
            )

            self.save_url(title, article['ArticleId'])
