import jwt  #Librería para generar tokens
from jwt import ExpiredSignatureError, InvalidTokenError 
from fastapi import HTTPException 

def createToken(datos:dict): #Función para crear el token
    token:str = jwt.encode(payload=datos, key='clave', algorithm='HS256') #Genera el token
    return token #Regresa el token generado

def validateToken(token:str):
    try:
        data:dict = jwt.decode(token, key='clave', algorithms=['HS256']) #Devuelve true si el token es valido
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail='El token expiró')
    except InvalidTokenError:
        raise HTTPException(status_code=404, detail='Token no autorizado')