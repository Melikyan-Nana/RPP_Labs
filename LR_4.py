from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import math

import os
import logging

# Активация системы логирования
logging.basicConfig(level=logging.INFO)

# Получение токена из переменных окружения
bot_token = os.getenv('API_TOKEN')

# Создание бота с токеном, который выдал в BotFather при регистрации бота
bot = Bot(token=bot_token)
# Инициализация диспетчера команд
dp = Dispatcher(bot, storage=MemoryStorage())

saved_state_global = {}


class Step1(StatesGroup):
    currency_name = State()
    rate = State()


class Step2(StatesGroup):
    currency_name2 = State()
    amount = State()


# Обработчик команды /save_currency
@dp.message_handler(commands=['save_currency'])
async def save_currency_command(message: types.Message):
    await Step1.currency_name.set()
    await message.reply("Введите название валюты")


# Обработка
@dp.message_handler(state=Step1.currency_name)
async def process_currency(message: types.Message, state: FSMContext):
    await state.update_data(currency_name=message.text)
    user_data = await state.get_data()
    await Step1.rate.set()
    await message.reply("Введите курс валюты к рублю")


@dp.message_handler(state=Step1.rate)
async def process_rate(message: types.Message, state: FSMContext):
    await state.update_data(rate=message.text)
    user_data = await state.get_data()
    saved_state_global['step1'] = user_data
    await state.finish()
    await message.reply("Курс валюты сохранен")


@dp.message_handler(commands=['convert'])
async def start_command2(message: types.Message):
    await Step2.currency_name2.set()
    await message.reply("Введите название валюты")


@dp.message_handler(state=Step2.currency_name2)
async def process_currency2(message: types.Message, state: FSMContext):
    await state.update_data(currency_name2=message.text)
    user_data = await state.get_data()
    await Step2.amount.set()
    await message.reply("Введите сумму в указанной валюте")


@dp.message_handler(state=Step2.amount)
async def process_convert(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)
    user_data = await state.get_data()
    await message.reply(math.ceil(int(user_data['amount']) / int(saved_state_global['step1']['rate'])))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp, skip_updates=True)
