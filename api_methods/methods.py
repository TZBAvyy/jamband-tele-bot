from telegram import Update
from telegram.ext import ContextTypes
import os
import requests
from datetime import datetime, timedelta

time_offset = timedelta(hours=8)
APPSCRIPT_API_URL = os.getenv("APPSCRIPT_API_URL")

async def read_all_entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Fetching all entries...")
    response = requests.get(url=APPSCRIPT_API_URL, headers=headers, allow_redirects=True)
    data = response.json()['data']
    chat_response = "Here are all the entries:"
    for entry in data:
        start = datetime.strptime(entry[1], "%Y-%m-%dT%H:%M:%S.000Z") + time_offset
        end = datetime.strptime(entry[2], "%Y-%m-%dT%H:%M:%S.000Z") + time_offset
        chat_response += f"""
{start.strftime("%d %b %Y [%H:%M]")} - {end.strftime("%d %b %Y [%H:%M]")}
Type: {entry[5]}
Booked by {entry[3]} [{entry[4]}] for {entry[6]} 
""" 
    await context.bot.send_message(chat_id=update.effective_chat.id, text=chat_response)