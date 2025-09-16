import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv()
from api_methods.methods import *

TELE_API_TOKEN = os.getenv("TELE_API_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_message = """
Hi, I'm Hall 1 Jamband's Music Room Booking Bot! Here are the list of commands available:
/help - Show this help message
/read - Read all current booking entries
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELE_API_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', start)
    read_handler = CommandHandler('read', read_all_entries)

    application.add_handler(start_handler)
    application.add_handler(read_handler)
    
    application.run_polling()