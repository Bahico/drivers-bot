from aiogram import types

from admin.menu import admin_menu
from admin.message import admin_message
from driver.activation import activation_driver
from models.return_value import ReturnValue
from models.user import UserRes
from models.userType import UserStageEnum, MessageTexts, UserType


async def simple_message(message: types.Message, user: UserRes) -> ReturnValue:
    if user.data().type == UserType.SIMPLE:
        if user.data().step == UserStageEnum.DRIVER_PASSWORD:
            await activation_driver(message, user)
        else:
            user.data().change_step(UserStageEnum.DRIVER_PASSWORD)
            await message.reply("Parolni kiriting")
    elif user.data().type == UserType.DRIVER:
        if user.data().step == UserStageEnum.PASSWORD:
            if message.text == MessageTexts.PASSWORD:
                user.data().change_type(UserType.ADMIN)
                user.data().change_step(UserStageEnum.MENU)
                await message.reply("Siz admin bo'ldingiz!!")
                return admin_menu()
            else:
                await message.reply("Parolni to'g'ri kiriting")
        else:
            if message.text == MessageTexts.ADMIN:
                user.data().change_step(UserStageEnum.PASSWORD)
                await message.reply("Parolni kiriting")
    else:
        return admin_message(message, user)
        # await admin_menu(message)

