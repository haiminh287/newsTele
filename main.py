import tradingview as tv
import client as c
from botTele import TelegramBot
from client_fxstreet import FXStreetBot
from forex_live import ForexLiveBot

import time
intros = ['Quý vị cần tư vấn chuyên nghiệp và tận tâm về giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị muốn tối ưu hóa lợi nhuận từ giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị cần lời khuyên và chiến lược đỉnh cao về giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị muốn khám phá cơ hội mới trên thị trường ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị muốn chinh phục thị trường ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị cần tư vấn về các bước đi đúng đắn trong giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị cần một người đồng hành trong hành trình giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị mới bắt đầu giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị muốn nâng cao kỹ năng giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị không muốn bỏ lỡ cơ hội giao dịch ngoại hối hiệu quả? Hãy yêu cầu tư vấn.',
          'Quý vị mới vào thị trường ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị cần hỗ trợ chuyên nghiệp để khởi đầu giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị đang tìm hiểu về giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị muốn nâng cao kỹ năng giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị muốn cải thiện kỹ năng giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị không muốn bỏ lỡ cơ hội học hỏi về giao dịch ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị muốn giao dịch ngoại hối hiệu quả hơn? Hãy yêu cầu tư vấn.',
          'Quý vị muốn tìm hiểu cách giao dịch ngoại hối thành công? Hãy yêu cầu tư vấn.',
          'Quý vị muốn tăng cường kiến thức và kỹ năng ngoại hối? Hãy yêu cầu tư vấn.',
          'Quý vị muốn thành công trong giao dịch ngoại hối? Hãy yêu cầu tư vấn.'
          ]
BOT_LUX = TelegramBot(
    "7554041257:AAFUAwMCoYs4491t6vDocZ1W9qBvbvjVzto", "BOT_LUX", "https://t.me/TNH9898")
BOT_LUX = TelegramBot(
    "6866400621:AAFUt7yBvStoq2GxtBZYmXYBZonMI5bMyUc", "HM_LO_BOT", "https://t.me/applehm")
FX_BOT = FXStreetBot(
    api_id=18353013,
    api_hash="e39976efc4e58975354ca48914a2c48e",
    group_id='-1002007128570',
    bot=BOT_LUX,
    users=[{
        'Admin': 'https://t.me/TNH9898'
    }],
    intros=intros
)
FL_BOT = ForexLiveBot(
    api_id=18353013,
    api_hash="e39976efc4e58975354ca48914a2c48e",
    bot=BOT_LUX,
    group_id='-1002007128570',
    users=[],
    intros=intros)
if __name__ == "__main__":
    while True:
        try:
            # tv.Scrap_community_idea(BOT_LUX=BOT_LUX, group_id='-1002406206404')
            # time.sleep(30)
            c.bot_send_client(BOT_LUX=BOT_LUX, group_id=-1002007128570)
            time.sleep(5)
            FX_BOT.run(-1001510625232)
            time.sleep(5)
            FL_BOT.run()
            time.sleep(360)
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in 60 seconds...")
            time.sleep(30)
