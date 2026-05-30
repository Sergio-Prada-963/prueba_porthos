from itertools import count

from models import Tarea, TareaCrear, EstadoTarea
from security import hashear

# Almacenamiento en memoria
_tareas: dict[int, Tarea] = {}
_secuencia = count(1)

# Usuario de demostración
USUARIOS = {
    "admin": hashear("admin123"),
}

def crear_tarea(datos: TareaCrear) -> Tarea:
    tarea = Tarea(id=next(_secuencia), **datos.model_dump())
    _tareas[tarea.id] = tarea
    return tarea

def listar_tareas() -> list[Tarea]:
    return list(_tareas.values())


def obtener_tarea(tarea_id: int) -> Tarea | None:
    return _tareas.get(tarea_id)

def actualizar_estado(tarea_id: int, estado: EstadoTarea) -> Tarea | None:
    tarea = _tareas.get(tarea_id)
    if tarea is None:
        return None
    tarea.estado = estado
    return tarea

def eliminar_tarea(tarea_id: int) -> bool:
    return _tareas.pop(tarea_id, None) is not None
