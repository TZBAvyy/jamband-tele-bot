import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()
TELE_API_TOKEN = os.getenv("TELE_API_TOKEN")
APPSCRIPT_API_URL = os.getenv("APPSCRIPT_API_URL")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

timezone = "Asia/Singapore"
time_offset = timedelta(hours=8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def read_all_entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.get(url=APPSCRIPT_API_URL, headers=headers, allow_redirects=True)
    data = response.json()['data']
    chat_response = "Here are all the entries:"
    for entry in data:
        print(entry) #2025-09-10T09:00:00.000Z
        start = datetime.strptime(entry[1], "%Y-%m-%dT%H:%M:%S.000Z") + time_offset
        end = datetime.strptime(entry[2], "%Y-%m-%dT%H:%M:%S.000Z") + time_offset
        chat_response += f"""
{start} - {end} | Booked by {entry[3]} [{entry[4]}] for {entry[6]} | Type: {entry[5]}
""" 
    await context.bot.send_message(chat_id=update.effective_chat.id, text=chat_response)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELE_API_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    read_handler = CommandHandler('read', read_all_entries)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(read_handler)
    
    application.run_polling()