import sys

import os

import configparser


dir_of_executable = os.path.dirname(__file__)
path_to_project_root = os.path.abspath(os.path.join(dir_of_executable, '..'))
sys.path.insert(0, path_to_project_root)
os.chdir(path_to_project_root)

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
    
    try:
        router.auth(config['Authentication']['login'], 
                    config['Authentication']['password'])
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