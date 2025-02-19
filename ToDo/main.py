from fastapi import FastAPI

app = FastAPI(
    title="Gestión de Tareas",
    description="Gerardo Ligorio Zea",
    version="1.0.0"
)

tareas = [
    {
        "id": 1,
        "titulo": "Estudiar para el exámen",
        "descripcion": "Repasar los apuntes de TAI",
        "vencimiento": "14-02-2024",
        "estado": "completada"
    },
    {
        "id": 2,
        "titulo": "Hacer compras",
        "descripcion": "Comprar en el mercado",
        "vencimiento": "15-02-2024",
        "estado": "no completada"
    },
    {
        "id": 3,
        "titulo": "Ir al gimnasio",
        "descripcion": "Hacer ejercicio",
        "vencimiento": "16-02-2024",
        "estado": "no completada"
    }
]

@app.get("/", tags=["Inicio"])
def main():
    return {"Repaso FASTAPI": "Gestión de Tareas"}

#Endpoint para obtener todas las tareas
@app.get("/tareas", tags=["Tareas"])
def get_tareas():
    return tareas
