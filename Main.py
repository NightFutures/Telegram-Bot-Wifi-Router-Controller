import configparser

from core.service.RouterAuthService import RouterAuthService
from core.config.AuthInfo import *
from core.actions.changePassword import *

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config/settings.ini')
    
    authInfo = AuthInfo()
    
    router = RouterAuthService(authInfo)
    router.auth(config['Authentication']['login'], 
                config['Authentication']['password'])
    
    router.logout()