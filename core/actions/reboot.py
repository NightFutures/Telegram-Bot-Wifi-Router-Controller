import requests
import configparser

from core.config.AuthInfo import *

from core.assist.http import sendRequest

config = configparser.ConfigParser()
config.read('config/url.ini')

def reboot(authInfo : AuthInfo) -> bool:
    headers = {'Referer' : config['Router']['url'],
               'TokenID' : authInfo.tokenId}
    response = sendRequest(requests.post, 
                           url=config['Router']['url'] + config['Reboot']['url'], 
                           headers=headers, 
                           cookies=authInfo.jSessionId, 
                           data=config['Reboot']['command'].
                           replace('\\r', '\r').
                           replace('\\n', '\n'))
    
    if response.status_code != 200 or response.content.decode('utf-8') != config['Reboot']['response'].replace('\\r', '\r').replace('\\n', '\n'):
        return False
        
    return True