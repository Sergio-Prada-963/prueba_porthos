from fastapi import Depends, FastAPI, HTTPException, status
import storage
from models import Credenciales, Tarea, TareaActualizar, TareaCrear, Token
from security import crear_token, usuario_actual, verificar_contrasena

app = FastAPI(title="Mini API de Tareas", version="1.0.0")

@app.get("/")
def home():
    return {"servicio": "Mini API de Tareas", "docs": "/docs"}

@app.post("/auth/login", response_model=Token, tags=["auth"])
def login(credenciales: Credenciales):
    hash_guardado = storage.USUARIOS.get(credenciales.usuario)
    if not hash_guardado or not verificar_contrasena(credenciales.contrasena, hash_guardado):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    return Token(access_token=crear_token(credenciales.usuario))

# Todos los endpoints de tareas dependen de usuario_actual -> sin token válido devuelven 401.
@app.get("/tasks", response_model=list[Tarea], tags=["tasks"])
def listar(usuario: str = Depends(usuario_actual)):
    return storage.listar_tareas()

@app.post("/tasks", response_model=Tarea, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def crear(datos: TareaCrear, usuario: str = Depends(usuario_actual)):
    return storage.crear_tarea(datos)

@app.patch("/tasks/{tarea_id}", response_model=Tarea, tags=["tasks"])
def actualizar(tarea_id: int, datos: TareaActualizar, usuario: str = Depends(usuario_actual)):
    tarea = storage.actualizar_estado(tarea_id, datos.estado)
    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return tarea


@app.delete("/tasks/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def eliminar(tarea_id: int, usuario: str = Depends(usuario_actual)):
    if not storage.eliminar_tarea(tarea_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
