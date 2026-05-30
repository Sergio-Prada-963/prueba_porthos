from enum import Enum
from pydantic import BaseModel, Field


class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completado = "completado"

class Credenciales(BaseModel):
    usuario: str = Field(..., min_length=1, description="Nombre de usuario")
    contrasena: str = Field(..., min_length=1, description="Contraseña en texto plano")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TareaCrear(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=120)
    descripcion: str = Field("", max_length=2000)
    estado: EstadoTarea = EstadoTarea.pendiente

class TareaActualizar(BaseModel):
    # Solo se permite cambiar el estado, según el enunciado (PATCH actualiza estado).
    estado: EstadoTarea

class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: EstadoTarea
