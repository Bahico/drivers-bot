from aiogram import Bot

from driver.accept_or_cancel_message import accept_or_cancel_message
from driver.driver_callback import DriverCallback
from driver.edit_message import edit_client_message
from models.message import MessageModel
from models.order import DriverOrder
from models.return_value import ReturnValue
from models.user import UserRes


async def take_turn(callback_data: DriverCallback, user: UserRes, bot: Bot) -> ReturnValue:
    message = MessageModel(message_id=callback_data.id, client=user.data())
    if message.checkDriver(user.data()):
        order = DriverOrder(user.data(), callback_data.id, 0, True)
        message.drivers.append({"id": order.id, "user": order.user.id, "order": order.order})
        message.update()
        await edit_client_message(message, bot)
        if message.drivers[message.driver_order_index]['id'] == order.id:
            return accept_or_cancel_message(user=user.data(), message=message)
