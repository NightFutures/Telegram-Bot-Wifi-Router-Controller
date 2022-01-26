import configparser

from core.RouterService import RouterService

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config/settings.ini')
    
    router = RouterService()
    router.auth(config['Authentication']['login'], config['Authentication']['password'])
    router.logout()