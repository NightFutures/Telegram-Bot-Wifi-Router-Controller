import requests

import re

from py_mini_racer import py_mini_racer

from core.config.Url import Url


def sendRequest(func, *args, **kwargs) -> requests.Response:
    response = func(*args, **kwargs)
    for _ in range(4):
        if(response.status_code == 200):
            break
        response = func(*args, **kwargs)
    return response

class RouterService:
    def __init__(self):
        headers = {'Referer' : Url.router}
        response = sendRequest(requests.post, url=Url.router + Url.keys, headers=headers)
        self.nn = re.findall(b'nn="(.*)"', response.content)[0].decode('utf-8')
        self.ee = re.findall(b'ee="(\d*)"', response.content)[0].decode('utf-8')
        
        file = open('external/Encode.js')     
        self.encoder = py_mini_racer.MiniRacer()
        self.encoder.eval(file.read())
        file.close()
        
        file = open('external/Encrypt.js')
        self.encrypter = py_mini_racer.MiniRacer()
        self.encrypter.eval(file.read())
        file.close()
    
    def auth(self, login, password):     
        login = self.encrypter.call('RsaEncrypt', login, self.nn, self.ee)
        password = self.encoder.call('Base64Encoding', password)
        password = self.encrypter.call('RsaEncrypt', password, self.nn, self.ee)
        
        headers = {'Referer' : Url.router}
        response = sendRequest(requests.post, url=Url.router + Url.login.format(login, password), headers=headers)
        self.cookies = response.cookies
        
        response = sendRequest(requests.get, url=Url.router, headers=headers, cookies=self.cookies)
        self.token = re.findall(b'<script type="text\/javascript">var token="(.*)";<\/script>', response.content)[0].decode('utf-8')
        
        headers = {'Referer' : Url.router, 'TokenID' : self.token}
    
    def logout(self):
        headers = {'TokenID' : self.token, 
                   'Referer' : Url.router}
        
        sendRequest(requests.post, url=Url.router + Url.cgi8, headers=headers, cookies=self.cookies, data='[/cgi/logout#0,0,0,0,0,0#0,0,0,0,0,0]0,0\r\n')