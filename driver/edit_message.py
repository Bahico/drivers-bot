from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton
from aiogram import Bot, types

from driver.driver_callback import DriverCallback, DriverCallbackType
from models.message import MessageModel
from models.send_message import SendMessage
from models.userType import UserType


async def edit_client_message(message: MessageModel, bot: Bot):
    send_message = SendMessage.ids(message.message_id)
    drivers_text = f"""XABAR: {message.text}\n\n\nHaydovchi navbat🗓\n"""

    index = 0
    for driver in message.drivers:

        driver_type = ''
        print(message.accept_driver, driver['user'], "test")
        if message.accept_driver and message.accept_driver['user']['telegram_id'] == driver['user']['telegram_id']:
            driver_type = "✅"
        elif index == message.driver_order_index:
            driver_type = "♻️"

        index += 1
        drivers_text += f"""{index.__str__()}. <a href="tg://user?id={driver['user']['telegram_id']}">{driver['user']['last_name']}</a> {driver_type}\n"""

    queue = InlineKeyboardButton(
        text="O'chirid olish",
        callback_data=DriverCallback(
            role=UserType.DRIVER,
            type=DriverCallbackType.TAKE_TURNS,
            id=message.message_id.__str__()
        ).pack()
    )
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[queue]])
    if not message.accept_driver:
        for i in send_message:
            await bot.edit_message_text(
                chat_id=i['chat_id'], message_id=i['message_id'], text=drivers_text,
                reply_markup=markup,
                parse_mode=ParseMode.HTML
            )
    else:
        for i in send_message:
            await bot.edit_message_text(
                chat_id=i['chat_id'], message_id=i['message_id'], text=drivers_text,
                parse_mode=ParseMode.HTML
            )