import requests

from constans import getEndpoint
from userType import UserType


class UserModel:
    __resourceUrl__ = getEndpoint('user/')

    telegram_id: int
    type = UserType.SIMPLE
    username: str
    last_name: str
    new = False

    def __init__(self, telegram_id: int, last_name: str, username: str = None, type: str = None):
        self.telegram_id = telegram_id
        self.username = username
        self.type = type
        self.last_name = last_name

    def user_data(self):
        return {
            "telegram_id": self.telegram_id,
            "username": self.username,
            "type": self.type,
            "last_name": self.last_name
        }

    def get(self, call):
        print(self.user_data())
        user = requests.post(f"{self.__resourceUrl__}{self.telegram_id.__str__()}/", json=self.user_data())
        self.change_values(user.json())
        self.check_new(user)
        call()

    def check_new(self, request: requests.post):
        if request.status_code == 201:
            self.new = True

    def is_new(self) -> bool:
        return self.new

    def change_values(self, user: all):
        self.username = user['username']
        self.type = user['type']

    def change_type(self, type: UserType):
        self.type = type
        self.update()

    def update(self):
        requests.put(f"{self.__resourceUrl__}{self.telegram_id.__str__()}/", json=self.user_data())


class UserStage:
    __resourceUrl__ = getEndpoint('user/stage')

    telegram_id: int
    step: str
    step_under: str

    def __init__(self, telegram_id: int):
        self.telegram_id = telegram_id

    def change_values(self):
        user = requests.get(f"{self.__resourceUrl__}/{self.telegram_id}/")
        if user.json():
            self.step = user.json()['step']
            self.step_under = user.json()['step_under']

    def change_step(self, step: str):
        self.step = step
        self.update()

    def change_step_under(self, under_step: str):
        self.step_under = under_step
        self.update()

    def update(self):
        requests.put(f"{self.__resourceUrl__}/{self.telegram_id}/", json=self.rowValue())

    def rowValue(self):
        return {
            "telegram_id": self.telegram_id,
            "step": self.step,
            "step_under": self.step_under,
        }


class UserRes:
    __data: UserModel
    __stage: UserStage

    def __init__(self, telegram_id: int, last_name: str = None, username: str = None, user_type: int = None):
        self.__data = UserModel(telegram_id, last_name, username, user_type)
        self.__stage = UserStage(telegram_id)
        self.__data.get(self.__stage.change_values)

    def stage(self):
        return self.__stage

    def data(self):
        return self.__data
