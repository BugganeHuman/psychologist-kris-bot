import asyncio
from aiogram import Bot, Dispatcher
import os
import handlers
from dotenv import load_dotenv


load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))

dp = Dispatcher()


async def main():
    dp.include_router(handlers.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
