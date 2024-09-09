from aiogram import Bot

from driver.accept_or_cancel_message import accept_or_cancel_message
from driver.driver_callback import DriverCallback
from driver.edit_message import edit_client_message
from models.message import MessageModel
from models.order import DriverOrder
from models.return_value import ReturnValue
from models.user import UserRes


async def cancel(callback_data: DriverCallback, bot: Bot) -> ReturnValue:
    DriverOrder.cancel_order(callback_data.id)
    message = MessageModel(callback_data.id)

    await edit_client_message(message, bot)

    if len(message.drivers) >= message.driver_order_index + 1:
        driver = UserRes(message.drivers[message.driver_order_index]['user']['telegram_id'])

        return ReturnValue(edit_message=True, callback_func=accept_or_cancel_message(user=driver.data(), message=message), message="Rahmat!")
