BOT_KEY = "7386046746:AAG5pKVitiW5snb9pX6adDhGjconHq_oBLE"
SERVER_URL = "http://176.221.29.221:8000/"


def getEndpoint(url: str) -> str:
    return SERVER_URL + url


def add_one_hour(hour: float) -> float:
    return hour + 14388
