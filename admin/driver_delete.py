from admin.admin_callback import DriverDeleteCallback
from admin.drivers_list import drivers_list
from models.return_value import ReturnValue
from models.user import UserModel


def driver_delete(callback_data: DriverDeleteCallback, user: UserModel):
    deleted_user = user.delete(callback_data.id)

    callback_data.id = user.__resourceUrl__ + "?user_type=2&page=" + str(callback_data.page)

    return ReturnValue(
        message=f"O'chirilgan haydovchi: {deleted_user['last_name']} {'@' + deleted_user['username'] if deleted_user['username'] else ''}",
        remove_message=True,
        callback_func=drivers_list(user=user, callback_data=callback_data, edit_message=False, page=0))
