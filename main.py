import os
import asyncio
from telegram.ext import Application, CommandHandler
from logic import StrategyEngine
from snapshot import snapshot
from config import CONFIG

async def main():
    app = Application.builder().token(CONFIG['TELEGRAM_TOKEN']).build()

    # Register snapshot command
    app.add_handler(CommandHandler('snapshot', snapshot))

    # Schedule zone alerts
    engine = StrategyEngine()
    app.job_queue.run_repeating(
        lambda ctx: engine.evaluate(),
        interval=CONFIG['poll_interval'],
        first=10
    )

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
