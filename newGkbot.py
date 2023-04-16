from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup as bs
import requests
import os
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
from pytube import YouTube

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.1027 Yowser/2.5 Safari/537.36"
}
async def on_startup(_):
    print("bot вышел в онлайн")



# команда старт
@dp.message_handler(commands=["start"])
async def start(message: types.message):
    print(message.chat.id, message.text)
    await bot.send_message(message.chat.id, """я буду скидывать аудио из тех ссылок на ютуб что вы мне отправите( после отправки ссылки подождите 1-2 минуты. ибо инет у меня не как в пентагоне""",

parse_mode="html", disable_web_page_preview=True)


# ПАРСЕР
@dp.message_handler(content_types=["text"])
async def parser(message: types.message):
    print(message.chat.id, message.text)
    if "https://youtu" in message.text or "https://www.youtu" in message.text:
        url = message.text
        request = requests.get(url, headers=headers)
        soup = bs(request.text, "html.parser")
        data = soup.text.split('YouTube')
        name = data[0][:-3]+".mp3"
        yt = YouTube(message.text)
        yd = yt.streams.get_audio_only()
        yd.download(filename=name)
        await bot.send_audio(message.chat.id, open(name,"rb"))
        os.remove(name)
    else:
        await bot.send_message(message.chat.id, """отправте пожалуйста ссылку с ютуба""")

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)