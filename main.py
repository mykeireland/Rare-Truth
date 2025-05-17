from telegram.ext import Application, CommandHandler
from logic import StrategyEngine
from snapshot import snapshot
from config import CONFIG

if __name__ == '__main__':
    app = Application.builder().token(CONFIG['TELEGRAM_TOKEN']).build()
    # snapshot command
    app.add_handler(CommandHandler('snapshot', snapshot))
    # recurring zone alerts
    engine = StrategyEngine()
    app.job_queue.run_repeating(
        lambda ctx: engine.evaluate(),
        interval=CONFIG['poll_interval'],
        first=10
    )
    app.run_polling()
