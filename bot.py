import asyncio
import logging
import sys
from os import getenv
import main as weather
import db
import draw

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

#---------------------------------------------------------
# Telegram bot by Nikita (Xenyzz) Sersts :)
#---------------------------------------------------------

load_dotenv()
TOKEN = getenv("TELEGRAM_TOKEN")
dp = Dispatcher()
dp.include_router(Router())


class Form(StatesGroup):
    default_city = State()
    weather_taking = State()
    weather_delete = State()


def cities_kb(*, user_id: int):
    kb_list = []
    for city in db.print_users_cities(user_id=user_id):
        kb_list.append([KeyboardButton(text=city)])
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb_list, one_time_keyboard=True)
    return keyboard

def welcome_kb():
    kb_list = [
        [KeyboardButton(text="Add a city🌆"), KeyboardButton(text="Delete a city ⛔️")],
        [KeyboardButton(text="Check the weather☁️"), KeyboardButton(text="Check the weather for specific city🌡")]
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb_list)
    return keyboard


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n", reply_markup=welcome_kb())


@dp.message(F.text == "Add a city🌆")
async def set_default_city(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.default_city)
    await message.answer("Sure! Enter your city name below: ")

@dp.message(Form.default_city)
async def process_city_setting(message: Message, state: FSMContext) -> None:
    if not weather.get_geo(message.text):
        await state.set_state(Form.default_city)
        await message.answer("Wrong city! Try again!")
        return None
    db.link_user_and_city(city=message.text, user_id=message.from_user.id, user_name=message.from_user.full_name)
    await message.answer("Success!", reply_markup=welcome_kb())
    await state.clear()


@dp.message(F.text == "Check the weather☁️")
async def check_weather_for_cities(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    await state.set_state(Form.weather_taking)
    await message.answer("Sure! Choose the city!\n", reply_markup=cities_kb(user_id=user_id))

@dp.message(Form.weather_taking)
async def process_check_weather(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    weather_info = weather.get_weather(city=message.text)
    draw.draw_image(weather_info, user_id=user_id)
    photo = FSInputFile(path=f"weather_final{user_id}.png")
    await message.bot.send_photo(chat_id=message.chat.id, photo=photo)
    await state.clear()


@dp.message(F.text == "Delete a city ⛔️")
async def delete_a_city(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    await state.set_state(Form.weather_delete)
    await message.answer("Sure! Choose the city to delete!\n", reply_markup=cities_kb(user_id=user_id))

@dp.message(Form.weather_delete)
async def process_delete_city(message: Message, state: FSMContext) -> None:
    if db.unlink_user_and_city(city=message.text, user_id=message.from_user.id):
        await message.answer("City is deleted!", reply_markup=welcome_kb())
    else:
        await message.answer("City is not deleted! Non-existent city", reply_markup=welcome_kb())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
