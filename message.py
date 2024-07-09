from aiogram import types

from admin.menu import admin_menu
from admin.message import admin_message
from models.return_value import ReturnValue
from models.user import UserRes
from models.userType import UserStageEnum, MessageTexts, UserType


async def simple_message(message: types.Message, user: UserRes) -> ReturnValue:
    if user.data().type == UserType.DRIVER or user.data().type == UserType.SIMPLE:
        if user.stage().step == UserStageEnum.START:
            if message.text == MessageTexts.ADMIN:
                user.stage().change_step(UserStageEnum.PASSWORD)
                await message.reply("Parolni kiriting")
        elif user.stage().step == UserStageEnum.PASSWORD:
            if message.text == MessageTexts.PASSWORD:
                user.data().change_type(UserType.ADMIN)
                user.stage().change_step(UserStageEnum.MENU)
                await message.reply("Siz admin bo'ldingiz!!")
                return admin_menu()
            else:
                await message.reply("Parolni to'g'ri kiriting")
    else:
        return admin_message(message, user)
        # await admin_menu(message)

