BOT_KEY = "7386046746:AAF-GDBIu-qUGf_KvT3Rfd6n6CvhF6V8On0"
SERVER_URL = "http://45.61.140.211:8000/"


def getEndpoint(url: str) -> str:
    return SERVER_URL + url


def add_one_hour(hour: float) -> float:
    return hour + 14388
