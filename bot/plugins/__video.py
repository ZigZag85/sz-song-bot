#MIT License

#Copyright (c) 2021 slgeekshow

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from __future__ import unicode_literals
import os
import wget
import requests
from yt_dlp import YoutubeDL
from pyrogram import  filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from youtube_search import YoutubeSearch


from bot import bot as app

@app.on_message(filters.command(["video"]))
async def vsong(pbot, message):
    ydl_opts = {
        'format':'best',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        views = results[0]["views"]
        results[0]["url_suffix"]
        results[0]["views"]
        button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Watch On Youtube🎬", url=f"{link}")
        ],
        [
            InlineKeyboardButton("Search here 🔎", switch_inline_query_current_chat="")
        ]
    ]
    
    )
        rby = message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("📥 **downloading video...**")
        with YoutubeDL(ydl_opts) as ytdl:
            rep = f'🏷 **Video name**: [{title[:35]}]({link})\n⏱️ **Video Duration**: `{duration}`\n👁‍🗨 **Video Views**: `{views}`\n**🎧 Requested by:** {message.from_user.mention}\n 🤟Downloaded By : @szsongbot '
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"❌**YouTube Download Error !*** {str(e)}\n\n Go support chat👉 @slbotzone")
    preview = wget.download(thumbnail)
    await msg.edit("📤 **uploading video...**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=rep,
        reply_markup= button)
    try:
        os.remove(file_name)
        msg.delete()
    except Exception as e:
        print(e)
        
