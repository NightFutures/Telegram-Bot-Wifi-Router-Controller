from py_mini_racer import MiniRacer, py_mini_racer

#Loads Encode.js to python
def getEncoder() -> MiniRacer:
    file = open('external/Encode.js')     
    encoder = py_mini_racer.MiniRacer()
    encoder.eval(file.read())
    file.close()
    
    return encoder
    
#Loads Encrypt.js to python    
def getEncrypter() -> MiniRacer:
    file = open('external/Encrypt.js')
    encrypter = py_mini_racer.MiniRacer()
    encrypter.eval(file.read())
    file.close()
    
    return encrypter