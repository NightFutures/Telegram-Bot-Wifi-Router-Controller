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
        keys = requests.post(url=Url.router + Url.keys, headers=headers).content
        print(keys)
        
    
    def auth(self, login, password):
        n, e = self.getKeys()
        login = self.encrypter.Encrypt(login, self.n, self.e)
        password = self.encrypter.Encrypt(self.encoder.Base64Encoding(password), self.n, self.e)