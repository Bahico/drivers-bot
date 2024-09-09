from aiogram import types

from admin.activation_key_generate import activation_key_generate
from admin.admin_callback import AdminCallbackType, AdminCallback, DriverDeleteCallback
from admin.driver_delete import driver_delete
from admin.drivers_list import drivers_list
from admin.drivers_next import drivers_next
from admin.group.create import group_create
from admin.group.delete import delete_group
from admin.group.list import group_list
from admin.menu import admin_menu
from models.return_value import ReturnValue
from models.user import UserRes


def admin_callback(query: types.CallbackQuery, callback_data: AdminCallback, user: UserRes) -> ReturnValue:
    if callback_data.type == AdminCallbackType.GET_MESSAGE or callback_data.type == AdminCallbackType.SEND_MESSAGE:
        return group_list(callback_data.type)
    elif callback_data.type == AdminCallbackType.GET_GROUP_CREATE or callback_data.type == AdminCallbackType.SEND_GROUP_CREATE:
        return group_create(callback_type=callback_data.type, user=user)
    elif callback_data.type == AdminCallbackType.SEND_GROUP_DELETE or callback_data.type == AdminCallbackType.GET_GROUP_DELETE:
        return delete_group(callback_data.id, callback_data.type)
    elif callback_data.type == AdminCallbackType.MENU:
        return admin_menu(True)
    elif callback_data.type == AdminCallbackType.DRIVERS_LIST:
        return drivers_list(callback_data=callback_data, user=user.data())
    elif callback_data.type == AdminCallbackType.DRIVER_NEXT:
        return drivers_next(callback_data=callback_data, user=user.data())
    elif callback_data.type == AdminCallbackType.ACTIVATION_KEY:
        return activation_key_generate(user=user.data())
