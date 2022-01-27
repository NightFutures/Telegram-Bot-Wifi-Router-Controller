import configparser

from core.service.RouterAuthService import RouterAuthService
from core.config.AuthInfo import *

from core.actions.ChangePassword import *
from core.actions.Reboot import *

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config/settings.ini')
    
    authInfo = AuthInfo()
    
    router = RouterAuthService(authInfo)
    
    try:
        router.auth(config['Authentication']['login'], 
                    config['Authentication']['password'])
        
        router.logout()
    except HttpRequestException as exception:
        print(exception.message)
        print('Status code: ' + str(exception.status_code))
        if(exception.status_code == 200):
            print(exception.response)
            