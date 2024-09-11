import os, argparse
import time
import pytz
import datetime
import aiohttp
import aiofiles
import asyncio, shlex
import logging
import requests
import tgcrypto
import subprocess
import concurrent.futures
from utils import progress_bar
from os.path import join
from aiofiles.os import remove
from aiohttp import ClientSession
from typing import  Union, List
from pyrogram import Client, filters
from pyrogram.types import Message
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig

# pw_token = os.environ.get("token")
pw_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjIxMzM4MzkuOTM2LCJkYXRhIjp7Il9pZCI6IjYyYTYwYWM0MWEzMDk3MDAxMTMyMmZjOCIsInVzZXJuYW1lIjoiODI3MjA1NTA1NCIsImZpcnN0TmFtZSI6IlVOSVFVRSIsImxhc3ROYW1lIjoiVU5JUVVFIiwib3JnYW5pemF0aW9uIjp7Il9pZCI6IjVlYjM5M2VlOTVmYWI3NDY4YTc5ZDE4OSIsIndlYnNpdGUiOiJwaHlzaWNzd2FsbGFoLmNvbSIsIm5hbWUiOiJQaHlzaWNzd2FsbGFoIn0sImVtYWlsIjoibXVqZWVtMDAwQGdtYWlsLmNvbSIsInJvbGVzIjpbIjViMjdiZDk2NTg0MmY5NTBhNzc4YzZlZiJdLCJjb3VudHJ5R3JvdXAiOiJJTiIsInR5cGUiOiJVU0VSIn0sImlhdCI6MTcyMTUyOTAzOX0.SnzidAv5BzTeecU5MjrexdpEgZHMIgaQY49VcdblJQY"
#pw_token = "9550bce0978b3f1354cf0b4b0ad81afaf2e1283d372f8aa87749854701a12da6"

def duration(filename):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", filename
    ],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)

async def vision(url, name, cookies):

    ka = f'{name}.pdf'

    async with aiohttp.ClientSession() as session:

        async with session.get(url, cookies = cookies) as resp:

            if resp.status == 200:

                f = await aiofiles.open(ka, mode='wb')

                await f.write(await resp.read())

                await f.close()

    return ka     

async def download(url, name):
    ka = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka



async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'


