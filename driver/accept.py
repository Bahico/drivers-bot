from aiogram import Bot

from driver.driver_callback import DriverCallback
from driver.edit_message import edit_client_message
from driver.return_inside_message import return_inside_message
from models.message import MessageModel
from models.order import DriverOrder
from models.return_value import ReturnValue


async def accept(callback_data: DriverCallback, bot: Bot):
    DriverOrder.accept_order(callback_data.id)
    message = MessageModel(callback_data.id)

    await edit_client_message(message, bot)
    return ReturnValue(
        edit_message=True,
        message=f"{return_inside_message(message.client['telegram_id'], text=message.text, last_name=message.client['last_name'])}\nRahmat!"
    )
