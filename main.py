import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import BOT_API_TOKEN
from handlers.handlers import router

logging.basicConfig(level=logging.INFO, filename='log_info_bot.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = BOT_API_TOKEN

dp = Dispatcher()
dp.include_router(router)

async def main():

        try:
            bot = Bot(token = API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
            await dp.start_polling(bot)
            logging.info(f'Бот запущен. {bot.get_me()}')
        except Exception as e:
            logging.error(f'Ошибка при запуске бота: {e}')
            print('Ошибка при запуске бота')

if __name__ == '__main__':
        asyncio.run(main())


