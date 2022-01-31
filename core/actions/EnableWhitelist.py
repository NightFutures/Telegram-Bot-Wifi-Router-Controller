import requests
import configparser

from core.config.AuthInfo import *

from core.assist.Http import sendRequest

from core.exception.HttpRequestException import *

config = configparser.ConfigParser()
config.read('config/url.ini')

def enableWhitelist(authInfo : AuthInfo, enable : bool) -> bool:
    headers = {'Referer' : config['Router']['url'],
               'TokenID' : authInfo.tokenId}
    
    response = sendRequest(requests.post, 
                           url=config['Router']['url'] + config['Enable whitelist']['url'], 
                           headers=headers, 
                           cookies=authInfo.cookies, 
                           data=config['Enable whitelist']['command'].format(int(enable)).
                           replace('\\r', '\r').
                           replace('\\n', '\n'))
    
    if response.status_code != 200 or response.content.decode('utf-8') != config['Enable whitelist']['response'].replace('\\r', '\r').replace('\\n', '\n'):
        raise HttpRequestException('Error while enabling whitelist', response.status_code, response.content)