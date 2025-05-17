ifrom telegram.ext import Application, CommandHandler
from logic import StrategyEngine
from snapshot import snapshot
from config import CONFIG

# Entry point
if __name__ == '__main__':
    # Build the bot application
    app = Application.builder() \
        .token(CONFIG['TELEGRAM_TOKEN']) \
        .build()

    # Register the /snapshot command
    app.add_handler(CommandHandler('snapshot', snapshot))

    # Schedule automated zone alerts
    engine = StrategyEngine()
    app.job_queue.run_repeating(
        lambda ctx: engine.evaluate(),
        interval=CONFIG['poll_interval'],
        first=10
    )

    # Start polling (blocks until interrupted)
    app.run_polling()
