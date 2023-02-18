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

def Parser():
    return "123"

def start_kb():
    button_1 = bt('Учебные программы')
    button_2 = bt('Поступление')
    button_3 = bt('Проживание')
    button_4 = bt('Другое')
    st_kn = kb().add(button_1, button_2, button_3, button_4)
    return st_kn

# Старт бота
@dp.message_handler(commands=['start'], state=None)
async def bot_start(message: types.Message):
    await bot.send_message(message.from_user.id, """Здравствуйте! Это телеграм-бот для интересующихся поступлением в университет Innopolis абитуриентов. Вам нужно выбрать несколько категорий. Что бы вы хотели узнать?""", reply_markup=start_kb())
    await Queue.first.set()

def HandlerFirst(message):
    answers = {
        "учебные программы": ["""""", kb().add(bt('Бакалавриат'), bt('Магистратура'), bt('Аспирантура'))],
        "поступление": ["""Здесь находится информация о поступлении в университет Innopolis. Дальше вам требуется снова выбрать одну из категорий.""", 
                        kb().add(bt('День открытых дверей'), bt('Подать заявку'), bt('Отбор'), 
                        bt('Платное обучение'), bt('Грант'), bt('Олимпиадные бонусы'), bt('Документы'))],
        "проживание": ["Пук-Хрюк", kb().add(bt('Кампус университета Иннополис'), bt('Студенческая жизнь'), bt('Город Иннополис'))],
        "другое": ["Пук-Хрюк", kb().add(bt('Отзывы'), bt('Новости и события'), bt('Часто задаваемые вопросы'), bt('Контакты'), bt('Статистика за 5 лет'))],
    }
    if message.lower() not in answers:
        return ["", ""]
    return answers[message.lower()]

@dp.message_handler(state=Queue.first)
async def First(message: types.Message, state: FSMContext):
    handler = HandlerFirst(message.text)
    if (handler == ["", ""]):
        # Провекра остальных вложен.
        await bot.send_message(message.from_user.id, "Простите, но вы ввели некорректный запрос. Попробуйте снова", reply_markup=start_kb())
    else:
        handler[1] = handler[1].add(bt('Назад'))
        Queue.first = handler
        await bot.send_message(message.from_user.id, handler[0], reply_markup=handler[1])
        await Queue.next()

def HandlerSecond(message): # None - клавиатура пред.
    answers = {
        "бакалавриат": ["Пук-Хрюк", kb().add(bt("Профили подготовки"), bt("Структура обучения"))],
        "магистратура": ["Пук-Хрюк", kb().add()],
        "аспирантура": ["Пук-Хрюк", kb().add()],
        "день открытых дверей": ["Пук-Хрюк", None],
        "подать заявку": ["Пук-Хрюк", None],
        "отбор": ["Пук-Хрюк", None],
        "платное обучение": ["Пук-Хрюк", None],
        "грант": ["Пук-Хрюк", None],
        "олимпиадные бонусы": ["Пук-Хрюк", None],
        "документы": ["Пук-Хрюк", None],
        "кампус университета иннополис": ["Пук-Хрюк", None],
        "студенческая жизнь": ["Пук-Хрюк", None],
        "город иннополис": ["Пук-Хрюк", None],
        "отзывы": ["Пук-Хрюк", kb().add()],
        "новости и события": ["Пук-Хрюк", kb().add()],
        "часто задаваемые вопросы": ["Пук-Хрюк", kb().add()],
        "контакты": ["Пук-Хрюк", kb().add()],
        "cтатистика за 5 лет": ["Пук-Хрюк", None],
        "назад": ["Back", None]
    }
    if message.lower() not in answers:
        return ["", ""]
    return answers[message.lower()]

@dp.message_handler(state=Queue.second)
async def Second(message: types.Message, state: FSMContext):
    handler = HandlerSecond(message.text)
    if (handler == ["", ""]):
        # Провекра остальных вложен.
        await bot.send_message(message.from_user.id, "Простите, но вы ввели некорректный запрос. Попробуйте снова", reply_markup=Queue.first[1])
    else:
        if (handler[0] == "Back"):
            await bot.send_message(message.from_user.id, "Хрюк", reply_markup=start_kb())
            await Queue.previous()
        elif (handler[1] is None):
            handler[1] = Queue.first[1]
            await bot.send_message(message.from_user.id, Parser(), reply_markup=handler[1])
        else:
            handler[1] = handler[1].add(bt('Назад'))
            Queue.second = handler
            await bot.send_message(message.from_user.id, handler[0], reply_markup=handler[1])
            await Queue.next()

def HandlerThird(message): # None - клавиатура пред.
    answers = {
        
    }
    if message.lower() not in answers:
        return ["", ""]
    return answers[message.lower()]

@dp.message_handler(state=Queue.third)
async def Second(message: types.Message, state: FSMContext):
    handler = HandlerThird(message.text)
    if (handler == ["", ""]):
        # Провекра остальных вложен.
        await bot.send_message(message.from_user.id, "Простите, но вы ввели некорректный запрос. Попробуйте снова", reply_markup=Queue.first[1])
    else:
        if (handler[0] == "Back"):
            await bot.send_message(message.from_user.id, "Хрюк", reply_markup=Queue.first[1])
            await Queue.previous()
        elif (handler[1] is None):
            handler[1] = Queue.first[1]
            await bot.send_message(message.from_user.id, Parser(), reply_markup=handler[1])
        else:
            Queue.second = handler
            await bot.send_message(message.from_user.id, handler[0], reply_markup=handler[1])
            await Queue.next()

if __name__ == '__main__':
    executor.start_polling(dp)