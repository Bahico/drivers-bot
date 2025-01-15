import json
import os
from datetime import datetime
from aiogram import Bot
import requests
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from admin.admin_callback import AdminCallbackType
from models.constans import getEndpoint, add_one_hour
from driver.driver_callback import DriverCallback, DriverCallbackType
from models.message import MessageModel
from models.send_message import SendMessage
from models.userType import UserStageEnum, UserType
from models.user import UserRes
from utils import mask_uzbek_phone_numbers


class GroupType:
    GET_MESSAGE = 1
    SEND_MESSAGE = 2


class Group:
    id: int or None
    name: str
    telegram_id: str
    type: int

    def __init__(self, name: str, telegram_id: str or str, type: int, id: int = None):
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
        if group_type is None:
            return requests.get(f"{self.resourceUrl}list/").json()
        return requests.get(f"{self.resourceUrl}filter/{str(group_type)}/").json()

    def delete(self, id):
        self.delete_json_file()
        return requests.delete(f'{self.resourceUrl}{id}/')

    @staticmethod
    def create_start(user: UserRes, callback_type: str):
        if callback_type == AdminCallbackType.GET_GROUP_CREATE:
            user.data().change_step(UserStageEnum.GET_GROUP_CREATE_NAME)
        else:
            user.data().change_step(UserStageEnum.SEND_GROUP_CREATE_NAME)

    @staticmethod
    def create_name(name: str, user: UserRes):
        user.data().step_under = name
        if user.data().step == UserStageEnum.GET_GROUP_CREATE_NAME:
            user.data().change_step(UserStageEnum.GET_GROUP_CREATE_ID)
        else:
            user.data().change_step(UserStageEnum.SEND_GROUP_CREATE_ID)

    def create_id(self, id: str, user: UserRes) -> Group or bool:
        try:
            group_type = GroupType.SEND_MESSAGE
            if user.data().step == UserStageEnum.GET_GROUP_CREATE_ID:
                group_type = GroupType.GET_MESSAGE
            return self.create(Group(telegram_id=id, name=user.data().step_under, type=group_type))
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

    def search(self, chat_id: str):
        groups = self.group_list()
        for group in groups:
            if group['telegram_id'] == chat_id:
                return group

    async def send_message(self, message, bot: Bot):
        MessageModel(message['message_id'], text=message['text'], client=message['user'].data(), create=True)

        await bot.delete_message(message_id=message['message_id'], chat_id=message['chat_id'])
        await bot.send_message(chat_id=str(message['chat_id']), text=f"""
            ✅ Xurmatli #{message['last_name']} sizning zakasingiz\n🚖 Haydovchilar guruhiga tushdi.\n💬 Lichkangizga ishonchli 🚕 shoferlarimiz aloqaga chiqadi.\n📞 Murojaat uchun tel: +998 93 979 09 91\n💬 Admin: @Sanjarbek772
        """)

        queue = InlineKeyboardButton(
            text="O'chirid olish",
            callback_data=DriverCallback(
                role=UserType.DRIVER,
                type=DriverCallbackType.TAKE_TURNS,
                id=message['message_id'].__str__()
            ).pack()
        )
        start_keyboard = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[queue]])
        for group in self.group_list():
            if group['type'] == GroupType.SEND_MESSAGE:
                voice = None
                if message['file_id']:
                    voice = await bot.send_voice(chat_id=group['telegram_id'], voice=message['file_id'])
                    send_message = await bot.send_message(
                        reply_to_message_id=voice.message_id,
                        text=f"Xabar: Ovozli habar",
                        parse_mode=ParseMode.HTML,
                        chat_id=group['telegram_id'],
                        reply_markup=start_keyboard
                    )
                else:
                    send_message = await bot.send_message(
                        text=f"Xabar: {mask_uzbek_phone_numbers(message['text'])}",
                        parse_mode=ParseMode.HTML,
                        chat_id=group['telegram_id'],
                        reply_markup=start_keyboard
                    )

                SendMessage(chat_id=group['telegram_id'], client_message_id=message['message_id'].__str__(), message_id=send_message.message_id, voice=True if voice else False, create=True)
