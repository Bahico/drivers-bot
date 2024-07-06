from aiogram.types import InlineKeyboardButton

from callback import AdminCallback, AdminCallbackType
from return_value import ReturnValue
from userType import UserType

inline_btn_1 = InlineKeyboardButton(
    text="Habar olish group",
    callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.GET_MESSAGE, id="").pack()
)
inline_btn_2 = InlineKeyboardButton(
    text='Habar jonatish group',
    callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.SEND_MESSAGE, id="").pack()
)


def admin_menu(remove_message = None) -> ReturnValue:
    return ReturnValue(message="Admin menu", reply_markup=[[inline_btn_1, inline_btn_2]], remove_message=remove_message)
