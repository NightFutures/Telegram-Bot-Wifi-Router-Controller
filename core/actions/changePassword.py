import requests
import configparser

from core.config.AuthInfo import *

from core.assist.http import sendRequest

config = configparser.ConfigParser()
config.read('config/url.ini')

def changePassword(authInfo : AuthInfo, password : str) -> bool:
    settings = configparser.ConfigParser()
    settings.read('config/settings.ini')
    
    headers = {'Referer' : config['Router']['url'],
               'TokenID' : authInfo.tokenId}
    response = sendRequest(requests.post, 
                           url=config['Router']['url'] + config['Change password']['url'], 
                           headers=headers, 
                           cookies=authInfo.jSessionId, 
                           data=config['Change password']['command'].
                           replace('\\r', '\r').
                           replace('\\n', '\n').
                           format(settings['Authentication']['password'], settings['Authentication']['login'], password))
    
    if response.status_code != 200 or response.content.decode('utf-8') != config['Change password']['response'].replace('\\r', '\r').replace('\\n', '\n'):
        return False
    
    config.set('Authentication', 'password', password)
    with open('config/settings.ini', 'w') as configfile:
        config.write(configfile)
    
    return True