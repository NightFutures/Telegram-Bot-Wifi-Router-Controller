import requests
import re
import configparser

from core.config.AuthInfo import *
from core.assist.SecurityJs import *

from core.assist.Http import *

from core.exception.HttpRequestException import *

config = configparser.ConfigParser()
config.read('config/url.ini')
    
class RouterAuthService:
    def __init__(self, authInfo : AuthInfo):
        self.authInfo = authInfo
    
    def auth(self, login, password) -> bool:
        encoder, encrypter = getEncoder(), getEncrypter()
        nn, ee = getKeys()

        login = encrypter.call('RsaEncrypt', login, nn, ee)
        password = encoder.call('Base64Encoding', password)
        password = encrypter.call('RsaEncrypt', password, nn, ee)
        
        headers = {'Referer' : config['Router']['url']}
        response = sendRequest(requests.post, 
                               url=config['Router']['url'] + config['Login']['url'].format(login, password), 
                               headers=headers)

        if response.status_code != 200 or response.content.decode('utf-8') != config['Login']['response'].replace('\\r', '\r').replace('\\n', '\n'): 
            raise HttpRequestException('Error while loging in', response.status_code, response.content)
        
        tokenId = getToken(response.cookies)
        
        self.authInfo.tokenId = tokenId
        self.authInfo.cookies = response.cookies
        self.authInfo.nnKey = nn
        self.authInfo.eeKey = ee
    
    def logout(self) -> bool:
        headers = {'TokenID' : self.authInfo.tokenId, 
                   'Referer' : config['Router']['url']}
        
        response = sendRequest(requests.post, 
                    url=config['Router']['url'] + config['Logout']['url'],
                    headers=headers, 
                    cookies=self.authInfo.cookies, 
                    data=config['Logout']['command'].replace('\\r', '\r').replace('\\n', '\n'))
        
        if response.status_code != 200 or response.content.decode('utf-8') != config['Logout']['response'].replace('\\r', '\r').replace('\\n', '\n'):
            raise HttpRequestException('Error while loging out', response.status_code, response.content)
        
        
def getKeys() -> str:
    headers = {'Referer' : config['Router']['url']}
    response = sendRequest(requests.post, 
                           url=config['Router']['url'] + config['Keys']['url'], 
                           headers=headers)
    if response.status_code != 200:
        raise HttpRequestException('Error while getting keys', response.status_code, response.content)
    
    return re.findall(b'nn="(.*)"', response.content)[0].decode('utf-8'), re.findall(b'ee="(\d*)"', response.content)[0].decode('utf-8')

def getToken(cookies : RequestsCookieJar) -> str:
    headers = {'Referer' : config['Router']['url']}
    response = sendRequest(requests.get, 
                           url=config['Router']['url'], 
                           headers=headers, 
                           cookies=cookies)
    
    if response.status_code != 200:
        raise HttpRequestException('Error while getting token', response.status_code, response.content)
        
    return re.findall(b'<script type="text\/javascript">var token="(.*)";<\/script>', 
                          response.content)[0].decode('utf-8')