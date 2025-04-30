from decouple import config
import telegram

tg_token = config('TG_TOKEN')
bot = telegram.Bot(token=tg_token)

chat_id = '@dvmn_space_photos'
bot.send_photo(chat_id=chat_id, photo=open('images/spacex/spacex_0.jpg', 'rb'))