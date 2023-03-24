from token2 import token3
from random import *
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command

def random_number():       #Генератор числа
    return randint(1,100)

BOT_TOKEN: str= token3

bot=Bot(BOT_TOKEN)
dp=Dispatcher()

ATTEMPTS=5
user={
    'game': False,
    'user_number': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}

@dp.message(Command(commands=['Start']))
async def command_start(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')

@dp.message(Command(commands=['help']))
async def commadn_help(message:Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')

@dp.message(Command(commands=['stat']))
async def command_stat(message:Message):
    await message.answer(f'Всего игр сыграно: {user["total_games"]}\n'
                         f'Игр выиграно: {user["wins"]}')

@dp.message(Command(commands=['cancel']))
async def command_cancel():
    if user['game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        user['game']=False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')

@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def positive_answer(message:Message):
    if not user['game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать!')
        user['game']=True
        user['user_number']= random_number()
        user['attempts']= ATTEMPTS
    else:
        await message.answer(
            'Пока мы играем в игру я могу\nреагировать только на числа от 1 до 100\nи команды /cancel и /stat')

@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def negative_answer(message:Message):
    if not user['game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100')

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def main_game(message:Message):
    if user['game']:
        if int(message.text) == user['user_number']:
            await message.answer('Ура!!! Вы угадали число!\n\n'
                                 'Может, сыграем еще?')
            user['game']=False
            user['total_games']+=1
            user['wins']+=1
        elif int(message.text) > user['user_number']:
            await message.answer('Мое число меньше')
            user['attempts']-=1
        elif int(message.text) < user['user_number']:
            await message.answer('Мое число больше')
            user['attempts'] -=1
        if user['attempts'] == 0:
            await message.answer('Вы проиграли!')
            user['game']=False
            user['total_games']+=1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')

@dp.message()
async def command_else(message: Message):
    if user['game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')

if __name__=='__main__':
    dp.run_polling(bot)
