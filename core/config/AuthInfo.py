from requests.cookies import RequestsCookieJar

class AuthInfo:
    tokenId : str
    cookies : RequestsCookieJar
    nnKey : str
    eeKey : str