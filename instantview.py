# https://telegra.ph/upload
# https://api.telegra.ph/createPage
import json
import requests


def createAcount():
    url = "https://api.telegra.ph/createAccount"
    data = {
        "short_name": "LUX",
        "author_name": "LUX"
    }
    response = requests.post(url, json=data)
    result = response.json()
    if response.status_code == 200:
        return [result["result"]["access_token"], result["result"]["auth_url"]]
    else:
        print(response.json())


def revokeAccessToken(access_token):
    url = "https://api.telegra.ph/revokeAccessToken"
    data = {
        "access_token": access_token
    }
    response = requests.post(url, json=data)
    result = response.json()
    if response.status_code == 200:
        return [result["result"]["access_token"], result["result"]["auth_url"]]
    else:
        print(response.json())


def createPage(nameAuthor, access_token, title, content, author_url, return_content=True):
    url = "https://api.telegra.ph/createPage"
    author_name = nameAuthor
    data = {
        "access_token": access_token,
        "title": title,
        "author_name": author_name,
        "author_url": author_url,
        "content": content,
        "return_content": return_content
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["result"]["url"]
    else:
        revoke = revokeAccessToken(access_token)
        access_token = revoke[0]
        author_url = revoke[1]
        createPage(access_token, title, content, author_url)
# createAcount()
