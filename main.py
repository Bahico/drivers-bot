import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from admin.admin_callback import admin_callback
from callback import AdminCallback
from constans import BOT_KEY
from group import GroupRes, GroupType
from message import simple_message
from return_value import ReturnValue
from user import UserRes
from userType import UserType

bot = Bot(BOT_KEY)
router = Router()

dp = Dispatcher()


@dp.message(CommandStart())
async def send_id(message: types.Message) -> None:
    id = message.from_user.id
    username = message.from_user.username
    user = UserRes(telegram_id=id, username=username, type=UserType.DRIVER)
    if user.data().is_new():
        await message.reply("Siz haydovchilar ro'yxatiga muvofaqiyatli qo'shildingiz")
    else:
        await message.reply("Siz haydovchilar ro'yxatida borsiz")


@dp.message()
async def message(message: types.Message) -> None:
    print(message.chat.type)
    if message.chat.type in ["group", "supergroup"]:
        group = GroupRes()
        if group.search(message.chat.id)['type'] == GroupType.GET_MESSAGE:
            user = UserRes(telegram_id=message.from_user.id)
            if user.data().type == UserType.SIMPLE:
                await group.send_message(message_id=message.message_id,chat_id=message.chat.id, message=message.text, bot=bot)
    else:
        user = UserRes(telegram_id=message.from_user.id)
        data = await simple_message(message, user)
        await send_message(message.from_user.id, data)


@router.callback_query(AdminCallback.filter(F.role == UserType.ADMIN))
async def my_callback_foo(query: CallbackQuery, callback_data: AdminCallback):
    user = UserRes(telegram_id=query.from_user.id)
    data = admin_callback(query, callback_data, user)
    await send_message(query.message.chat.id, data, message_id=query.message.message_id)


async def send_message(chat_id: int, data: ReturnValue, message_id: int = None):
    if data.reply_markup:
        markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=data.reply_markup)
        if data.editMessage:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=data.message, reply_markup=markup)
        else:
            await bot.send_message(chat_id, data.message, reply_markup=markup)
    else:
        await bot.send_message(chat_id, data.message)

    if data.remove_message:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)

    if data.callback_func:
        await send_message(chat_id=chat_id, data=data.callback_func(), message_id=message_id)


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
