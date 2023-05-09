from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from config import TOKEN_API
from data import cityList

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

class UserStatesGroup(StatesGroup):
    name = State()
    age = State()
    city = State()
    hardSkills = State()


def getKbStart() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    return kb

@dp.message_handler(commands=['start'])
async def cmdStart(message: types.Message) -> None:
    await message.answer('Привет, для начала заполни анкету - командой /create', reply_markup=getKbStart())


@dp.message_handler(commands=['create'])
async def cmdCreate(message: types.Message) -> None:
    await message.answer('Давай начнем запаолнять анкету!\nДля начала отправь свое имя')
    await UserStatesGroup.name.set()

@dp.message_handler(content_types=['text'], state=UserStatesGroup.name)
async def loadName(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    
    await message.reply("Сколько тебе лет?")
    await UserStatesGroup.next()

@dp.message_handler(content_types=['text'], state=UserStatesGroup.age)
async def loadAge(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text
    
    await message.reply("Из какого вы города?")
    await UserStatesGroup.next()

def getKbHardSkillsFirst() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Разработка web-приложений'),
           KeyboardButton('Разработка desktop-приложений'),
           KeyboardButton('Разработка мобильных приложений'),
           KeyboardButton('Разработка игр'),
           KeyboardButton('Программирование встраиваемых систем'),
           KeyboardButton('Далее к заполнению анкеты'))
    return kb

@dp.message_handler(content_types=['text'], state=UserStatesGroup.city)
async def loadCity(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        while True:
            if message.text in cityList:
                data['city'] = message.text
                break
            else:
                await message.answer("Такого города не существует в России, попробуйте еще раз")
    
    await message.reply("Выберите свое направление(можно несколько)!", reply_markup=getKbHardSkillsFirst())
    await UserStatesGroup.next()

def getKbHardSkillsWeb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Type Script'),
           KeyboardButton('Java Script'),
           KeyboardButton('CSS/HTML'),
           KeyboardButton('C#'),
           KeyboardButton('C++'),
           KeyboardButton('Scala'),
           KeyboardButton('PHP'),
           KeyboardButton('Scala'),
           KeyboardButton('Rust'),
           KeyboardButton('Node JS'),
           KeyboardButton('Erlang'),
           KeyboardButton('Java'),
           KeyboardButton('Python'),
           KeyboardButton('Golang'),
           KeyboardButton('Назад'))
    return kb

def getKbHardSkillsMobile() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Kotlin'),
           KeyboardButton('C#'),
           KeyboardButton('C++'),
           KeyboardButton('Swift'),
           KeyboardButton('Objective-C'),
           KeyboardButton('Java'),
           KeyboardButton('Назад'))
    return kb

def getKbHardSkillsDesktop() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('C#'),
           KeyboardButton('C++'),
           KeyboardButton('Swift'),
           KeyboardButton('Objective-C'),
           KeyboardButton('Java'),
           KeyboardButton('Python'),
           KeyboardButton('Назад'))
    return kb

def getKbHardSkillsGame() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('C#'),
           KeyboardButton('C++'),
           KeyboardButton('Swift'),
           KeyboardButton('Назад'))
    return kb

def getKbHardSkillsIron() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('C++'),
           KeyboardButton('Java Script'),
           KeyboardButton('Java'),
           KeyboardButton('Python'),
           KeyboardButton('Назад'))
    return kb





@dp.message_handler(content_types=['text'], state=UserStatesGroup.hardSkills)
async def loadHardSkills(message: types.Message, state: FSMContext) -> None:
    hardskills = []
    while message.text != 'Далее к заполнению анкеты' and len(hardskills) == 0:
        if message.text ==  "Далее к заполнению анкеты" and len(hardskills) == 0:
            await message.answer("Вы еще ничего не выбрали!", reply_markup=getKbHardSkillsFirst())
        elif  message.text ==  "Разработка web-приложений":
            while message.text != "Назад":
                await message.answer("Выберите языки которые вы знаете!", reply_markup=getKbHardSkillsWeb())
                hardskills.append(message.text)
        elif  message.text ==  "Разработка desktop-приложений":
            while message.text != "Назад":
                await message.answer("Выберите языки которые вы знаете!", reply_markup=getKbHardSkillsWeb())
                hardskills.append(message.text)
        elif  message.text ==  "Разработка мобильных приложений":
            while message.text != "Назад":
                await message.answer("Выберите языки которые вы знаете!", reply_markup=getKbHardSkillsWeb())
                hardskills.append(message.text)
        elif  message.text ==  "Разработка игр":
            while message.text != "Назад":
                await message.answer("Выберите языки которые вы знаете!", reply_markup=getKbHardSkillsWeb())
                hardskills.append(message.text)
        elif  message.text ==  "Программирование встраиваемых систем":
            while message.text != "Назад":
                await message.answer("Выберите языки которые вы знаете!", reply_markup=getKbHardSkillsWeb())
                hardskills.append(message.text)
        else:
            await message.answer("Вы ввели что то не верное попробуйте снова!", reply_markup=getKbHardSkillsFirst())


    async with state.proxy() as data:
            data['hardSkills'] = hardskills
    
    await message.reply("Хорошо")
    #await UserStatesGroup.next()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)