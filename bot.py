from aiogram import types, Bot, Dispatcher, F
from aiogram.filters import Command, Text
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message, ReplyKeyboardRemove, InlineKeyboardButton
import asyncio

from config import TOKEN_API
from data import cityList

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot=bot, storage=storage)

class UserStatesGroup(StatesGroup):
    userId = State()
    name = State()
    age = State()
    city = State()
    hardSkills = State()
    aboutMe = State()


def getKbStart() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = '/create'))
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command('start'))
async def cmdStart(message: Message) -> None:
    await message.answer('Привет, для начала заполни анкету - командой /create', reply_markup=getKbStart())


@dp.message(Command('create'))
async def cmdCreate(message: Message, state: FSMContext) -> None:
    await state.update_data(userId=message.from_user.id)
    await message.answer('Давай начнем запаолнять анкету!\nДля начала отправь свое имя', reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserStatesGroup.name)

@dp.message(UserStatesGroup.name, F.text)
async def loadName(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.reply("Сколько тебе лет?")
    await state.set_state(UserStatesGroup.age)

@dp.message(UserStatesGroup.age, F.text)
async def loadAge(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await message.reply("Из какого вы города?")
    await state.set_state(UserStatesGroup.city)

def getKbHardSkillsFirst() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text = 'Разработка web-приложений'),
           KeyboardButton(text = 'Разработка desktop-приложений'),
           KeyboardButton(text = 'Разработка мобильных приложений'),
           KeyboardButton(text = 'Разработка игр'),
           KeyboardButton(text = 'Программирование встраиваемых систем'),
           KeyboardButton(text = 'Далее к заполнению анкеты')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

@dp.message(UserStatesGroup.city, F.text)
async def loadCity(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await message.reply("Выберите свое направление(можно несколько)!", reply_markup=getKbHardSkillsFirst())
    await state.set_state(UserStatesGroup.hardSkills)

def getKbHardSkillsWeb() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Java Script', callback_data='lang_web_JavaScript'),
           InlineKeyboardButton(text='CSS/HTML', callback_data='lang_web_CSS/HTML'),
           InlineKeyboardButton(text='C#', callback_data='lang_web_C#'),
           InlineKeyboardButton(text='C++', callback_data='lang_web_C++'),
           InlineKeyboardButton(text='Scala', callback_data='lang_web_Scala'),
           InlineKeyboardButton(text='PHP', callback_data='lang_web_PHP'),
           InlineKeyboardButton(text='Scala', callback_data='lang_web_Scala'),
           InlineKeyboardButton(text='Rust', callback_data='lang_web_Rust'),
           InlineKeyboardButton(text='Node JS', callback_data='lang_web_Node JS'),
           InlineKeyboardButton(text='Erlang', callback_data='lang_web_Erlang'),
           InlineKeyboardButton(text='Java', callback_data='lang_web_Java'),
           InlineKeyboardButton(text='Python', callback_data='lang_web_Python'),
           InlineKeyboardButton(text='Golang', callback_data='lang_web_Golang'),
           InlineKeyboardButton(text='Назад', callback_data = 'lang_web_back'))
    builder.adjust(3)
    return builder.as_markup()
def getKbHardSkillsMobile() -> types.InlineKeyboardMarkup: 
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='C#', callback_data='lang_mobile_C#'),
           InlineKeyboardButton(text='C++', callback_data='lang_mobile_C++'),
           InlineKeyboardButton(text='Swift', callback_data='lang_mobile_Swift'),
           InlineKeyboardButton(text='Objective-C', callback_data='lang_mobile_Objective-C'),
           InlineKeyboardButton(text='Java', callback_data='lang_mobile_Java'),
           InlineKeyboardButton(text='Назад', callback_data = 'lang_mobile_back'))
    builder.adjust(3)
    return builder.as_markup()
def getKbHardSkillsDesktop() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='C#', callback_data='lang_desktop_C#'),
           InlineKeyboardButton(text='C++', callback_data='lang_desktop_C++'),
           InlineKeyboardButton(text='Swift', callback_data='lang_desktop_Swift'),
           InlineKeyboardButton(text='Objective-C', callback_data='lang_desktop_Objective-C'),
           InlineKeyboardButton(text='Java', callback_data='lang_desktop_Java'),
           InlineKeyboardButton(text='Python', callback_data='lang_desktop_Python'),
           InlineKeyboardButton(text='Назад', callback_data = 'lang_desktop_back'))
    builder.adjust(3)
    return builder.as_markup()
