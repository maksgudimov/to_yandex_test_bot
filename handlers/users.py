from aiogram import types
from aiogram.types import InputFile , ChatActions
from aiogram.dispatcher.filters import Text
import os
import speech_recognition as sr
from pydub import AudioSegment
import shutil
import openai

from config import bot,MYID,OPENTOKEN
from strBot.message_text import *
from keyboards.inline_keyboard import *
#в данном проекте не используется FSMContext и База Данных, т.к. это не требуется.

openai.api_key = OPENTOKEN
r = sr.Recognizer()

#хелп функция
async def get_git(message:types.Message):
    await bot.send_message(message.chat.id, f"{git_message}\n\n{go_back_message}")

#хелп функция
async def help(message:types.Message):
    await bot.send_message(message.chat.id, help_message)

#стартовая функция
async def start(message:types.Message):
    await bot.send_message(message.chat.id,start_message,reply_markup=start_keyboard())

#функция обработки callback
async def user_touch_start_kb(callback:types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "photo":
        photo_face = types.InputFile("img/myface.jpg")
        photo_school = types.InputFile("img/myschool.jpg")
        await bot.send_photo(callback.from_user.id,photo_face,photo_self_message)
        await bot.send_photo(callback.from_user.id, photo_school, photo_school_message)
        await bot.send_message(callback.from_user.id,go_back_message)
    if str == "postabout":
        photo_code = types.InputFile("img/code.jpeg")
        await bot.send_photo(callback.from_user.id, photo_code, photo_code_message,parse_mode="HTML")
    if str == "voices":
        voice_gpt = types.InputFile("voices/gpt.ogg")
        voice_sql = types.InputFile("voices/sql.ogg")
        voice_love = types.InputFile("voices/love.ogg")
        voices = [voice_gpt,voice_sql,voice_love]
        for voic , mess in zip(voices,voices_message):
            await bot.send_voice(callback.from_user.id, voic, mess)
        await bot.send_message(callback.from_user.id, go_back_message)

#функция для принятия и отправки мне сообщение от команды /nextstep
async def next_step(message:types.Message):
    if message.text == "/nextstep":
        await bot.send_message(message.chat.id, f"Сообщение не может быть пустым!")
        return
    message_from_user = message.text.split()
    message_to_me = ""
    for i in message_from_user:
        if i == "/nextstep":
            continue
        message_to_me += f" {i}"
    await bot.send_message(MYID,message_to_me)
    await bot.send_message(message.chat.id, f"Ваше сообщение - ({message_to_me}) доставлено!")
    await start(message)

#функция обработки голосовых сообщений
async def voice_message(message:types.Message):
    try:
        if os.path.exists(f"/home/maks/Документы/bot_to_yandex/{message.chat.id}") == False:
            os.mkdir(f"/home/maks/Документы/bot_to_yandex/{message.chat.id}")
        file = await bot.get_file(message.voice.file_id)  # Get file path

        await bot.download_file(file.file_path,
                                f"/home/maks/Документы/bot_to_yandex/{message.chat.id}/{message.voice.file_id}")

        audio_segment = AudioSegment.from_ogg(
            f"/home/maks/Документы/bot_to_yandex/{message.chat.id}/{message.voice.file_id}")
        audio_segment.export(f"/home/maks/Документы/bot_to_yandex/{message.chat.id}/{message.voice.file_id}",
                             format="wav")

        audi = sr.AudioFile(f'/home/maks/Документы/bot_to_yandex/{message.chat.id}/{message.voice.file_id}')
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.TYPING)
        with audi as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            result_ru = r.recognize_google(audio, language='ru-RU')

        await bot.send_message(message.chat.id, f"Ваше сообщение: {result_ru}\n\n{go_back_message}")

        shutil.rmtree(f"/home/maks/Документы/bot_to_yandex/{message.chat.id}")
    except:
        await bot.send_message(message.chat.id, f"Что-то пошло не так, попробуйте еще раз\n\n{go_back_message}")

#функция общения с GPT
async def to_gpt(message:types.Message):
    message_from_user = message.text.split()
    message_to_gpt = ""
    for i in message_from_user:
        if i == "/gpt":
            continue
        message_to_gpt += f" {i}"
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.TYPING)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # gpt-3.5-turbo text-davinci-003
            messages=[
                {"role": "system", "content": "/start"},
                {"role": "user", "content": message_to_gpt}
            ]
        )
        await bot.send_message(message.chat.id,
                               f"{response['choices'][0]['message']['content']}\n\n{go_back_message}")
    except:
        await bot.send_message(message.chat.id,
                               f"Что-то пошло не так. Попробуйте позже.\n\n{go_back_message}")



#функция регистрации хендлеров
def setup(dp):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(help, commands='help')
    dp.register_message_handler(next_step, commands='nextstep')
    dp.register_message_handler(voice_message, content_types=['voice'])
    dp.register_message_handler(to_gpt, commands='gpt')
    dp.register_message_handler(get_git, commands='git')

    dp.register_callback_query_handler(user_touch_start_kb,Text(startswith="start_"))