from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("TTN")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


class UserStates(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Calories")
async def age_set(message):
    age_question = "Введите свой возраст: "
    await message.answer(age_question)
    await UserStates.age.set()


@dp.message_handler(state=UserStates.age)
async def growth_set(message, state):
    await state.update_data(age=int(message.text))
    growth_question = "Введите свой рост в сантиметрах: "
    await message.answer(growth_question)
    #if not message.text.isdigit():
    #    await message.answer("Введено неверное значение. Повторите ввод.")
    await UserStates.growth.set()


@dp.message_handler(state=UserStates.growth)
async def weight_set(message, state):
    await state.update_data(growth=int(message.text))
    weight_question = "Введите свой вес: "
    await message.answer(weight_question)
    await UserStates.weight.set()


@dp.message_handler(state=UserStates.weight)
async def result(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    calories_spend = (10 * data['age'] + 6.25 * data['growth'] - 5 * data['weight'] + 5) * 1.375
    await message.answer(
        "Ваша суточная норма каллорий при слвбой физической активности: {} каллорий".format(int(calories_spend)))
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
