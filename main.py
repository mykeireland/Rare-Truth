import os
from telegram.ext import Application, CommandHandler
from logic import StrategyEngine
from snapshot import snapshot

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = Application.builder().token(token).build()

    # 1) On-demand snapshot
    app.add_handler(CommandHandler("snapshot", snapshot))

    # 2) Scheduled zone alerts
    engine = StrategyEngine()
    app.job_queue.run_repeating(
        lambda ctx: engine.evaluate(),
        interval=engine.config["poll_interval"],
        first=10
    )

    app.run_polling()

if __name__ == "__main__":
    main()