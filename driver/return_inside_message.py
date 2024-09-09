def return_inside_message(telegram_id: int, text: str, last_name: str):
    return f"Xabar: {text}\n\n<a href=\"tg://user?id={telegram_id.__str__()}\">Profile: {last_name}</a>"
