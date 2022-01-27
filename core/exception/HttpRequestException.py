class HttpRequestException(Exception):
    def __init__(self, message : str, status_code : int, response : bytes):            
        self.message = message
        self.status_code = status_code
        self.response = response.decode('utf-8')