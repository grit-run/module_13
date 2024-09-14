from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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


keyb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton("Рассчитать")
button2 = KeyboardButton("Информация")
keyb1.row(button1, button2)

keyb2_inline = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button4 = InlineKeyboardButton(text="Формулы расчёта'", callback_data="formulas")
button5 = InlineKeyboardButton(text="Выход", callback_data="exit")
keyb2_inline.add(button3, button4, button5)

formula_explanation = ("Доработанный вариант формулы Миффлина-Сан Жеора учитывает степень физической активности "
                       "человека: для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A, "
                       "где A – это уровень активности человека, его различают обычно по пяти степеням физических "
                       "нагрузок в сутки")


@dp.message_handler(commands=['start'])
async def start(message):
    content = "Привет!"
    await message.answer(content, reply_markup=keyb1)


@dp.message_handler(text="Информация")
async def information(message):
    content = "Бот, позволяющий рассчитать суточное потребление калорий"
    await message.answer(content)


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию: ", reply_markup=keyb2_inline)


@dp.callback_query_handler(text="formulas")
async def formulas(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, formula_explanation)
    await callback_query.answer() @ dp.callback_query_handler(text="formulas")


@dp.callback_query_handler(text="exit")
async def exit_to_main(call):
    await call.message.answer("Обратно в начало", reply_markup=keyb1)


@dp.callback_query_handler(text="calories")
async def age_set(call):
    age_question = "Введите свой возраст: "
    await call.message.answer(age_question)
    await UserStates.age.set()


@dp.message_handler(state=UserStates.age)
async def growth_set(message, state):
    await state.update_data(age=int(message.text))
    growth_question = "Введите свой рост в сантиметрах: "
    await message.answer(growth_question)
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
