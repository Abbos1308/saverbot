from simple_header import get
from time import sleep
from handlers.users.music_search_name import recieve_text
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import logging,re
from aiogram import types
from aiogram.types import CallbackQuery , InputFile
from .insta import instadownloader
from .facebook import fbdownloader
from .tiktok import ttdownloader
from .pin import pindownloader
from .download import download_file
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
    try:
        db.add_user(user_id=user.id,name=user.first_name,active=1)
    except:
        pass
    user_id = message.from_user.first_name
    await message.answer("<b>🤖Bu bot orqali quyidagilarni yuklab olishingiz mumkin: \n• Instagram - (stories/post/reels) \n• TikTok - (video/photo)\n• YouTube - (video)\n• Facebook - (video)\n\n😉Maksimal yuklash hajmi - 400mb\n🤖 @full_downloaderr_bot</b>",parse_mode="HTML")


instagram_regex = r'(https?:\/\/(?:www\.)?instagram\.com\/[-a-zA-Z0-9@:%._+~#=]*)'
tiktok_regex = r'(https?:\/\/(?:www\.)?tiktok\.com\/@[-a-zA-Z0-9_]+\/video\/\d+)'
#youtube_regex = r'(https?:\/\/(?:www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]+)'
youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
facebook_regex = re.compile(
    r'^(https?://)?(www\.)?facebook\.com/([A-Za-z0-9._-]+)(/)?'
)

async def download_instagram_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    download_data = await instadownloader(text)

    if download_data:
        try:
            sub = random.choice(words)
            sub2 = random.choice(words)
            filename = f"video_insta_{sub}_{sub2}.mp4"
            response = requests.get(download_data)

            with open(filename, 'wb') as f:
                f.write(response.content)
            file = types.InputFile(filename)
            #video = InputFile.from_url(download_data)
            await bot.send_document(message.chat.id, file, caption="@full_downloaderr_bot orqali yuklab olindi!")
        except Exception as err:
            print(err)
            
            await message.answer("<b>Kechirasiz, kontentni yuklashda xatolik yuz berdi, qaytadan urining 😔</b>")
    else:
        await message.answer("<b>Bu havolada kontent topilmadi 😔</b>")
    os.remove(f"{filename}")
async def download_facebook_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    download_data = await fbdownloader(text)

    if download_data:
        try:
            sub = random.choice(words)
            sub2 = random.choice(words)
            filename = f"video_fb_{sub}_{sub2}.mp4"
            response = requests.get(download_data)

            with open(filename, 'wb') as f:
                f.write(response.content)
            file = types.InputFile(filename)
            #video = InputFile.from_url(download_data)
            await bot.send_document(message.chat.id, file, caption="@full_downloaderr_bot orqali yuklab olindi!")
        except Exception as err:
            print(err)
            
            await message.answer("<b>Kechirasiz, kontentni yuklashda xatolik yuz berdi, qaytadan urining 😔</b>")
    else:
        await message.answer("<b>Bu havolada kontent topilmadi 😔</b>")
    os.remove(f"{filename}")

async def download_tiktok_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    #headers = {'Host': 'tikcdn.io', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Sec-Ch-Ua': '"Not A(Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': 'Windows', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Referer': 'https://www.instagram.com/', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5'}
    download_data = await ttdownloader(text)
    headers = get(text,mobile=True)
    if download_data:
        try:
            sub = random.choice(words)
            sub2 = random.choice(words)
            filename = f"video_tt_{sub}_{sub2}.mp4"
            await download_file(download_data,filename,headers)
            file = types.InputFile(filename)
            #video = InputFile.from_url(download_data)
            await bot.send_video(message.chat.id, file, caption="@full_downloaderr_bot orqali yuklab olindi!")
        except Exception as err:
            print(err)
            
            await message.answer("<b>Kechirasiz, kontentni yuklashda xatolik yuz berdi, qaytadan urining 😔</b>")
    else:
        await message.answer("<b>Bu havolada kontent topilmadi 😔</b>")
    os.remove(f"{filename}")
async def download_youtube_video(message, text):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

    r = requests.get(f"https://youtube-dl.wave.video/info?url={text}&type=video")
    print(r.status_code)
    vid_size = r.json().get('formats', [{}])[0].get('filesize_approx') or r.json().get('formats', [{}])[0].get('filesize')
    vid_size = vid_size/(1024*1024)
    if vid_size > 35:
        await message.answer("Video hajmi juda katta")
    else:
        vid = r.json().get('formats', [{}])[0].get('downloadUrl')
        sub = random.choice(words)
        sub2 = random.choice(words)
        filename = f"video_{sub}_{sub2}.mp4"
        response = requests.get(vid)

        with open(filename, 'wb') as f:
            f.write(response.content)
        
        #await download_file(vid,filename)
        file = types.InputFile(filename)
        try:
            print("hello")
            await bot.send_video(chat_id=message.chat.id, video=file, caption="@full_downloaderr_bot orqali yuklab olindi!")
            
        except Exception as err:
            print(err)
            await message.answer("<b>Kechirasiz, kontentni yuklashda xatolik yuz berdi, qaytadan urining 😔</b>")
        os.remove(f"{filename}")

async def download_pin_video(message):
    msg_del = await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    download_data = await pindownloader(message.text)
    if download_data:
        if download_data['type']=="video":
            await message.answer_video(download_data['url'])
        else:
            await message.answer_photo(download_data['url'])
    else:
        await message.answer("Noto'g'ri havola")


# Handle text messages
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    text = message.text
    matches_yt = re.findall(youtube_regex, text)
    matches_fb = re.findall(facebook_regex,text)
    # Agar link topilsa True, aks holda False qaytarish
    if re.search(instagram_regex, text):
        await download_instagram_video(message, text)
    elif "tiktok.com" in text:
        await download_tiktok_video(message, text)
    elif bool(matches_yt):
        await download_youtube_video(message, text)
    elif bool(matches_fb):
        await download_facebook_video(message,text)
    elif "pin" in text and "http" in text:
        await download_pin_video(message)
    else:
        await recieve_text(message)

@dp.callback_query_handler(text_contains="^")
async def music(message:types.Message):
    await send_music(message)
