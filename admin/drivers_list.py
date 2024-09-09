from aiogram.types import InlineKeyboardButton

from admin.admin_callback import AdminCallback, AdminCallbackType, DriverDeleteCallback
from models.return_value import ReturnValue
from models.user import UserModel
from models.userType import UserType


def drivers_list(
        user: UserModel,
        callback_data: AdminCallback or DriverDeleteCallback,
        edit_message=True
) -> ReturnValue:
    if len(callback_data.id) > 0:
        drivers = user.next_or_previous(url=callback_data.id)
    else:
        drivers = user.users(user_type=UserType.DRIVER)

    drivers_button = []
    drivers_text = f"Haydovchilar soni: {str(drivers['count'])}\nHozirgi sahifa: {str(drivers['current_page'])}\n\n"
    index = 0
    for i in drivers['results']:
        index += 1

        drivers_text += f"{index}. {i['last_name']} {'@' + i['username'] if i['username'] else ''}\n"

        drivers_button.append(InlineKeyboardButton(
            text=index.__str__(),
            callback_data=DriverDeleteCallback(
                role=UserType.ADMIN,
                type=AdminCallbackType.DRIVER_DELETE,
                id=i['id'],
                page=drivers['current_page'] if len(drivers['results']) > 1 else drivers['current_page'] - 1
            ).pack()
        ))

    next_or_previous = []

    if drivers['links']['previous']:
        next_or_previous.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.DRIVER_NEXT,
                                        id=str(drivers['current_page'] - 1)).pack()
        ))
    next_or_previous.append(InlineKeyboardButton(
        text="Bosh menu",
        callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.MENU,
                                    id="").pack()
    ))
    if drivers['links']['next']:
        next_or_previous.append(InlineKeyboardButton(
            text="➡️",
            callback_data=AdminCallback(role=UserType.ADMIN, type=AdminCallbackType.DRIVER_NEXT,
                                        id=str(drivers['current_page'] + 1)).pack()
        ))
    if len(drivers_button) > 8:
        return ReturnValue(message=drivers_text,
                           reply_markup=[drivers_button[:5], drivers_button[5:], next_or_previous],
                           edit_message=edit_message)
    return ReturnValue(message=drivers_text, reply_markup=[drivers_button, next_or_previous], edit_message=edit_message)
