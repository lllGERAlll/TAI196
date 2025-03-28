from pydantic import BaseModel, Field, EmailStr


class modelUsuario(BaseModel):
    name: str = Field(..., min_length=3, max_length=15, description="Nombre, solo letras y espacios")
    age: int = Field(..., gt=0, lt=150, description="Edad, solo numeros positivos")
    email: str = Field(..., pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$", description="Correo electronico", examples={"gerardo@gmail.com"})
    
class modelAuth(BaseModel): #Modelo para la autenticación
    correo:EmailStr
    passw:str  = Field(..., min_length=8, strip_whitespace=True, description="Contraseña, minimo 8 caracteres")