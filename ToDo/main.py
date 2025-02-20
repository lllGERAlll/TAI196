from fastapi import FastAPI, HTTPException
from typing import List

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

#Endpoint para obtener una tarea por su id
@app.get("/tareas/{tarea_id}", tags=["Obtener tarea específica"])
def get_tarea(tarea_id: int):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

#Endpoint para crear una nueva tarea
@app.post("/tareas/", tags=["Crear tarea"])
def create_tarea(tarea: dict):
    for t in tareas:
        if t["id"] == tarea.get("id"):
            raise HTTPException(status_code=400, detail="La tarea ya existe")
    tareas.append(tarea)
    return tarea

#Endpoint para actualizar una tarea
@app.put("/tareas/{tarea_id}", tags=["Actualizar tarea"])
def update_tarea(tarea_id: int, tarea: dict):
    for t in tareas:
        if t["id"] == tarea_id:
            t.update(tarea)
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

#Endpoint para eliminar una tarea
@app.delete("/tareas/{tarea_id}", tags=["Eliminar tarea"])
def delete_tarea(tarea_id: int):
    for i, t in enumerate(tareas):
        if t["id"] == tarea_id:
            tareas.pop(i)
            return {"message": "Tarea eliminada"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")