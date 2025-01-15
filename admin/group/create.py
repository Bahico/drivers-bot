from admin.menu import admin_menu
from models.group import GroupRes
from models.return_value import ReturnValue
from models.user import UserRes
from models.userType import UserStageEnum


def group_create(callback_type: str, user: UserRes) -> ReturnValue:
    GroupRes.create_start(user, callback_type)
    return ReturnValue(message="Guruh nomini yuboring", remove_message=True)


def group_name(name: str, user: UserRes) -> ReturnValue:
    GroupRes.create_name(name, user)
    return ReturnValue(message='Guruh "ID" sini yuboring')


def group_id(id: str, user: UserRes) -> ReturnValue:
    group = GroupRes().create_id(id, user)
    if group:
        user.data().step = UserStageEnum.MENU
        user.data().change_step()
        return ReturnValue(message="Guruh muvofaqiyatli yaratildi", callback_func=admin_menu())
    return ReturnValue(message="Iltimos faqat raqam kiriting")