import logging
from email import message

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputFile
from pytube import YouTube
import math


import physics
from physics import topics

TOKEN = ''
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = []


@dp.message_handler(commands='start')
async def start(message: types.Message, physic=None):
    physic_choice = InlineKeyboardMarkup()
    for physic in topics:
        button = InlineKeyboardButton(text=physic, callback_data=physic)
        physic_choice.add(button)
    await message.answer(text='Привіт, я бот про фізику🤓\n Oбери тему з фізики,'
                              ' про яку хочеш дізнатися',
                         reply_markup=physic_choice)
    await message.answer(text='ось список програмок зі слешами\n'
                              '/start = запуск бота\n'
                              '/calc1 = калькулятор що рахує 2 закон ньютона\n'
                              '/calc2 = калькулятор що рахує формулу тонкої лінзи\n'
                              '/calc3 = калькулятор  що рахує оптичну силу лінзи\n'
                              '/calc4 = калькулятор що рахує закон кулона')



@dp.callback_query_handler()
async def get_physic_info(callback_query: types.CallbackQuery, physic=None):
    if callback_query.data in topics.keys():
        with open(topics[callback_query.data]['photo'], 'rb') as ph:
            photo = InputFile(ph)
            await bot.send_photo(callback_query.message.chat.id, photo)
        formulas = topics[callback_query.data]['formulas']
        law = topics[callback_query.data]['law']
        video = topics[callback_query.data]['video_lesson']
        message = f"<b>Video lesson :</b> {video} \n\n<b>Forlmula(S):</b> {formulas}\n\n<b>Law:</b> {law}"
        await bot.send_message(callback_query.message.chat.id, message, parse_mode='html')


#команда яка б рахувала 2 закон ньютона,2 закон = F= m*a
m = 0
@dp.message_handler(commands='calc1')
async def add(massage: types.Message, state: FSMContext):
    await massage.answer(text='2 закон Ньютона це F = m * a\n'
                              'щоб порахувати силу введіть цифрові данні\n'
                              '1.введіть масу: ')
    await state.set_state('sent_masa_of_n')

@dp.message_handler(state='sent_masa_of_n')
async def masa(massage: types.Message, state: FSMContext):
    global m
    if massage.text.isnumeric():
        m = int(massage.text)
        await massage.answer(text='2.введіть прискорення: ')
        await state.set_state('sent_a_of_n')
    else:
        await massage.answer(text='ви ввели неправельні данні будь ласка ведіть ЦИФРОВЕ значення')

@dp.message_handler(state='sent_a_of_n')
async def masa2(message: types.Message, state: FSMContext):
    global a
    if message.text.isnumeric():
        a = int(message.text)
        f = a * m
        await message.answer(text=f'відповідь: {f}')
        await state.finish()
    else:
        await message.answer(text='ви ввели неправельні данні будь ласка ведіть ЦИФРОВЕ значення')

#формула тонкої лінзи 1/F=(1/d)+(1/f)
d = 0
@dp.message_handler(commands='calc2')
async def add(massage: types.Message, state: FSMContext):
    await massage.answer(text='формула тонкої лінзи 1/F = (1/d) + (1/f)\n'
                              'щоб порахувати формулу введіть цифрові данні\n'
                              '1.введіть відстань від предмета до лінзи це d: ')
    await state.set_state('sent_d')

@dp.message_handler(state='sent_d')
async def masa(massage: types.Message, state: FSMContext):
    global d
    if massage.text.isnumeric():
        d = int(massage.text)
        await massage.answer(text='2.введіть відстань від зображення до лінзи це f: ')
        await state.set_state('sent_f')
    else:
        await massage.answer(text='ви ввели неправельні данні будь ласка ведіть ЦИФРОВЕ значення')

@dp.message_handler(state='sent_f')
async def masa2(message: types.Message, state: FSMContext):
    global f
    if message.text.isnumeric():
        f = int(message.text)
        F=(1/d)+(1/f)
        await message.answer(text=f'відповідь: {F}')
        await state.finish()
    else:
        await message.answer(text='ви ввели неправельні данні будь ласка ведіть ЦИФРОВЕ значення')

#команда яка рахує формулу оптичної лінзи D = 1/F
q = 0
@dp.message_handler(commands='calc3')
async def add(message: types.Message, state: FSMContext):
    await message.answer(text='формула сили лінзи D = 1/F\n'
                              'щоб порахувати формулу введіть цифрові данні\n'
                              '1.введіть фокусну відстань лінзи: ')
    await state.set_state('sent_q')

@dp.message_handler(state='sent_q')
async def masa(message: types.Message, state: FSMContext):
    global q
    if message.text.isnumeric():
        q = int(message.text)
        D = 1/q
        await message.answer(text=f'відповідь: {D}')
        await state.finish()
    else:
        await message.answer(text='ви ввели неправельні данні будь ласка ведіть ЦИФРОВЕ значення')

k=0


@dp.message_handler(commands='calc4')
async def add(message: types.Message, state: FSMContext):
    await message.answer(text='формула закона кулона F = k*|q1|*|q2|/r^2\n'
                              'щоб порахувати формулу введіть цифрові данні\n'
                              '1.Введіть коофіцієнт пропорційності: ')

    await  state.set_state('sent_k')
@dp.message_handler(state='sent_k')
async def masa(message: types.Message, state: FSMContext):
    global k
    if message.text.isnumeric():
        k = int(message.text)
        await message.answer(text='2.введіть величину взаємодіючих зарядів q1: ')
        await state.set_state('sent_k2')

q1 = 0
@dp.message_handler(state='sent_k2')
async def masa(message: types.Message, state: FSMContext):
    global q1
    if message.text.isnumeric():
        q1 = int(message.text)
        await message.answer(text='3.введіть q2: ')
        await state.set_state('sent_k3')
q2 = 0
@dp.message_handler(state='sent_k3')
async def masa(message: types.Message, state: FSMContext):
    global q2
    if message.text.isnumeric():
        q2 = int(message.text)
        await message.answer(text='4.введіть r: ')
        await state.set_state('sent_r')
r = 0

@dp.message_handler(state='sent_r')
async def masa(message: types.Message, state: FSMContext):
    global r
    if message.text.isnumeric():
        r = int(message.text)
        F = (k*math.fabs(q1)*math.fabs(q2))/r**2
        await message.answer(text=f'відповідь: {F}')
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
