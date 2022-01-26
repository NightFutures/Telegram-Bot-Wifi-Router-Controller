import requests

import re

from core.config.Url import Url
from core.config.AuthInfo import AuthInfo

from core.assist.securityJs import *
from core.assist.http import *

def getKeys():
    headers = {'Referer' : Url.router}
    response = sendRequest(requests.post, url=Url.router + Url.keys, headers=headers)
    nn = re.findall(b'nn="(.*)"', response.content)[0].decode('utf-8')
    ee = re.findall(b'ee="(\d*)"', response.content)[0].decode('utf-8')
    
    return nn, ee

def getToken(authInfo : AuthInfo):
    headers = {'Referer' : Url.router}
    response = sendRequest(requests.get, url=Url.router, headers=headers, cookies=authInfo.jSessionId)
    
    return re.findall(b'<script type="text\/javascript">var token="(.*)";<\/script>', response.content)[0].decode('utf-8')
    
class RouterService:
    def __init__(self, authInfo : AuthInfo):
        self.authInfo = authInfo
    
    def auth(self, login, password):
        encoder, encrypter = getEncoder(), getEncrypter()
        nn, ee = getKeys()
        
        login = encrypter.call('RsaEncrypt', login, nn, ee)
        password = encoder.call('Base64Encoding', password)
        password = encrypter.call('RsaEncrypt', password, nn, ee)
        
        headers = {'Referer' : Url.router}
        response = sendRequest(requests.post, url=Url.router + Url.login.format(login, password), headers=headers)
        
        self.authInfo.setJSessionId(response.cookies)
        self.authInfo.setTokenId(getToken(self.authInfo))
        self.authInfo.setNnKey(nn)
        self.authInfo.setEeKey(ee)
    
    def logout(self):
        headers = {'TokenID' : self.authInfo.tokenId, 
                   'Referer' : Url.router}
        
        sendRequest(requests.post, url=Url.router + Url.cgi8, headers=headers, cookies=self.authInfo.jSessionId, data='[/cgi/logout#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r\n')