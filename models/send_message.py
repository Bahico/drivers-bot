import requests

from models.constans import getEndpoint


class SendMessage:
    client_message_id: int
    message_id: int
    chat_id: int

    def __init__(self, client_message_id: int, message_id: int = None, chat_id: int = None, create: bool = None):
        self.client_message_id = client_message_id
        self.message_id = message_id
        self.chat_id = chat_id
        if create:
            self.create()

    def rowValue(self):
        return {
            "client_message_id": self.client_message_id,
            "message_id": self.message_id,
            "chat_id": self.chat_id
        }

    def create(self):
        requests.post(getEndpoint("send-message/"), json=self.rowValue())

    @staticmethod
    def ids(client_message_id: int):
        return requests.get(f"{getEndpoint("send-message/")}{client_message_id}").json()
