from aiogram import types

from admin.group.create import group_name, group_id
from admin.menu import admin_menu
from models.userType import UserStageEnum
from models.return_value import ReturnValue
from models.user import UserRes


def admin_message(message: types.Message, user: UserRes) -> ReturnValue:
    print(user.stage().step, user.stage().rowValue())
    if user.stage().step == UserStageEnum.GET_GROUP_CREATE_NAME or user.stage().step == UserStageEnum.SEND_GROUP_CREATE_NAME:
        return group_name(message.text, user)
    elif user.stage().step == UserStageEnum.GET_GROUP_CREATE_ID or user.stage().step == UserStageEnum.SEND_GROUP_CREATE_ID:
        return group_id(message.text, user)
    else:
        return admin_menu()
