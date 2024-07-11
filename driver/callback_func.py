from aiogram import types

from driver.accept import accept
from driver.cancel import cancel
from driver.driver_callback import DriverCallbackType, DriverCallback
from driver.take_turn import take_turn
from models.return_value import ReturnValue
from models.user import UserRes


async def driver_callback(query: types.CallbackQuery, callback_data: DriverCallback, user: UserRes, bot) -> ReturnValue:
    if callback_data.type == DriverCallbackType.TAKE_TURNS:
        return await take_turn(callback_data, user, bot=bot)
    elif callback_data.type == DriverCallbackType.CANCEL:
        return await cancel(callback_data, bot=bot)
    elif callback_data.type == DriverCallbackType.ACCEPT:
        return await accept(callback_data, bot)
