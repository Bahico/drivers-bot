import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from admin.admin_callback import AdminCallback, DriverDeleteCallback
from admin.callback_func import admin_callback
from admin.driver_delete import driver_delete
from driver.callback_func import driver_callback
from driver.driver_callback import DriverCallback
from models.constans import BOT_KEY
from models.group import GroupRes, GroupType
from message import simple_message
from models.return_value import ReturnValue
from models.user import UserRes
from models.userType import UserType, UserStageEnum

bot = Bot(BOT_KEY)
router = Router()

dp = Dispatcher()


@dp.message(CommandStart())
async def send_id(message: types.Message) -> None:
    if message.chat.type not in ["group", "supergroup"]:
        message_id = message.from_user.id
        username = message.from_user.username
        user = UserRes(
            telegram_id=message_id,
            chat_id=message.chat.id,
            last_name=message.from_user.first_name, username=username
        )
        if user.data().is_new() or user.data().type == UserType.SIMPLE:
            user.stage().step = UserStageEnum.DRIVER_PASSWORD
            user.stage().update()
            await message.reply("Parolni kiriting")
        else:
            await message.reply("Siz haydovchilar ro'yxatida borsiz")


@dp.message()
async def message(message: types.Message) -> None:
    if message.chat.type in ["group", "supergroup"]:
        group = GroupRes()
        group_type = group.search(str(message.chat.id))
        if group_type and group_type['type'] == GroupType.GET_MESSAGE:
            user = UserRes(telegram_id=message.from_user.id, last_name=message.from_user.first_name)
            if user.data().type == UserType.SIMPLE:
                await group.send_message(message={
                    "message_id": message.message_id,
                    "chat_id": message.chat.id,
                    "user_id": message.from_user.id,
                    "last_name": message.from_user.first_name,
                    "text": message.text,
                    "user": user,
                    "file_id": message.voice.file_id if message.voice else None
                }, bot=bot)
    else:
        user = UserRes(telegram_id=message.from_user.id, last_name=message.from_user.first_name,
                       chat_id=message.chat.id)
        data = await simple_message(message, user)
        await send_message(message.from_user.id, data)


@router.callback_query(AdminCallback.filter(F.role == UserType.ADMIN))
async def my_callback_foo(query: CallbackQuery, callback_data: AdminCallback):
    user = UserRes(telegram_id=query.from_user.id, last_name=query.from_user.first_name)
    data = admin_callback(query, callback_data, user)
    await send_message(query.message.chat.id, data, message_id=query.message.message_id)


@router.callback_query(DriverDeleteCallback.filter(F.role == UserType.ADMIN))
async def my_callback_foo(query: CallbackQuery, callback_data: DriverDeleteCallback):
    user = UserRes(telegram_id=query.from_user.id, last_name=query.from_user.first_name)
    data = driver_delete(callback_data=callback_data, user=user.data())
    await send_message(query.message.chat.id, data, message_id=query.message.message_id)


@router.callback_query(DriverCallback.filter(F.role == UserType.DRIVER))
async def my_callback_foo(query: CallbackQuery, callback_data: DriverCallback):
    user = UserRes(telegram_id=query.from_user.id, last_name=query.from_user.first_name)
    if user.data().type == UserType.DRIVER or user.data().type == UserType.ADMIN:
        data = await driver_callback(query, callback_data, user, bot)
        await send_message(query.message.chat.id, data, message_id=query.message.message_id)


async def send_message(chat_id: int, data: ReturnValue, message_id: int = None):
    if data:
        if data.reply_markup:
            markup = types.InlineKeyboardMarkup(row_width=5, inline_keyboard=data.reply_markup)
            if data.editMessage:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=data.message,
                                            reply_markup=markup, parse_mode=ParseMode.HTML)
            elif data.chat_id:
                await bot.send_message(chat_id=data.chat_id, text=data.message, reply_markup=markup,
                                       parse_mode=ParseMode.HTML)
            else:
                await bot.send_message(chat_id, data.message, reply_markup=markup, parse_mode=ParseMode.HTML)

        else:
            if data.editMessage:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=data.message,
                                            parse_mode=ParseMode.HTML)
            else:
                await bot.send_message(chat_id, data.message, parse_mode=ParseMode.HTML)

        if data.remove_message:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        if data.callback_func:
            await send_message(chat_id=data.chat_id or chat_id, data=data.callback_func, message_id=message_id)


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
