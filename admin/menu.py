from aiogram.types import InlineKeyboardButton

from admin.admin_callback import AdminCallback, AdminCallbackType
from models.return_value import ReturnValue
from models.userType import UserType

inline_btn_1 = InlineKeyboardButton(
    text="Habar olish group",
    callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.GET_MESSAGE, id="").pack()
)
inline_btn_2 = InlineKeyboardButton(
    text='Habar jonatish group',
    callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.SEND_MESSAGE, id="").pack()
)
users_list = InlineKeyboardButton(
    text="Haydovchilar ro'yxati",
    callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.DRIVERS_LIST, id="").pack()
)
activation_key = InlineKeyboardButton(
    text="Activation key",
    callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.ACTIVATION_KEY, id="").pack()
)


def admin_menu(remove_message=None) -> ReturnValue:
    return ReturnValue(message="Admin menu", reply_markup=[[inline_btn_1, inline_btn_2], [users_list, activation_key]], remove_message=remove_message)
