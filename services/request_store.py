PENDING_REQUESTS: dict = {}


def save_request(token: str, data: dict):
    PENDING_REQUESTS[token] = data


def get_request(token: str):
    return PENDING_REQUESTS.get(token)


def remove_request(token: str):
    PENDING_REQUESTS.pop(token, None)
