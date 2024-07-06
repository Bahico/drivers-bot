from callback import AdminCallback, AdminCallbackType
from group import GroupRes, GroupType
from aiogram import types

from return_value import ReturnValue
from userType import UserType


def group_list(callback_type: str, edit_message=False) -> ReturnValue:
    add_button_text = "Habar yuboriluvchi guruh qo'shish"
    group_title = "Habar yuboriluvchi guruhlar"
    add_type = AdminCallbackType.SEND_GROUP_CREATE
    group_type = GroupType.SEND_MESSAGE
    delete_type = AdminCallbackType.SEND_GROUP_DELETE
    if callback_type == AdminCallbackType.GET_MESSAGE:
        add_button_text = "Habar oluvchi guruh qo'shish"
        group_title = "Habar oluvchi guruhlar"
        add_type = AdminCallbackType.GET_GROUP_CREATE
        group_type = GroupType.GET_MESSAGE
        delete_type = AdminCallbackType.GET_GROUP_DELETE

    buttons = []
    groups = GroupRes().get_groups(group_type)

    for group in groups:
        buttons.append([
            types.InlineKeyboardButton(
                text=group['name'],
                callback_data=AdminCallback(
                    role=UserType.ADMIN,
                    type=delete_type,
                    id=str(group['telegram_id'])
                ).pack()
            ),
            types.InlineKeyboardButton(
                text="o'chirish ❌",
                callback_data=AdminCallback(
                    role=UserType.ADMIN,
                    type=delete_type,
                    id=str(group['telegram_id'])
                ).pack()
            )
        ])

    buttons.append([
        types.InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=AdminCallback(
                role=UserType.ADMIN,
                type=AdminCallbackType.MENU,
                id=""
            ).pack()),
        types.InlineKeyboardButton(
            text=add_button_text,
            callback_data=AdminCallback(
                role=UserType.ADMIN,
                type=add_type,
                id=""
            ).pack())
    ])
    return ReturnValue(message=group_title, reply_markup=buttons, edit_message=edit_message, remove_message=not edit_message)