def getKbHardSkillsGame() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='C#', callback_data='lang_game_C#'),
           InlineKeyboardButton(text='C++', callback_data='lang_game_C++'),
           InlineKeyboardButton(text='Swift', callback_data='lang_game_Swift'),
           InlineKeyboardButton(text='Назад', callback_data = 'lang_game_back'))
    builder.adjust(3)
    return builder.as_markup()
def getKbHardSkillsIron() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='C++', callback_data='lang_iron_C++'),
           InlineKeyboardButton(text='Java Script', callback_data='lang_iron_Java Script'),
           InlineKeyboardButton(text='Java', callback_data='lang_iron_Java'),
           InlineKeyboardButton(text='Python', callback_data='lang_iron_Python'),
           InlineKeyboardButton(text='Назад', callback_data = 'lang_iron_back'))
    builder.adjust(3)
    return builder.as_markup()

hardSkillsData = {}
@dp.message(UserStatesGroup.hardSkills, F.text == 'Разработка web-приложений')
async def loadHardSkillsWeb(message: Message, state: FSMContext) -> None:
    hardSkillsData[message.from_user.id] = hardSkillsData.get(message.from_user.id, {})
    await message.answer("Выберите языки которые знаете!", reply_markup=getKbHardSkillsWeb())
@dp.message(UserStatesGroup.hardSkills, F.text == 'Разработка desktop-приложений')
async def loadHardSkillsDesktop(message: Message, state: FSMContext) -> None:
    hardSkillsData[message.from_user.id] = hardSkillsData.get(message.from_user.id, {})
    await message.answer("Выберите языки которые знаете!", reply_markup=getKbHardSkillsDesktop())
@dp.message(UserStatesGroup.hardSkills, F.text == 'Разработка мобильных приложений')
async def loadHardSkillsMobile(message: Message, state: FSMContext) -> None:
    hardSkillsData[message.from_user.id] = hardSkillsData.get(message.from_user.id, {})
    await message.answer("Выберите языки которые знаете!", reply_markup=getKbHardSkillsMobile())
@dp.message(UserStatesGroup.hardSkills, F.text == 'Разработка игр')
async def loadHardSkillsGame(message: Message, state: FSMContext) -> None:
    hardSkillsData[message.from_user.id] = hardSkillsData.get(message.from_user.id, {})
    await message.answer("Выберите языки которые знаете!", reply_markup=getKbHardSkillsGame())
@dp.message(UserStatesGroup.hardSkills, F.text == 'Программирование встраиваемых систем')
async def loadHardSkillsIron(message: Message, state: FSMContext) -> None:
    hardSkillsData[message.from_user.id] = hardSkillsData.get(message.from_user.id, {})
    await message.answer("Выберите языки которые знаете!", reply_markup=getKbHardSkillsIron())
@dp.message(UserStatesGroup.hardSkills, F.text == 'Далее к заполнению анкеты')
async def loadHardSkillsNext(message: Message, state: FSMContext) -> None:
    if len(hardSkillsData) == 0:
        await message.answer("Вы ничего не выбрали!")
    else:
        await state.update_data(hardSkills=hardSkillsData[message.from_user.id])
        await message.reply("Напишете о себе!(до 4000 символов)")
        await state.set_state(UserStatesGroup.aboutMe)

@dp.callback_query(Text(startswith="lang_"))
async def callbacks_lang(callback: types.CallbackQuery):
    facul,action = callback.data.split("_")[1:3]
    hardSkillsData[callback.from_user.id][facul] = hardSkillsData[callback.from_user.id].get(facul, set())

    if action != "back":
        hardSkillsData[callback.from_user.id][facul].add(action)
    elif action == "back":
        await callback.message.edit_text(f"Вы выбрали{hardSkillsData[callback.from_user.id]}")

    await callback.answer(f'Вы выбрали {action}')

@dp.message(UserStatesGroup.aboutMe, F.text)
async def loadName(message: Message, state: FSMContext) -> None:
    await state.update_data(aboutMe=message.text)
    user_data = await state.get_data()
    await state.clear()
    await message.answer('Ваша анкета сохранена!')
    print(user_data)




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())