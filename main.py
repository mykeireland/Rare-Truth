import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from snapshot import snapshot
from config import CONFIG

async def main():
    print("🛠️ Booting up...")
    app = ApplicationBuilder().token(CONFIG["telegram_token"]).build()
    app.add_handler(CommandHandler("snapshot", snapshot))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
