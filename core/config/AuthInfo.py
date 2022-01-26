from requests.cookies import RequestsCookieJar

class AuthInfo:
    def setTokenId(self, tokenId : str):
        self.tokenId = tokenId
        
    def setJSessionId(self, jSessionId : RequestsCookieJar):
        self.jSessionId = jSessionId
        
    def setNnKey(self, nnKey : str):
        self.nnKey = nnKey
        
    def setEeKey(self, eeKey : str):
        self.eeKey = eeKey