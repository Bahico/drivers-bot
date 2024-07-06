from aiogram.filters.callback_data import CallbackData


class AdminCallback(CallbackData, prefix="my"):
    role: int
    type: str
    id: str


class AdminCallbackType:
    GET_MESSAGE = "get-message"
    SEND_MESSAGE = "send-message"
    GROUP_DETAIL = "group-detail"
    GET_GROUP_DELETE = "get-group-delete"
    SEND_GROUP_DELETE = "send-group-delete"
    GET_GROUP_CREATE = "get-group-create"
    SEND_GROUP_CREATE = "send-group-create"
    MENU = "menu"
