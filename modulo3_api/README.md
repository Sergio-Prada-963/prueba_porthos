# 🗂️ Módulo 3 · Mini API de Tareas con Autenticación

## 📝 Descripción

API REST construida con **FastAPI** que gestiona tareas y protege sus operaciones con **JWT**. Para usar los endpoints de tareas hay que autenticarse primero en `/auth/login` y enviar el token en cada petición.

---

## 🎯 Características

- ✅ `POST /auth/login` — devuelve un token JWT
- ✅ `GET /tasks` — lista las tareas (requiere token)
- ✅ `POST /tasks` — crea una tarea con título, descripción y estado (`pendiente` / `en_progreso` / `completado`)
- ✅ `PATCH /tasks/{id}` — actualiza el estado de una tarea
- ✅ `DELETE /tasks/{id}` — elimina una tarea
- ✅ Endpoints de tareas protegidos con JWT: sin token válido devuelve **401**
- ✅ Almacenamiento en memoria (sin base de datos)
- ✅ Pruebas automáticas con \`pytest\`

---

## 📂 Estructura

\`\`\`
modulo3_api/
├── main.py              # App FastAPI y definición de endpoints
├── models.py            # Esquemas Pydantic (tareas, login, token)
├── security.py          # Generación y validación de JWT + hashing de contraseñas
├── storage.py           # Almacenamiento en memoria y usuario de demo
├── tests/
│   └── test_api.py      # Pruebas: login, creación de tarea y rechazo sin token
├── requirements.txt
└── .gitignore
\`\`\`

---

## 🚀 Instalación

### Requisitos

- **Python 3.10+**

### Pasos

\`\`\`bash
cd modulo3_api

# Crear entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
\`\`\`

> **Clave JWT (opcional):** por defecto se usa una clave de desarrollo. Para producción defínela con la variable de entorno \`JWT_SECRET\`.

---

## ▶️ Ejecución

\`\`\`bash
uvicorn main:app --reload
\`\`\`

El servicio queda en \`http://127.0.0.1:8000\` y la documentación interactiva (Swagger) en \`http://127.0.0.1:8000/docs\`.

**Usuario de demostración:** \`admin\` / \`admin123\`

---

## 🧪 Ejemplos de uso (curl)

### 1. Login — obtener el token

\`\`\`bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"usuario": "admin", "contrasena": "admin123"}'
\`\`\`

Respuesta:

\`\`\`json
{ "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...", "token_type": "bearer" }
\`\`\`

> Guarda el \`access_token\`; se envía en la cabecera \`Authorization: Bearer <token>\` en las siguientes peticiones.

### 2. Crear una tarea

\`\`\`bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Preparar entrega", "descripcion": "Revisar checklist", "estado": "pendiente"}'
\`\`\`

### 3. Listar tareas

\`\`\`bash
curl http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer <TOKEN>"
\`\`\`

### 4. Actualizar el estado

\`\`\`bash
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"estado": "completado"}'
\`\`\`

### 5. Eliminar una tarea

\`\`\`bash
curl -X DELETE http://127.0.0.1:8000/tasks/1 \
  -H "Authorization: Bearer <TOKEN>"
\`\`\`

### Sin token → 401

\`\`\`bash
curl -i http://127.0.0.1:8000/tasks
# HTTP/1.1 401 Unauthorized
\`\`\`

---

## ✅ Pruebas

Con el entorno virtual activado y las dependencias instaladas:

\`\`\`bash
pytest -q
\`\`\`

Cubren tres casos clave:

1. **Login exitoso** — devuelve un token válido
2. **Creación de tarea** — con token, responde \`201\` y la tarea creada
3. **Rechazo sin token** — \`GET /tasks\` sin token devuelve \`401\`

---
