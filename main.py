from telegram.ext import Application, CommandHandler
from snapshot import snapshot

import asyncio

async def main():
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("snapshot", snapshot))
    await app.run_polling()
