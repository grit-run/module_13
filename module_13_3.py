from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


load_dotenv()
BOT_TOKEN = os.getenv("TTN")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start(message):
    content = "Привет! Я бот помогающий твоему здоровью."
    await message.answer(content)

@dp.message_handler()
async def all_massages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


