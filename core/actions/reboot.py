import requests

from core.config.AuthInfo import *
from core.config.Url import *

from core.assist.http import sendRequest

def reboot(authInfo : AuthInfo) -> int:
    headers = {'Referer' : Url.router,
               'TokenID' : authInfo.tokenId}
    response = sendRequest(requests.post, 
                           url=Url.router + Url.cgi7, 
                           headers=headers, 
                           cookies=authInfo.jSessionId, 
                           data='[ACT_REBOOT#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r\n')
    
    return response.status_code