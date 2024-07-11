import requests

from models.constans import getEndpoint
from models.user import UserModel


class DriverOrder:
    __resourceUrl__ = getEndpoint('order/')
    id: int
    user: UserModel
    order: int

    def __init__(self, user: UserModel, message_id: int or str, order: int = 0, create=False):
        self.user = user
        self.order = order
        self.message_id = message_id
        if create:
            self.create()

    def rowValue(self):
        return {
            "user": self.user.id,
            "order": self.order
        }

    def create(self):
        self.id = requests.post(f"{self.__resourceUrl__}{self.message_id}/", json=self.rowValue()).json()['id']

    @staticmethod
    def cancel_order(message_id: str):
        return requests.get(getEndpoint(f'cancel-order/{message_id}'))

    @staticmethod
    def accept_order(message_id: str):
        return requests.get(getEndpoint(f'accept-order/{message_id}'))
