from decouple import config
import telegram

tg_token = config('TG_TOKEN')
bot = telegram.Bot(token=tg_token)

chat_id = '@dvmn_space_photos'
bot.send_message(chat_id=chat_id, text="Hello, world!")
