BOT_KEY = "5179562412:AAGGQcgs2kD1rJpDZCTnzrjSiQm5zk9n0IA"
SERVER_URL = "http://45.61.140.211:8000/"


def getEndpoint(url: str) -> str:
    return SERVER_URL + url


def add_one_hour(hour: float) -> float:
    return hour + 14388
