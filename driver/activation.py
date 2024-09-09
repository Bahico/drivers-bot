from aiogram.types import Message

from models.user import UserRes
from models.userType import UserStageEnum


async def activation_driver(message: Message, user: UserRes):
    activation = user.data().activation({
        "activation_key": message.text,
        "telegram_id": user.data().telegram_id
    }).json()

    if activation['success']:
        user.stage().step = UserStageEnum.START
        user.stage().update()
        await message.reply("Siz haydovchilar ro'yxatiga qo'shildingiz")
    else:
        await message.reply("Iltimos to'g'ri parol kiriting")
