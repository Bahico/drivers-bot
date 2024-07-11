from aiogram.filters.callback_data import CallbackData


class DriverCallback(CallbackData, prefix="my"):
    role: int
    type: str
    id: str


class DriverCallbackType:
    TAKE_TURNS = "take turns"
    ACCEPT = "accept"
    CANCEL = 'cancel'
