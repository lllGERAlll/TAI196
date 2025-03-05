from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from genToken import validateToken

class BearerJWT(HTTPBearer): #Trabaja de forma asincrona
    async def __call__(self, request:Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        
        if not isinstance(data, dict):
            raise HTTPException(status_code=401, detail='Formato de token no valido')
        
        if data.get('correo') != 'gera@gmail.com':
            raise HTTPException(status_code=401, detail='Credenciales no validas') 
    