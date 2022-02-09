import sys
import os

dir_of_executable = os.path.dirname(__file__)
path_to_project_root = os.path.abspath(os.path.join(dir_of_executable, '..'))
sys.path.insert(0, path_to_project_root)
os.chdir(path_to_project_root)

import configparser
import time

from core.service.RouterAuthService import RouterAuthService

from core.actions.ChangePassword import *
from core.actions.Reboot import *
from core.actions.EnableWhitelist import *

from core.assist.Console import clearConsole



#Check if it the main executable file
if __name__ != '__main__':
    sys.exit()



config = configparser.ConfigParser()
config.read('config/settings.ini')

router = RouterAuthService()

enableTime = 11
disableTime = 4

i = 0
while True:
    try:
        authInfo = router.auth(config['Authentication']['login'], 
                    config['Authentication']['password'])
        enableWhitelist(authInfo, True)
    except HttpRequestException as exception:
        print(exception.message)
        print(f'Status code: {str(exception.status_code)}')
        if(exception.status_code == 200):
            print(exception.response)
            
    try:       
        router.logout()
    except HttpRequestException as exception:
        print(exception.message)
        print(f'Status code: {str(exception.status_code)}')
        if(exception.status_code == 200):
            print(exception.response)
    
    clearConsole()
    print(f'Whitelist enabled for {enableTime} seconds...')
    time.sleep(enableTime)
    
    try:
        router.auth(config['Authentication']['login'], 
                    config['Authentication']['password'])
        enableWhitelist(authInfo, False)
    except HttpRequestException as exception:
        print(exception.message)
        print(f'Status code: {str(exception.status_code)}')
        if(exception.status_code == 200):
            print(exception.response)
            
    try:       
        router.logout()
    except HttpRequestException as exception:
        print(exception.message)
        print(f'Status code: {str(exception.status_code)}')
        if(exception.status_code == 200):
            print(exception.response)
            
    clearConsole()
    print(f'Whitelist disabled for {disableTime} seconds...')
    time.sleep(disableTime)