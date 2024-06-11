from time import sleep
from handlers.users.music_search_name import recieve_text
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import logging,re
from aiogram import types
from aiogram.types import CallbackQuery
from .insta import instadownloader
from data.config import ADMINS
from filters import IsUser, IsSuperAdmin, IsGuest
from filters.admins import IsAdmin
from keyboards.inline.main_menu_super_admin import main_menu_for_super_admin, main_menu_for_admin
from loader import dp, db, bot
from utils.files.spotify import SearchFromSpotify
from utils.files.download_spotify import DownloadMusic
logging.basicConfig(level=logging.INFO)
import re,json
#from tiktok_downloader import snaptik
import os, requests
from utils.files.shazam import shazamtop
import random  
import os
from .slider_sender import send_music
word = "q w e r t y u i  o p a s d f g h  j k l z x  c v b n m"
words = word.split(' ')




@dp.message_handler(IsAdmin(), CommandStart(), state="*")
async def bot_start_admin(message: types.Message):
    await message.answer(f"Salom admin, {message.from_user.full_name}!",
                         reply_markup=main_menu_for_admin)

@dp.message_handler(IsSuperAdmin(), CommandStart(), state="*")
async def bot_start_super_admin(message: types.Message):
    await message.answer(f"Salom boss, {message.from_user.full_name}!",
                         reply_markup=main_menu_for_super_admin)

@dp.message_handler(commands=['start'], state="*")
async def bot_start(message: types.Message):
    user = message.from_user
    if 2<5:
        db.add_user(user_id=user.id,name=user.first_name,active=True)
    else:
        pass
    user_id = message.from_user.first_name
    await message.answer("🤖Bu bot orqali quyidagilarni yuklab olishingiz mumkin: \n• Instagram - (stories/post/reels) \n• TikTok - (video/photo) [ Tez kunda ]\n• YouTube - (video)\n\n😉Maksimal yuklash hajmi - 400mb\n🤖 @full_downloaderr_bot")

    #await message.answer(f"Assalomu alaykum{user_id}\n\n </b>Media yuklashim uchun havolani yuboring")

instagram_regex = r'(https?:\/\/(?:www\.)?instagram\.com\/[-a-zA-Z0-9@:%._+~#=]*)'
tiktok_regex = r'(https?:\/\/(?:www\.)?tiktok\.com\/@[-a-zA-Z0-9_]+\/video\/\d+)'
#youtube_regex = r'(https?:\/\/(?:www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]+)'
youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    

async def download_instagram_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    download_data = await instadownloader(text)

    if download_data:
        try:
            await bot.send_document(message.chat.id, download_data['url'], caption="@full_downloaderr_bot orqali yuklab olindi!")
            
        except Exception as err:
            print(err)
            await message.answer("<b>Kechirasiz, kontentni yuklashda xatolik yuz berdi, qaytadan urining 😔</b>")
    else:
        await message.answer("<b>Bu havolada kontent topilmadi 😔</b>")

async def download_tiktok_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

    res = snaptik(text)
    video = res[0].download(f"{message.message_id}.mp4")
    input_file = types.InputFile(f"{message.message_id}.mp4")
    await bot.send_video(message.chat.id, video=input_file, caption="@full_downloaderr_bot orqali yuklab olindi!")
    os.remove(f"{message.message_id}.mp4")

async def download_youtube_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

    r = requests.get(f"https://youtube-dl.wave.video/info?url={text}&type=video")
    print(r.status_code)
    vid = r.json().get('formats', [{}])[0].get('downloadUrl')
    sub = random.choice(words)
    sub2 = random.choice(words)
    filename = f"video_{sub}_{sub2}.mp4"

    response = requests.get(vid)

    with open(filename, 'wb') as f:
        f.write(response.content)
    file = types.InputFile(filename)
    try:
        print("hello")
        await bot.send_video(chat_id=message.chat.id, video=file, caption="@full_downloaderr_bot orqali yuklab olindi!")
        
    except Exception as err:
        print(err)
        await message.answer("<b>Kechirasiz, kontentni yuklashda xatolik yuz berdi, qaytadan urining 😔</b>")
    os.remove(f"{filename}")
# Handle text messages
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    text = message.text
    matches = re.findall(youtube_regex, text)
    
    # Agar link topilsa True, aks holda False qaytarish
    if re.search(instagram_regex, text):
        await download_instagram_video(message, text)
    elif "tiktok.com" in text:
        await download_tiktok_video(message, text)
    elif bool(matches):
        await download_youtube_video(message, text)
    else:
        await recieve_text(message)

@dp.callback_query_handler(text_contains="^")
async def music(message:types.Message):
    await send_music(message)
