import logging
import os
import psycopg2
import math
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat, KeyboardButton, ReplyKeyboardMarkup

import uvicorn
import psycopg2

from fastapi import FastAPI, HTTPException

app = FastAPI()


def calculate_rate(source: str, target: str, sum: int):
    conn = psycopg2.connect(
        host="localhost",
        database="rpp_lab_7",
        user="postgre",
        password="postgre"
    )

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT %(sum)s * crv.rate
            FROM public.currency_rates cr
            JOIN public.currency_rates_values crv ON cr.id = crv.currency_rate_id
            WHERE
                cr.base_currency = %(source)s
                AND crv.currency_code = %(target)s
        """, {"source": source, "target": target, "sum": sum})

        return cursor.fetchone()
    finally:
        conn.close()


@app.get("/convert")
async def convert(source: str, target: str, sum: int):
    """
        select 10 * crv.rate
        from public.currency_rates cr
        JOIN public.currency_rates_values crv ON cr.id = crv.currency_rate_id
        WHERE cr.base_currency = 'USD' AND crv.currency_code = 'RUB'
        ;

    "param_source": ""
    "param_target": ""
    :param sum:
    :return:
    """

    try:
        return {"converted": calculate_rate(source=source, target=target, sum=sum)[0]}
    except:
        raise HTTPException(status_code=500, detail="Что-то пошло не так")


@app.post("/load")
async def load(payload: dict):
    """
    payload =
    {
        "base_currency": "USD",
        "rates": [
            {
                "code": "RUB",
                "rate": 60
            },
            {
                "code": "TEH",
                "rate": 10
            }
        ]
    }

    :param payload: JSON
    :return: OK
    """
    base_currency = payload["base_currency"]
    rates = payload["rates"]
    conn = psycopg2.connect(
        host="localhost",
        database="rpp_lab_7",
        user="postgre",
        password="postgre"
    )

    check_currency_lack(base_currency=base_currency)

    try:
        cursor = conn.cursor()
        cursor.execute("insert into currency_rates(base_currency) values (%(base_currency)s) RETURNING id",
                       {"base_currency": base_currency})

        base_currency_id = cursor.fetchone()

        # То что мы будем сохранять в currency_rates_values
        # {
        #     "currency_code": element.code,
        #     "rate": element.rate,
        #     "currency_rate_id": base_currency_id
        # }
        for element in rates:
            cursor.execute("insert into currency_rates_values (currency_code, rate, currency_rate_id) "
                           "values (%(currency_code)s, %(rate)s, %(currency_rate_id)s)",
                           {
                               "currency_code": element["code"],
                               "rate": element["rate"],
                               "currency_rate_id": base_currency_id
                           })

        conn.commit()
        print(f"base_currency: {base_currency}; rates: {rates}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Не удалось сохранить данные")
    finally:
        conn.close()


def check_currency_lack(base_currency: str):
    conn = psycopg2.connect(
        host="localhost",
        database="rpp_lab_7",
        user="postgre",
        password="postgre"
    )
    cursor = conn.cursor()
    # Запрашиваем все имеющиеся валюты
    cursor.execute("SELECT 1 FROM currency_rates WHERE base_currency = %(base_currency)s",
                   {"base_currency": base_currency})
    found_currencies = cursor.fetchall()
    conn.close()
    # Если валюта уже существует, то сервис возвращает ошибку 500
    if len(found_currencies) == 1:
        raise HTTPException(status_code=500, detail="Валюта уже существует")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10610)


def get_currency_rates():
    conn = psycopg2.connect(
        host="localhost",
        database="rpp_lab_7",
        user="postgre",
        password="postgre"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT currency_name, rate FROM currencies")
    rows = cursor.fetchall()
    conn.close()
    logging.info(rows)
    return rows


# Активация системы логирования
logging.basicConfig(level=logging.INFO)

# Получение токена из переменных окружения
bot_token = os.getenv('TG_API_TOKEN')

# Создание бота с токеном, который выдал в BotFather при регистрации бота
bot = Bot(token=bot_token)

# Инициализация диспетчера команд
dp = Dispatcher(bot, storage=MemoryStorage())

saved_state_global = {}


class ManageStateGroup(StatesGroup):
    Add_currency_name_state = State()
    Add_currency_rate_state = State()
    Edit_currency_name_state = State()
    Edit_currency_rate_state = State()
    Delete_currency_state = State()


class Step2(StatesGroup):
    currency_name2 = State()
    amount = State()


# Получение чат-id пользователя, который прислал сообщение
@dp.message_handler(commands=['start'])
async def add_chat_id(message: types.Message):
    await message.reply("Добро пожаловать в бота")
    chat_id = message.chat.id


def add_chat_id(chat_id):
    conn = psycopg2.connect(
            host="localhost",
            database="rpp_lab_7",
            user="postgre",
            password="postgre"
        )
    cursor = conn.cursor()
    cursor.execute("""insert into admin (id, chat_id) VALUES  (:id, :chat_id) """,
                   {"id": id, "chat_id": chat_id})


@dp.message_handler(commands=['get_currencies'])
async def viewing_recorded_currencies(message: types.Message):
    currencies = get_currency_rates()
    response = ""
    if currencies:
        response = "Курсы валют к рублю:\n"
        for rate in currencies:
            response += f"{rate[0]}: {rate[1]} руб.\n"
    else:
        response = "Курсы валют не найдены"
    await bot.send_message(message.chat.id, response)


# Команды для админов
admin_commands = [
    BotCommand(command="/manage_currency", description="MANAGE CURRENCY"),
    BotCommand(command="/start", description="START"),
    BotCommand(command="/get_currencies", description="GET CURRENCIES"),
    BotCommand(command="/convert", description="CONVERT")
]

# Команды для всех пользователей
user_commands = [
    BotCommand(command="/start", description="START"),
    BotCommand(command="/get_currencies", description="GET CURRENCIES"),
    BotCommand(command="/convert", description="CONVERT")
]

# Тут должен быть только числовой формат
ADMIN_ID = [5278277671]


async def setup_bot_commands(dispatcher: Dispatcher):
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    for admin in ADMIN_ID:
        await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))


# Текст кнопок является также и командой, которую обработает бот
add_currency = KeyboardButton(text='Добавить валюту')
delete_currency = KeyboardButton(text='Удалить валюту')
change_rate = KeyboardButton(text='Изменить валюту')

markup = ReplyKeyboardMarkup(resize_keyboard=True).row(add_currency, delete_currency, change_rate)


# Обработчик команды /add_currency
@dp.message_handler(regexp=r"^Добавить валюту$")
async def add_currency_command(message: types.Message):
    """
    Обрабатывает любую строку, которая удовлетваряет паттерну 'Добавить валюту'
    Устанавливает состояние Step1.currency_name (Задание имени валюты для конвертации)

    :param message: сообщение от пользователя
    :return: ничего
    """
    await ManageStateGroup.Add_currency_name_state.set()
    await message.reply("Введите название валюты")


# Обработчик команды /delete_currency
@dp.message_handler(regexp=r"^Удалить валюту$")
async def command_delete_currency(message: types.Message):
    await message.reply("Введите название валюты, которую вы хотите удалить")
    await ManageStateGroup.Delete_currency_state.set()


@dp.message_handler(state=ManageStateGroup.Delete_currency_state)
async def process_delete_currency(message: types.Message, state: FSMContext):
    currency_name = message.text
    try:
        delete_currency_in_database(currency_name=currency_name)
        await message.answer("Валюта удалена")
    except Exception as e:
        logging.error("Ошибка удаления из БД", e)
        # Если у ошибки есть сообщение, то выводим его пользователю в качестве причины ошибки
        error_message = e.args[0] if len(e.args) > 0 else "Причина неизвестна"
        await message.answer(f"Валюту не удалось удалить: {error_message}")
    finally:
        await state.finish()


def delete_currency_in_database(currency_name: str):
    conn = psycopg2.connect(
            host="localhost",
            database="rpp_lab_7",
            user="postgre",
            password="postgre"
        )
    cursor = conn.cursor()
    # Запрашиваем все имеющиеся валюты, по параметру currency_name
    cursor.execute("SELECT 1 FROM currencies WHERE currency_name = %(currency_name)s", {"currency_name": currency_name})
    found_currencies = cursor.fetchall()

    if len(found_currencies) == 0:
        raise Exception("Валюты не существует")

    cursor.execute(
        "DELETE FROM currencies WHERE currency_name = %(currency_name)s", {"currency_name": currency_name}
    )

    # Для изменения валюты сделать ```UPDATE currencies SET rate=%(rate)s WHERE currency_name=%(currency_name)s```
    conn.commit()
    conn.close()


# Обработчик команды /edit_currency
@dp.message_handler(regexp=r"^Изменить валюту$")
async def command_edit_currency(message: types.Message):
    await message.reply("Введите название валюты, которую вы хотите изменить")
    await ManageStateGroup.Edit_currency_name_state.set()


@dp.message_handler(state=ManageStateGroup.Edit_currency_name_state)
async def command_edit_currency(message: types.Message, state: FSMContext):
    await message.reply("Введите новый курс валюты")
    await state.update_data(currency_name=message.text)
    await ManageStateGroup.Edit_currency_rate_state.set()


@dp.message_handler(state=ManageStateGroup.Edit_currency_rate_state)
async def process_edit_currency(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    rate = message.text
    try:
        edit_currency_in_database(currency_name=state_data['currency_name'], rate=rate)
        await message.answer("Курс валюты изменен")
    except Exception as e:
        logging.error("Ошибка взаимодействия с БД", e)
        # Если у ошибки есть сообщение, то выводим его пользователю в качестве причины ошибки
        error_message = e.args[0] if len(e.args) > 0 else "Причина неизвестна"
        await message.answer(f"Не удалось изменить курс валюты: {error_message}")
    finally:
        await state.finish()


def edit_currency_in_database(currency_name: str, rate: int):
    conn = psycopg2.connect(
            host="localhost",
            database="rpp_lab_7",
            user="postgre",
            password="postgre"
        )
    cursor = conn.cursor()
    # Запрашиваем все имеющиеся валюты, по параметру currency_name
    cursor.execute("SELECT 1 FROM currencies WHERE currency_name = %(currency_name)s", {"currency_name": currency_name})
    found_currencies = cursor.fetchall()

    if len(found_currencies) == 0:
        raise Exception("Валюты не существует")

    cursor.execute(
        "UPDATE currencies SET rate=%(rate)s WHERE currency_name=%(currency_name)s",
        {"currency_name": currency_name, "rate": rate}
    )

    # Для изменения валюты сделать ```UPDATE currencies SET rate=%(rate)s WHERE currency_name=%(currency_name)s```
    conn.commit()
    conn.close()


# Обработка
@dp.message_handler(state=ManageStateGroup.Add_currency_name_state)
async def process_currency(message: types.Message, state: FSMContext):
    await state.update_data(currency_name=message.text)
    user_data = await state.get_data()
    await ManageStateGroup.Add_currency_rate_state.set()
    await message.reply("Введите курс валюты к рублю")


def add_currency_in_database(currency_name: str, rate: int):
    conn = psycopg2.connect(
            host="localhost",
            database="rpp_lab_7",
            user="postgre",
            password="postgre"
        )
    cursor = conn.cursor()
    # Запрашиваем все имеющиеся валюты, по параметру currency_name
    cursor.execute("SELECT 1 FROM currencies WHERE currency_name = %(currency_name)s", {"currency_name": currency_name})
    found_currencies = cursor.fetchall()

    # Если найдена хотя бы одна валюта, currency_name которой совпадает с тем, что мы пытаемся сохранить, тогда
    # кидаем исключение с текстом "Валюта уже существует"
    if len(found_currencies) > 0:
        raise Exception("Валюта уже существует")

    cursor.execute(
        "INSERT INTO currencies(currency_name, rate) VALUES (%(currency_name)s, %(rate)s)",
        {
            "currency_name": currency_name,
            "rate": rate
        }
    )
    conn.commit()
    conn.close()


@dp.message_handler(state=ManageStateGroup.Add_currency_rate_state)
async def process_rate(message: types.Message, state: FSMContext):
    await state.update_data(rate=message.text)
    user_data = await state.get_data()
    saved_state_global['step1'] = user_data

    try:
        # Добавляем новую валюту в базу данных
        add_currency_in_database(currency_name=user_data['currency_name'], rate=user_data['rate'])
        # Если все прошло успешно, тогда выводим сообщение "Курс валюты сохранен"
        await message.reply("Курс валюты сохранен")
    except Exception as e:
        # Если получаем ошибки, то логируем их
        logging.error("Ошибка записи в БД", e)
        # Если у ошибки есть сообщение, то выводим его пользователю в качестве причины ошибки
        error_message = e.args[0] if len(e.args) > 0 else "Причина неизвестна"
        await message.reply(f"Курс валюты не удалось сохранить: {error_message}")
    finally:
        await state.finish()


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
    await message.reply(math.floor(int(user_data['amount']) * int(saved_state_global['step1']['rate'])))


@dp.message_handler(commands=['manage_currency'])
async def process_manage_currency(message: types.Message):
    await message.reply(text="Выберите операцию из доступных", reply_markup=markup)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)v
