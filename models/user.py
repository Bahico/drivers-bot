import requests

from models.constans import getEndpoint
from models.userType import UserType


class UserModel:
    __resourceUrl__ = getEndpoint('user/')

    id: int
    telegram_id: int
    type = UserType.SIMPLE
    username: str
    last_name: str
    new = False

    step: str
    step_under: str

    def __init__(self, telegram_id: int, last_name: str = None, username: str = None, user_type: str = None,
                 chat_id: int = None):
        self.telegram_id = telegram_id
        self.username = username
        self.type = user_type
        self.last_name = last_name
        self.chat_id = chat_id
        self.get()

    def user_data(self):
        return {
            "telegram_id": self.telegram_id,
            "username": self.username,
            "type": self.type,
            "last_name": self.last_name,
            "chat_id": self.chat_id
        }

    def get(self):
        user = requests.post(f"{self.__resourceUrl__}detail/{self.telegram_id.__str__()}/", json=self.user_data())
        self.change_values(user.json())
        self.check_new(user)

    def check_new(self, request: requests.post):
        if request.status_code == 201:
            self.new = True

    def is_new(self) -> bool:
        return self.new

    def change_values(self, user: all):
        self.username = user['username']
        self.type = user['type']
        self.id = user['id']
        self.chat_id = user['chat_id']
        self.step = user['step']
        self.step_under = user['step_under']

    def change_type(self, type: UserType):
        self.type = type
        self.update()

    def change_step(self, step: str = None):
        if step is not None:
            self.step = step
        requests.patch(f"{self.__resourceUrl__}detail/{self.telegram_id.__str__()}/", json={
            "step": self.step,
            "step_under": self.step_under,
        })

    def activation(self, data):
        return requests.post(f"{self.__resourceUrl__}activation/", json=data)

    def activation_key_generate(self):
        return requests.get(f"{self.__resourceUrl__}activation/")

    def update(self):
        requests.put(f"{self.__resourceUrl__}detail/{self.telegram_id.__str__()}/", json=self.user_data())

    def users(self, user_type: int):
        return requests.get(f"{self.__resourceUrl__}", params={"user_type": user_type}).json()

    @staticmethod
    def next_or_previous(url: str):
        return requests.get(url).json()

    def delete(self, user_id: int):
        return requests.delete(f"{self.__resourceUrl__}delete/{str(user_id)}/").json()


class UserRes:
    __data: UserModel

    def __init__(self, telegram_id: int, last_name: str = None, username: str = None, user_type: int = None,
                 chat_id: int = None):
        self.__data = UserModel(
            telegram_id=telegram_id,
            last_name=last_name,
            username=username, user_type=user_type,
            chat_id=chat_id
        )

    def data(self):
        return self.__data
