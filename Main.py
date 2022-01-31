import configparser
import time

from numpy import size

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
    
    timeDelays = [18, 13, 17, 17, 23, 18, 16, 9, 11, 11, 15, 7, 6, 13, 14]
    timeDelaysSize = size(timeDelays)
    
    i = 0
    while True:
        try:
            router.auth(config['Authentication']['login'], 
                        config['Authentication']['password'])
            enableWhitelist(authInfo, bool(i % 2))
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
                
        print(f'Waiting for {timeDelays[i]} seconds...')
        time.sleep(timeDelays[i])
        i = (i + 1) % timeDelaysSize