def old_download(url, file_name, chunk_size=1024 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name

def init(self):
        self._remoteapi = "https://app.magmail.eu.org/get_keys"



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



def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"


async def download_video(url, cmd, name):
    download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
    global failed_counter
    print(download_cmd)
    logging.info(download_cmd)
    k = subprocess.run(download_cmd, shell=True)
    if "visionias" in cmd and k.returncode != 0 and failed_counter <= 10:
        failed_counter += 1
        await asyncio.sleep(5)
        await download_video(url, cmd, name)
    failed_counter = 0
    try:
        if os.path.isfile(name):
            return name
        elif os.path.isfile(f"{name}.webm"):
            return f"{name}.webm"
        name = name.split(".")[0]
        if os.path.isfile(f"{name}.mkv"):
            return f"{name}.mkv"
        elif os.path.isfile(f"{name}.mp4"):
            return f"{name}.mp4"
        elif os.path.isfile(f"{name}.mp4.webm"):
            return f"{name}.mp4.webm"

        return name
    except FileNotFoundError as exc:
        return os.path.isfile.splitext[0] + "." + "mp4"

def init(self, name: str, resl: str, mpd: str):
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

    async def subprocess_call(self, cmd: Union[str, List[str]]):
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

    async def yt_dlp_drm(self) -> bool:
        video_download = self.__subprocess_call(
            f'yt-dlp -k --allow-unplayable-formats -f "{self.vid_format}" --fixup never "{self.mpd_link}" --external-downloader aria2c --external-downloader-args "-x 16 -s 16 -k 1M" -o "{self.encrypted_video}"'
        )
        audio_download = self.__subprocess_call(
            f'yt-dlp -k --allow-unplayable-formats -f ba --fixup never "{self.mpd_link}" --external-downloader aria2c --external-downloader-args "-x 16 -s 16 -k 1M" -o "{self.encrypted_audio}"'
        )
        return await asyncio.gather(video_download, audio_download)

    async def decrypt(self, key: str):
        LOGGER.info("Decrypting...")
        video_decrypt = self.__subprocess_call(
            f'mp4decrypt --show-progress {key} "{self.encrypted_video}" "{self.decrypted_video}"'
        )
        audio_decrypt = self.__subprocess_call(
            f'mp4decrypt --show-progress {key} "{self.encrypted_audio}" "{self.decrypted_audio}"'
        )
        return await asyncio.gather(video_decrypt, audio_decrypt)

    async def merge(self):
        LOGGER.info("Merging...")
        return await self.__subprocess_call(
            f'ffmpeg -i "{self.decrypted_video}" -i "{self.decrypted_audio}" -c copy "{self.merged}"'
        )

    async def cleanup_files(self):
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

async def decrypt_file(file_path, key):
    file_path = "result"
    if not os.path.exists(file_path):
     return False
    with open(file_path, "r+b") as f:
      num_bytes = min(28, os.path.getsize(file_path))
      with mmap.mmap(f.fileno(), length=num_bytes, access=mmap.ACCESS_WRITE) as mmapped_file:
          for i in range(num_bytes):
              mmapped_file[i] ^= ord(key[i]) if i < len(key) else i
      return True

async def xor_encrypt_to_base64(input_str, key="123456"):
    key_len = len(key)
    encrypted_bytes = [
        ord(char) ^ ord(key[i % key_len]) for i, char in enumerate(input_str)
    ]
    base64_encrypted = base64.b64encode(bytes(encrypted_bytes))
    return base64_encrypted.decode('utf-8')
    success = decrypt_file(key)
    print("Decryption successful:", success)

async def get_pssh_kid(mpd_url: str, headers: dict = {}, cookies: dict = {}):
    """
    Get pssh, kid from mpd url
    headers: Headers if needed
    """
    pssh = ""
    kid = ""
    for i in range(3):
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(mpd_url, headers=headers, cookies=cookies)
                mpd_res = res.text
        except Exception as e:
            print("Error fetching MPD:", e)
            continue
        try:
            matches = re.finditer("<cenc:pssh>(.*)</cenc:pssh>", mpd_res)
            pssh = next(matches).group(1)
            kid = re.findall(r'default_KID="([\S]+)"', mpd_res)[0].replace("-", "")
        except Exception as e:
            print("Error extracting PSSH or KID:", e)
            continue
        else:
            break
    return pssh, kid


class Penpencil:
    otp_url = "https://api.penpencil.co/v1/videos/get-otp?key="
    penpencil_bearer = f'{pw_token}'

    headers = {
        "Host": "api.penpencil.co",
        "content-type": "application/json",
        "authorization": f"Bearer {pw_token}",
        "client-version": "11",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; PACM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36",
        "Client-Type": "WEB",
        "accept-encoding": "gzip",
    }

    @classmethod
    def encode_utf16_hex(cls, input_string: str) -> str:
        hex_string = ''.join(f"{ord(char):04x}" for char in input_string)
        return hex_string

    @classmethod
    def get_otp_key(cls, kid: str):
        xor_bytes = bytes(
            [
                ord(kid[i]) ^ ord(cls.penpencil_bearer[i % len(cls.penpencil_bearer)])
                for i in range(len(kid))
            ]
        )
        f = base64.b64encode(xor_bytes).decode("utf-8")
        print(f"Generated OTP Key: {f}")
        return f

    @classmethod
    def get_key(cls, otp: str):
        a = base64.b64decode(otp)
        b = len(a)
        c = [int(a[i]) for i in range(b)]
        d = "".join(
            [
                chr(c[j] ^ ord(cls.penpencil_bearer[j % len(cls.penpencil_bearer)]))
                for j in range(b)
            ]
        )
        print(f"Decoded Key: {d}")
        return d

    @classmethod
    async def get_keys(cls, kid: str):
        otp_key = cls.get_otp_key(kid)
        encoded_hex = cls.encode_utf16_hex(otp_key)
        print(f"Encoded Hex: {encoded_hex}")

        keys = []
        for i in range(3):
            try:
                async with httpx.AsyncClient(headers=cls.headers) as client:
                    otp_url = f"{cls.otp_url}{encoded_hex}&isEncoded=true"
                    resp = await client.get(otp_url)
                    otp_dict = resp.json()
            except Exception as e:
                print("Error fetching OTP:", e)
                continue
            try:
                otp = otp_dict["data"]["otp"]
                print(f"Received OTP: {otp}")
                key = cls.get_key(otp)
                keys = f"{kid}:{key}"
            except Exception as e:
                print("Error extracting key:", e)
                continue
            else:
                break
        return keys

    @classmethod
    async def get_mpd_title(cls, url: str):
        return url

    @classmethod
    async def get_mpd_keys_title(cls, url: str, keys: list = []):
        mpd_url = await cls.get_mpd_title(url)
        if keys:
            return mpd_url
        if mpd_url:
            pssh, kid = await get_pssh_kid(mpd_url)
            print("PSSH:", pssh)
            print("KID:", kid)

            # keys = await cls.get_keys(kid)
            # print("Keys:", keys)

            key = await cls.get_keys(kid)
            print("Key:", key)
        return mpd_url, key

async def get_drm_keys(url: str):
    mpd_url, key = await Penpencil.get_mpd_keys_title(url)
    return key

async def drm_download_video(url, quality, name, keys):

    print(keys)
    keys = keys.split(":")
    if len(keys) != 2:
        print("Error: Two keys must be provided separated by a colon.")
        return None
    key1, key2 = keys


    if quality =="1":
        nqual="720"

    elif quality=="2":
        nqual= "480" 

    elif quality =="3":
        nqual="360"

    elif quality=="4":
        nqual="240"
    else :
        nqual="480"                
  
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to N_m3u8DL-RE
        n_m3u8dl_re_path = os.path.join(current_dir, "N_m3u8DL-RE.exe")


        # Use N_m3u8DL-RE for decryption
        nurl = url.replace("master",f"master_{nqual}")
        subprocess.run([n_m3u8dl_re_path, "--auto-select", "--key", f"{key1}:{key2}", nurl, "-mt", "-M", "format=mp4", "--save-name", name], check=True)

        # Verify download
        result = os.system(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{name}.mp4"')
        if result != 0:
            print("Verification of the downloaded video failed.")
            return None

        print(f"Decryption and download successful with key {key1}.")
        return f"{name}.mp4"

    except FileNotFoundError as exc:
        print(f"File not found: {exc}")
        return os.path.splitext(name)[0] + ".mp4", None
        
async def send_doc(bot: Client, m: Message,cc,ka,cc1,prog,count,name):
    reply = await m.reply_text(f"Uploading » `{name}`")
    time.sleep(1)
    start_time = time.time()
    await m.reply_document(ka,caption=cc1)
    count+=1
    await reply.delete (True)
    time.sleep(1)
    os.remove(ka)
    time.sleep(3) 


async def send_vid(bot: Client, m: Message,cc,filename,thumb,name,prog):
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
    await prog.delete (True)
    reply = await m.reply_text(f"**⥣ Uploading ...** » `{name}`")
    try:
        if thumb == "no":
            thumbnail = f"{filename}.jpg"
        else:
            thumbnail = thumb
    except Exception as e:
        await m.reply_text(str(e))

    dur = int(duration(filename))

    start_time = time.time()

    try:
        await m.reply_video(filename,caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur, progress=progress_bar,progress_args=(reply,start_time))
    except Exception:
        await m.reply_document(filename,caption=cc, progress=progress_bar,progress_args=(reply,start_time))
    os.remove(filename)

    os.remove(f"{filename}.jpg")
    await reply.delete (True)
    
