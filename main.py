# coding=utf-8
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


bot = Bot('6072475695:AAHpvdUEZN_AqD0Htilfnljgx366kThedFc')
dp = Dispatcher(bot, storage=MemoryStorage())
conn = sqlite3.connect('info.db') # Потом поменяем
sql = conn.cursor()

def start_kb():
    button_reg = KeyboardButton('Хз')
    button_enter = KeyboardButton('Тоже хз')
    st_kn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_reg, button_enter)
    return st_kn


# Старт бота
@dp.message_handler(commands=['start'], state=None)
async def bot_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Здравствуйте! \n"
                                                 "Я бот", reply_markup=start_kb())


if __name__ == '__main__':
    executor.start_polling(dp)