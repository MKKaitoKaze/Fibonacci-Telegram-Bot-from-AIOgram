import logging
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from time import sleep

logging.basicConfig(level=logging.INFO)
API_TOKEN = ''#Token Bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

class sost_kp(StatesGroup):
	get_int = State()

@dp.message_handler(commands=['start']) #Start command
async def send_welcome(message: types.Message):
	await message.reply("Привет!. \n Введите команду /help для получения команд бота")

@dp.message_handler(commands=['help']) #Help command
async def help_command(message: types.Message):
	await message.answer("Основно функционал этого бота: Вывод следующего числа Fibonacci, после введённого пользователем.\n Команды: \n /start \n /help \n /Fibonacci \n /buttons")

@dp.message_handler(commands=['buttons']) #Command to call a buttons
async def buttons_user(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text="Сайт колледжа", url="tehcollege.rv.ua")
	button2 = types.InlineKeyboardButton(text="Создатель бота", url="")
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	keyboard.add(button1, button2)
	await message.reply("Вот твои кнопки", reply_markup=keyboard)

@dp.message_handler(commands=['Fibonacci'], state="*") #Fibonacci function
async def get_user_text(message: types.Message):
	await message.answer("Введите число Fibonacci:")
	await  sost_kp.get_int.set()

@dp.message_handler(state=sost_kp.get_int) #Machine condition
async def second_verb_form(message: types.Message, state: FSMContext):
	F1 = 1
	F2 = 1
	if message.text.isdigit(): #cheking text for numbers
		while int(message.text) > F2:
			F1, F2 = F2, F1 + F2
		if int(message.text) == F2:
			await message.reply(F1 + F2)
		elif int(message.text) == 0:
			await message.answer("Веди число Fibonacci, оно должно быть больше 2") #false
			await message.answer_sticker(r'CAACAgIAAxkBAAEEr-lieP8OGe-6Bi3YrAcoFE51F_qrwAAC3AADeeg0LVO-y47bAv05JAQ') #Id and send sticker
			time.sleep(3)
			await message.answer("Попробуйте снова") #Send message after three minute expectations
		else:
			await message.answer("Число не в ряду Fibonacci") #false
			await message.answer_sticker(r'CAACAgIAAxkBAAEEr-lieP8OGe-6Bi3YrAcoFE51F_qrwAAC3AADeeg0LVO-y47bAv05JAQ')
			time.sleep(3)
			await message.answer("Попробуйте снова")
	await state.finish()
	
if __name__ == "__main__":
 executor.start_polling(dp,skip_updates=True) #continuous work
