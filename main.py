import asyncio
from logic import StrategyEngine

async def main():
    engine = StrategyEngine()
    while True:
        await engine.evaluate()
        await asyncio.sleep(engine.config.get("poll_interval", 60))

if __name__ == "__main__":
    asyncio.run(main())