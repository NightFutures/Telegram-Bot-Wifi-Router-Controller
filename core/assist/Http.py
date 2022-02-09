from requests import Response
from typing import Callable

def sendRequest(func : Callable[..., Response], **kwargs) -> Response:
    response = func(**kwargs)
    for _ in range(4):
        if(response.status_code == 200):
            break
        response = func(**kwargs)
    return response