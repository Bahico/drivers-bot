from typing import Callable

from aiogram import types


class ReturnValue:
    def __init__(
            self,
            message: str,
            reply_markup: types.List[types.List[types.InlineKeyboardButton]] = None,
            edit_message: bool = False,
            remove_message: bool = False,
            callback_func=None,
    ):
        self.message = message
        self.reply_markup = reply_markup
        self.editMessage = edit_message
        self.remove_message = remove_message
        self.callback_func = callback_func
