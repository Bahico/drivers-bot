from models.return_value import ReturnValue
from models.user import UserModel


def activation_key_generate(user: UserModel) -> ReturnValue:
    activation_key = user.activation_key_generate()
    return ReturnValue(message=activation_key.json()['activation_key'])
