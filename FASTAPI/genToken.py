import jwt  #Libreria para generar el token

def createToken(datos:dict): #Función para crear el token
    token:str = jwt.encode(payload=datos, key='clave', algorithm='HS256') #Genera el token
    return token #Regresa el token generado

