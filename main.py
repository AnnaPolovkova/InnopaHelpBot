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

class Queue(StatesGroup):
    first = State()
    second = State()
    third = State()

def kb():
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

def bt(message):
    return KeyboardButton(message)

def start_kb():
    button_1 = bt('Учебные программы')
    button_2 = bt('Проживание')
    button_3 = bt('Приемная кампания')
    button_4 = bt('Другое')
    st_kn = kb().add(button_1, button_2, button_3, button_4)
    return st_kn

async def g(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите логин')

@dp.message_handler(text=['Вход'], state=None)
async def bot_enter(message: types.Message):
    g(message)

# Старт бота
@dp.message_handler(commands=['start'], state=None)
async def bot_start(message: types.Message):
    await bot.send_message(message.from_user.id, """Здравствуйте!\n
                           Это телеграм-бот для интересующихся поступлением в университет Innopolis абитуриентов.\n
                           Вам нужно выбрать несколько категорий.\nЧто бы вы хотели узнать?""", reply_markup=start_kb())
    await Queue.first.set()

def HandlerFirst(message):
    answers = {
        "учебные программы": ("Пук-Хрюк", kb().add(bt('Бакалавриат'), bt('Магистратура'), bt('Аспирантура'))),
        "поступление": ("Пук-Хрюк", 
                        kb().add(bt('День открытых дверей'), bt('Подать заявку'), bt('Отбор'), 
                        bt('Платное обучение'), bt('Грант'), bt('Олимпиадные бонусы'), bt('Документы'))),
        "проживание": ("Пук-Хрюк", kb().add(bt('Кампус университета Иннополис'), bt('Студенческая жизнь'), bt('Город Иннополис'))),
        "другое": ("Пук-Хрюк", kb().add(bt('Отзывы'), bt('Новости и события'), bt('Часто задаваемые вопросы'), bt('Контакты'), bt('Статистика за 5 лет'))),
    }
    return answers[message.lower()]

@dp.message_handler(state=Queue.first)
async def what_edit_profile(message: types.Message, state: FSMContext):
    handler = HandlerFirst(message.text)
    await bot.send_message(message.from_user.id, handler[0], reply_markup=handler[1])


if __name__ == '__main__':
    executor.start_polling(dp)