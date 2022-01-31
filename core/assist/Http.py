from collections.abc import Callable

from requests import Response

def sendRequest(func, *args, **kwargs) -> Response:
    response = func(*args, **kwargs)
    for _ in range(4):
        if(response.status_code == 200):
            break
        response = func(*args, **kwargs)
    return response