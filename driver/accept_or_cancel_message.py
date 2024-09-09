from aiogram.types import InlineKeyboardButton

from driver.driver_callback import DriverCallback, DriverCallbackType
from driver.return_inside_message import return_inside_message
from models.message import MessageModel
from models.return_value import ReturnValue
from models.user import UserModel
from models.userType import UserType


def accept_or_cancel_message(user: UserModel, message: MessageModel, send_admin=True) -> ReturnValue:
    reply_markup = [[
        InlineKeyboardButton(
            text="✅",
            callback_data=DriverCallback(
                role=UserType.DRIVER,
                type=DriverCallbackType.ACCEPT,
                id=message.message_id.__str__()
            ).pack()
        ),
        InlineKeyboardButton(
            text="❌",
            callback_data=DriverCallback(
                role=UserType.DRIVER,
                type=DriverCallbackType.CANCEL,
                id=message.message_id.__str__()
            ).pack()
        )
    ]]

    if send_admin:
        reply_markup.append([
            InlineKeyboardButton(
                text="Adminga yuborish👨‍💻",
                callback_data=DriverCallback(
                    role=UserType.DRIVER,
                    type=DriverCallbackType.SEND_ADMIN,
                    id=message.message_id.__str__()
                ).pack()
            )
        ])

    return ReturnValue(
        chat_id=user.chat_id,
        message=return_inside_message(
            telegram_id=message.client['telegram_id'],
            last_name=message.client['last_name'],
            text=message.text
        ),
        edit_message=not send_admin,
        reply_markup=reply_markup
    )
