import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, WEBHOOK, PORT
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from aiohttp import web

from __future__ import annotations
from abc import ABC, abstractmethod

import pytz
import datetime
import os, argparse
import asyncio, shlex
from os.path import join
from aiofiles.os import remove
from aiohttp import ClientSession
from typing import  Union, List
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from style import Ashu 

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://github.com/AshutoshGoswami24")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
    
__version__ = "1.0"
__author__ = "https://t.me/hiddenextractorbot"
__license__ = "MIT"
__copyright__ = "Copyright 2024"


basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[FileHandler('logs.txt', encoding='utf-8'),
              StreamHandler()],
    level=INFO)


@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    await m.reply_text(
       Ashu.START_TEXT, reply_markup=InlineKeyboardMarkup(
            [
                    [
                    InlineKeyboardButton("✜ ᴀsʜᴜᴛᴏsʜ ɢᴏsᴡᴀᴍɪ 𝟸𝟺 ✜" ,url="https://t.me/AshutoshGoswami24") ],
                    [
                    InlineKeyboardButton("🦋 𝐅𝐨𝐥𝐥𝐨𝐰 𝐌𝐞 🦋" ,url="https://t.me/AshuSupport") ]                               
            ]))
@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("♦ 𝐒𝐭𝐨𝐩𝐩𝐞𝐭 ♦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)



@bot.on_message(filters.command(["txt2"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('sᴇɴᴅ ᴍᴇ .ᴛxᴛ ғɪʟᴇ  ⏍')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
       with open(x, "r") as f:
           content = f.read()
       content = content.split("\n")
       links = []
       for i in content:
           links.append(i.split("://", 1))
       os.remove(x)
            # print(len(links)
    except:
           await m.reply_text("∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.")
           os.remove(x)
           return
    
   
    await editable.edit(f"ɪɴ ᴛxᴛ ғɪʟᴇ ᴛɪᴛʟᴇ ʟɪɴᴋ 🔗** **{len(links)}**\n\nsᴇɴᴅ ғʀᴏᴍ  ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛᴀʟ ɪs `1`")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("∝ 𝐍𝐨𝐰 𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐞𝐧𝐝 𝐌𝐞 𝐘𝐨𝐮𝐫 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    

    await editable.edit(Ashu.Q1_TEXT)
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit(Ashu.C1_TEXT)
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Robin':
        MR = highlighter 
    else:
        MR = raw_text3
   
    await editable.edit(Ashu.T1_TEXT)
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'}).json()['url']
            
            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
           
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'**[🎬] Vid_ID: {str(count).zfill(3)}.**\n**Video Title :** {𝗻𝗮𝗺𝗲𝟭}.mkv\n**Batch Name :** {raw_text0}\n\n**Extracted By ➤ {MR}**'
                cc1 = f'**[📕] Pdf_ID: {str(count).zfill(3)}.**\n**Pdf Title :** {𝗻𝗮𝗺𝗲𝟭}.pdf \n**Batch Name :** {raw_text0}\n\n**Extracted By ➤ {MR}**'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    Show = f"❊⟱ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ⟱❊ »\n\n📝 𝐍𝐚𝐦𝐞 » `{name}\n⌨ 𝐐𝐮𝐥𝐢𝐭𝐲 » {raw_text2}`\n\n**🔗 𝐔𝐑𝐋 »** `{url}`"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n{str(e)}\n⌘ 𝐍𝐚𝐦𝐞 » {name}\n⌘ 𝐋𝐢𝐧𝐤 » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞")

async def main():
    if WEBHOOK:
        # Start the web server
        app = await web_server()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

if __name__ == "__main__":
    print("""
    █░█░█ █▀█ █▀█ █▀▄ █▀▀ █▀█ ▄▀█ █▀▀ ▀█▀     ▄▀█ █▀ █░█ █░█ ▀█▀ █▀█ █▀ █░█   
    ▀▄▀▄▀ █▄█ █▄█ █▄▀ █▄▄ █▀▄ █▀█ █▀░ ░█░     █▀█ ▄█ █▀█ █▄█ ░█░ █▄█ ▄█ █▀█ """)

    # Start the bot and web server concurrently
    async def start_bot():
        await bot.start()

    async def start_web():
        await main()

    loop = asyncio.get_event_loop()
    try:
        # Create tasks to run bot and web server concurrently
        loop.create_task(start_bot())
        loop.create_task(start_web())

        # Keep the main thread running until all tasks are complete
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup
        loop.stop()


@bot.on_message(filters.command(["drm"]))
async def account_login(bot: Client, m: Message):

os.makedirs("Videos/", exist_ok=True)

def print_ascii_art():
    text = '\033[92m'"""
    ____  ____  __  ___   ____                      __                __
   / __ \/ __ \/  |/  /  / __ \____ _      ______  / /___  ____ _____/ /
  / / / / /_/ / /|_/ /  / / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / 
 / /_/ / _, _/ /  / /  / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  
/_____/_/ |_/_/  /_/  /_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/   
                                                                           
    """'\033[0m''\033[33m'f'v{__version__} by {__author__}, {__license__} @{__copyright__}\n''\033[0m'
    print(text)

class SERVICE(ABC):

    def __init__(self):
        self._remoteapi = "https://app.magmail.eu.org/get_keys"

    @staticmethod
    def c_name(name: str) -> str:
        for i in ["/", ":", "{", "}", "|"]:
            name = name.replace(i, "_")
        return name

    def get_date(self) -> str:
        tz = pytz.timezone('Asia/Kolkata')
        ct = datetime.datetime.now(tz)
        return ct.strftime("%d %b %Y - %I:%M%p")

    async def get_keys(self):
        async with ClientSession(headers={"user-agent": "okhttp"}) as session:
            async with session.post(self._remoteapi,
                                    json={"link": self.mpd_link}) as resp:
                if resp.status != 200:
                    LOGGER.error(f"Invalid request: {await resp.text()}")
                    return None
                response = await resp.json(content_type=None)
        self.mpd_link = response["MPD"]
        return response["KEY_STRING"]


class Download(SERVICE):

    def __init__(self, name: str, resl: str, mpd: str):
        super().__init__()
        self.mpd_link = mpd
        self.name = self.c_name(name)
        self.vid_format = f'bestvideo.{resl}/bestvideo.2/bestvideo'

        videos_dir = "Videos"
        encrypted_basename = f"{self.name}_enc"
        decrypted_basename = f"{self.name}_dec"

        self.encrypted_video = join(videos_dir, f"{encrypted_basename}.mp4")
        self.encrypted_audio = join(videos_dir, f"{encrypted_basename}.m4a")
        self.decrypted_video = join(videos_dir, f"{decrypted_basename}.mp4")
        self.decrypted_audio = join(videos_dir, f"{decrypted_basename}.m4a")
        self.merged = join(videos_dir, f"{self.name} - {self.get_date()}.mkv")

    async def process_video(self):
        key = await self.get_keys()
        if not key:
            LOGGER.error("Could not retrieve decryption keys.")
            return
        LOGGER.info(f"MPD: {self.mpd_link}")
        LOGGER.info(f"Got the Keys > {key}")
        LOGGER.info(f"Downloading Started...")
        if await self.__yt_dlp_drm() and await self.__decrypt(
                key) and await self.__merge():
            LOGGER.info(f"Cleaning up files for: {self.name}")
            await self.__cleanup_files()
            LOGGER.info(f"Downloading complete for: {self.name}")
            return self.merged
        LOGGER.error(f"Processing failed for: {self.name}")
        return None

    async def __subprocess_call(self, cmd: Union[str, List[str]]):
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            LOGGER.error(
                f"Command failed: {' '.join(cmd)}\nError: {stderr.decode()}")
            return False
        return True

    async def __yt_dlp_drm(self) -> bool:
        video_download = self.__subprocess_call(
            f'yt-dlp -k --allow-unplayable-formats -f "{self.vid_format}" --fixup never "{self.mpd_link}" --external-downloader aria2c --external-downloader-args "-x 16 -s 16 -k 1M" -o "{self.encrypted_video}"'
        )
        audio_download = self.__subprocess_call(
            f'yt-dlp -k --allow-unplayable-formats -f ba --fixup never "{self.mpd_link}" --external-downloader aria2c --external-downloader-args "-x 16 -s 16 -k 1M" -o "{self.encrypted_audio}"'
        )
        return await asyncio.gather(video_download, audio_download)

    async def __decrypt(self, key: str):
        LOGGER.info("Decrypting...")
        video_decrypt = self.__subprocess_call(
            f'mp4decrypt --show-progress {key} "{self.encrypted_video}" "{self.decrypted_video}"'
        )
        audio_decrypt = self.__subprocess_call(
            f'mp4decrypt --show-progress {key} "{self.encrypted_audio}" "{self.decrypted_audio}"'
        )
        return await asyncio.gather(video_decrypt, audio_decrypt)

    async def __merge(self):
        LOGGER.info("Merging...")
        return await self.__subprocess_call(
            f'ffmpeg -i "{self.decrypted_video}" -i "{self.decrypted_audio}" -c copy "{self.merged}"'
        )

    async def __cleanup_files(self):
        for file_path in [
                self.encrypted_video, self.encrypted_audio,
                self.decrypted_audio, self.decrypted_video
        ]:
            try:
                await remove(file_path)
            except Exception as e:
                LOGGER.warning(f"Failed to delete {file_path}: {str(e)}")


async def main(name, resl, mpd):
    downloader = Download(name, resl, mpd)
    await downloader.process_video()


if __name__ == "__main__":
    print_ascii_art()
    parser = argparse.ArgumentParser(
        description='Download and Decrypt DRM Video via Remote Key API')
    parser.add_argument('-l',
                        '--link',
                        type=str,
                        help='Valid MPD Link',
                        required=True)
    parser.add_argument('-r',
                        '--resl',
                        type=str,
                        help=
                        'Video Resolution (1/2/3) where 1 is highest and 3 is lowest available resolution',
                        default="1")
    parser.add_argument('-o',
                        '--name',
                        type=str,
                        help='Custom name for the output file',
                        default="output")
    args = parser.parse_args()
    asyncio.run(
        main(name=args.name, resl=args.resl, mpd=args.link))

