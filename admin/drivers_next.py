from admin.admin_callback import DriverDeleteCallback, AdminCallback
from admin.drivers_list import drivers_list
from models.user import UserModel


def drivers_next(user: UserModel, callback_data: AdminCallback or DriverDeleteCallback):
    callback_data.id = user.__resourceUrl__ + "?user_type=2&page=" + callback_data.id
    return drivers_list(user=user, callback_data=callback_data)
