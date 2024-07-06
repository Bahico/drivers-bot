class UserType:
    ADMIN: int = 1
    DRIVER: int = 2
    SIMPLE: int = 3


class MessageTexts:
    ADMIN = "admin"
    PASSWORD = "1208"
    MENU = "menu"


class UserStageEnum:
    START = "start"
    PASSWORD = "password"
    MENU = "menu"
    GET_GROUP_CREATE_NAME = "get_group_create_name"
    GET_GROUP_CREATE_ID = "get_group_create_id"
    SEND_GROUP_CREATE_NAME = "send_group_create_name"
    SEND_GROUP_CREATE_ID = "send_group_create_id"