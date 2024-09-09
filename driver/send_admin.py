from aiogram import Bot
from aiogram.enums import ParseMode

from driver.accept_or_cancel_message import accept_or_cancel_message
from driver.driver_callback import DriverCallback
from driver.return_inside_message import return_inside_message
from models.message import MessageModel
from models.user import UserModel
from models.userType import UserType


async def send_admin(callback_data: DriverCallback, user: UserModel, bot: Bot):
    admins = user.users(UserType.ADMIN)
    message = MessageModel(callback_data.id)

    for i in admins['results']:
        await bot.send_message(
            chat_id=i['telegram_id'],
            text=return_inside_message(
                telegram_id=message.client['telegram_id'],
                text=message.text,
                last_name=message.client['last_name']
            ) + f'\n<a href="tg://user?id={str(user.telegram_id)}">Haydovchi profili</a>',
            parse_mode=ParseMode.HTML
        )

    return accept_or_cancel_message(user, message, False)
