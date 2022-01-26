from py_mini_racer import py_mini_racer

def getEncoder():
    file = open('external/Encode.js')     
    encoder = py_mini_racer.MiniRacer()
    encoder.eval(file.read())
    file.close()
    return encoder
    
def getEncrypter():
    file = open('external/Encrypt.js')
    encrypter = py_mini_racer.MiniRacer()
    encrypter.eval(file.read())
    file.close()
    
    return encrypter