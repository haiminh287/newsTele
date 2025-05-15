import requests
import cutImageMain as c
import instantview as iv


def read_and_write(filename, data) -> bool:
    with open(file=filename, mode='a+', encoding='utf-8') as f:
        f.seek(0)
        datas = f.read()
        if data not in datas:
            f.write(data + '\n')
            return True
        return False


def scrap_details(image_url) -> dict:
    data = requests.get(
        f"https://www.tradingview.com/chart/-/{image_url}/json/")
    return data.json()


def translate(title, content) -> str:
    title = c.translate_text(title, 'vi')
    content = c.translate_text(content, 'vi')
    return title, content


def Scrap_community_idea(BOT_LUX, group_id):
    url = "https://www.tradingview.com/api/v1/main_page/community_ideas/"
    res = requests.get(url)

    if (res.status_code == 200):

        items = res.json()['data']['popular']['items']

        for item in items:
            content = []
            title = item['name']
            if (read_and_write('tradingview.txt', title)):
                print(title)
                image_url = item['image_url']
                created_at = item['created_at']
                symbol = item["symbol"]['name']
                image = item['image']["big"]
                print(image)

                data_details = scrap_details(image_url)

                content.append(
                    {"tag": "img", "attrs": {"src": image, "caption": "Image Caption"}})

                title, description_detail = translate(
                    title, data_details['description'])
                content.append(description_detail)
                url_new_page = new_page_instanview(title, content)

                BOT_LUX.sendMessage(
                    group_id, '\n' + title, url_new_page)
                print(url_new_page)


def new_page_instanview(title, content):
    account = iv.createAcount()
    accessToken = account[0]
    auth_url = account[1]
    url_web = iv.createPage("LUX", accessToken, title, content, auth_url)
    return url_web
