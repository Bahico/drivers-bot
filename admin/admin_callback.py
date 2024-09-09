from aiogram.filters.callback_data import CallbackData


class AdminCallback(CallbackData, prefix="my"):
    role: int
    type: str
    id: str


class DriverDeleteCallback(CallbackData, prefix="my"):
    role: int
    type: str
    id: int
    page: int


class AdminCallbackType:
    GET_MESSAGE = "get-message"
    SEND_MESSAGE = "send-message"
    DRIVER_DELETE = "driver-delete"
    DRIVER_NEXT = "driver-next"
    DRIVERS_LIST = "drivers-list"
    ACTIVATION_KEY = "activation-key"
    GROUP_DETAIL = "group-detail"
    GET_GROUP_DELETE = "get-group-delete"
    SEND_GROUP_DELETE = "send-group-delete"
    GET_GROUP_CREATE = "get-group-create"
    SEND_GROUP_CREATE = "send-group-create"
    MENU = "menu"
