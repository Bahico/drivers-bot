import requests

from models.constans import getEndpoint
from models.order import DriverOrder
from models.user import UserModel


class MessageModel:
    __resourceUrl__ = getEndpoint('message/')
    message_id: int
    text: str
    client: UserModel
    drivers: list[DriverOrder]
    driver_order_index: int
    accept_driver: DriverOrder

    def __init__(self, message_id: int or str, client: UserModel = None, text: str = "", create=False):
        self.message_id = message_id
        self.text = text
        self.client = client
        if create:
            self.create()
        else:
            self.get()

    def rowValue(self):
        return {
            "message_id": self.message_id,
            "text": self.text,
            "client": self.client.id
        }

    def create(self):
        requests.post(self.__resourceUrl__, json=self.rowValue())

    def get(self):
        message = requests.get(f"{self.__resourceUrl__}{self.message_id}/").json()
        print(message)
        self.text = message['text']
        self.client = message['client']
        self.drivers = message['drivers']
        self.driver_order_index = message['driver_order_index']
        self.accept_driver = message['accept_driver']

    def update(self):
        self.drivers = requests.put(f"{self.__resourceUrl__}{self.message_id}/", json={
            "drivers": [x['id'] for x in self.drivers]
        }).json()['drivers']

    def checkDriver(self, user: UserModel):
        for i in self.drivers:
            if i['user']['id'] == user.id:
                return False
        return True
