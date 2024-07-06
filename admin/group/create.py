from admin.menu import admin_menu
from group import GroupRes
from return_value import ReturnValue
from user import UserRes
from userType import UserStageEnum


def group_create(callback_type: str, user: UserRes) -> ReturnValue:
    GroupRes.create_start(user, callback_type)
    return ReturnValue(message="Guruh nomini yuboring", remove_message=True)


def group_name(name: str, user: UserRes) -> ReturnValue:
    GroupRes.create_name(name, user)
    return ReturnValue(message='Guruh "ID" sini yuboring')


def group_id(id: str, user: UserRes) -> ReturnValue:
    group = GroupRes().create_id(id, user)
    if group:
        user.stage().change_step(UserStageEnum.MENU)
        return ReturnValue(message="Guruh muvofaqiyatli yaratildi", callback_func=admin_menu)
    return ReturnValue(message="Iltimos faqat raqam kiriting")