import requests
import configparser

from core.config.AuthInfo import *

from core.assist.http import sendRequest

config = configparser.ConfigParser()
config.read('config/url.ini')

def reboot(authInfo : AuthInfo) -> int:
    headers = {'Referer' : config['Router']['url'],
               'TokenID' : authInfo.tokenId}
    response = sendRequest(requests.post, 
                           url=config['Router']['url'] + config['Reboot']['url'], 
                           headers=headers, 
                           cookies=authInfo.jSessionId, 
                           data=config['Reboot']['command'] + '\r\n')
    
    return response.status_code