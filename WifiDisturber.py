import configparser
import time

from core.service.RouterAuthService import RouterAuthService
from core.config.AuthInfo import *

from core.actions.ChangePassword import *
from core.actions.Reboot import *
from core.actions.EnableWhitelist import *

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config/settings.ini')
    
    authInfo = AuthInfo()
    
    router = RouterAuthService(authInfo)
    
    enableTime = 7
    disableTime = 5
    
    i = 0
    while True:
        try:
            router.auth(config['Authentication']['login'], 
                        config['Authentication']['password'])
            enableWhitelist(authInfo, True)
        except HttpRequestException as exception:
            print(exception.message)
            print('Status code: ' + str(exception.status_code))
            if(exception.status_code == 200):
                print(exception.response)
                
        try:       
            router.logout()
        except HttpRequestException as exception:
            print(exception.message)
            print('Status code: ' + str(exception.status_code))
            if(exception.status_code == 200):
                print(exception.response)
        
        print("\033[H\033[J", end="")
        print(f'Whitelist enabled for {enableTime} seconds...')
        time.sleep(enableTime)
        
        try:
            router.auth(config['Authentication']['login'], 
                        config['Authentication']['password'])
            enableWhitelist(authInfo, False)
        except HttpRequestException as exception:
            print(exception.message)
            print('Status code: ' + str(exception.status_code))
            if(exception.status_code == 200):
                print(exception.response)
                
        try:       
            router.logout()
        except HttpRequestException as exception:
            print(exception.message)
            print('Status code: ' + str(exception.status_code))
            if(exception.status_code == 200):
                print(exception.response)
                
        print("\033[H\033[J", end="")
        print(f'Whitelist disabled for {disableTime} seconds...')
        time.sleep(disableTime)