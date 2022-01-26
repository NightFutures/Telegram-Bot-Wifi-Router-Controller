import configparser

from core.service.RouterAuthService import RouterService
from core.config.AuthInfo import *

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config/settings.ini')
    
    authInfo = AuthInfo()
    
    router = RouterService(authInfo)
    router.auth(config['Authentication']['login'], 
                config['Authentication']['password'])
    router.logout()