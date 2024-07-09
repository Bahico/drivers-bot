from admin.group.list import group_list
from callback import AdminCallbackType
from models.group import GroupRes
from models.return_value import ReturnValue


def delete_group(group_id: str, callback_type: str) -> ReturnValue:
    GroupRes().delete(group_id)
    if callback_type == AdminCallbackType.SEND_GROUP_DELETE:
        return group_list(AdminCallbackType.SEND_MESSAGE, True)
    else:
        return group_list(AdminCallbackType.GET_MESSAGE, True)