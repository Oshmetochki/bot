

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from token2 import token3

API_TOKEN: str = token3

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')

async def stickers(message: Message):
    await message.answer_sticker(message.sticker.file_id)

async def send_echo(message: Message):
    await message.answer(text=message.text)



dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(stickers)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)