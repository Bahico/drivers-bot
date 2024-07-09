import json
import os
from datetime import datetime
from aiogram import Bot
import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback import AdminCallbackType
from constans import getEndpoint, add_one_hour
from models.userType import UserStageEnum
from models.user import UserRes


class GroupType:
    GET_MESSAGE = 1
    SEND_MESSAGE = 2


class Group:
    id: int or None
    name: str
    telegram_id: int
    type: int

    def __init__(self, name: str, telegram_id: int or str, type: int, id: int = None):
        self.id = id
        self.name = name
        self.telegram_id = telegram_id
        self.type = type

    def rowValues(self):
        return {
            "id": self.id,
            "name": self.name,
            "telegram_id": self.telegram_id,
            "type": self.type,
        }


class GroupRes:
    resourceUrl = getEndpoint('group/')
    json_name = "group.json"
    groups_list_cache = []

    def group_list(self):
        if self.groups_list_cache:
            return self.groups_list_cache
        groups = self.groups()
        self.groups_list_cache = groups
        return groups

    def groups(self, group_type: int = None) -> list[Group]:
        try:
            f = open(self.json_name)
            data = json.load(f)
            if data['time'] >= add_one_hour(datetime.now().timestamp()):
                groups = self.get_groups(group_type)
                self.write_groups_json(groups)
                return groups
            else:
                return data['groups']
        except FileNotFoundError:
            groups = self.get_groups(group_type)
            self.write_groups_json(groups)
            return groups

    def write_groups_json(self, data: list[Group]):
        with open(self.json_name, "w") as outfile:
            outfile.write(json.dumps({
                "time": datetime.now().timestamp(),
                "groups": data
            }))

    def get_groups(self, group_type: int = None) -> list[Group]:
        print(False)
        if group_type is None:
            return requests.get(f"{self.resourceUrl}list/").json()
        return requests.get(f"{self.resourceUrl}filter/{str(group_type)}/").json()

    def delete(self, id):
        self.delete_json_file()
        return requests.delete(f'{self.resourceUrl}{id}/')

    @staticmethod
    def create_start(user: UserRes, callback_type: str):
        if callback_type == AdminCallbackType.GET_GROUP_CREATE:
            user.stage().change_step(UserStageEnum.GET_GROUP_CREATE_NAME)
        else:
            user.stage().change_step(UserStageEnum.SEND_GROUP_CREATE_NAME)

    @staticmethod
    def create_name(name: str, user: UserRes):
        user.stage().change_step_under(name)
        if user.stage().step == UserStageEnum.GET_GROUP_CREATE_NAME:
            user.stage().change_step(UserStageEnum.GET_GROUP_CREATE_ID)
        else:
            user.stage().change_step(UserStageEnum.SEND_GROUP_CREATE_ID)

    def create_id(self, id: str, user: UserRes) -> Group or bool:
        try:
            group_type = GroupType.SEND_MESSAGE
            if user.stage().step == UserStageEnum.GET_GROUP_CREATE_ID:
                group_type = GroupType.GET_MESSAGE
            return self.create(Group(telegram_id=int(id), name=user.stage().step_under, type=group_type))
        except:
            return False

    def create(self, group: Group) -> Group:
        self.delete_json_file()
        return requests.post(f"{self.resourceUrl}create/", group.rowValues()).json()

    def delete_json_file(self):
        self.groups_list_cache = []
        try:
            os.remove(self.json_name)
        except:
            pass

    def search(self, chat_id: int):
        groups = self.group_list()
        for group in groups:
            if group['telegram_id'] == chat_id:
                return group

    async def send_message(self, message, bot: Bot):
        message_id, chat_id, last_name, user_id = message

        await bot.delete_message(message_id=message_id, chat_id=chat_id)
        await bot.send_message(chat_id=chat_id, text=f"""
            ✅ Xurmatli #{last_name} sizning zakasingiz
            🚖 Haydovchilar guruhiga tushdi.
            💬 Lichkangizga ishonchli 🚕 shoferlarimiz aloqaga chiqadi.
            📞 Murojaat uchun tel: 
            +998909994921
            💬 Admin: @bahico0312
        """)

        studyboi = InlineKeyboardButton(text='Open profile', url=f'tg://user?id={user_id}')
        start_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[studyboi]])
        for group in self.group_list():
            if group['type'] == GroupType.SEND_MESSAGE:
                await bot.send_message(text=message, chat_id=group['telegram_id'], reply_markup=start_keyboard)