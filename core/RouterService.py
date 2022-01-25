import requests
import js2py
import re

from core.config.Url import Url


class RouterService:
    def __init__(self):
        eval_js, self.encoder = js2py.run_file('external/Encode.js')
        eval_js, self.encrypter = js2py.run_file('external/Encrypt.js')
        
    def getKeys(self):
        headers = {'Referer' : Url.router}
        response = requests.post(url=Url.router + Url.keys, headers=headers)
        self.nn = re.findall(b'nn="(.*)"', response.content)[0].decode('utf-8')
        self.ee = re.findall(b'ee="(\d*)"', response.content)[0].decode('utf-8')
        
    
    def auth(self, login, password):
        self.getKeys()
        login = self.encrypter.Encrypt(login, self.nn, self.ee)
        password = self.encrypter.Encrypt(self.encoder.Base64Encoding(password), self.nn, self.ee)
        
        headers = {'Referer' : Url.router}
        
        response = requests.post(url=Url.router + Url.login.format(login, password), headers=headers)
        
        self.cookies = response.cookies
        
        response = requests.get(url=Url.router, headers=headers, cookies=response.cookies)
        
        self.token = re.findall(b'<script type="text\/javascript">var token="(.*)";', response.content)[0].decode('utf-8')
    