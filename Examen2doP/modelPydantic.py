from pydantic import BaseModel, Field, EmailStr

class modelEnvio(BaseModel):
    cp: str = Field(..., min_length=5, description="Codigo Postal")
    destino: str = Field(..., min_length=6, description="Destino del envio")
    peso: int = Field(..., gt=0,min_length=1, max_length=499, description="Peso del envio")