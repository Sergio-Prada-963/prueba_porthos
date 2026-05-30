# 🤖 Módulo 2 · Inteligencia Artificial

## 📝 Descripción

Microservicio **FastAPI** que expone un endpoint `POST /responder` para generar respuestas profesionales y empáticas a mensajes de clientes. Internamente consulta la API de **Anthropic** (`claude-haiku-4-5`) con un prompt diseñado para una empresa ficticia llamada **CafeAroma** — una tienda online de café de especialidad.

---

## 🎯 Características

- ✅ Endpoint `POST /responder` con validación de entrada vía Pydantic
- ✅ Prompt con contexto de negocio + restricciones de tono y extensión (máx. 3 oraciones)
- ✅ Manejo explícito de errores: timeout, rate limit, fallo de conexión, respuestas vacías y truncadas por `max_tokens`
- ✅ 3 casos (queja, consulta, felicitación) en `ejemplos.md`
- ✅ Clave de API y modelo configurables vía `.env`

---

## 📂 Estructura

```
modulo2_ia/
├── main.py                # App FastAPI con el endpoint /responder
├── ejemplos.md            # Resultados generados por el modelo
├── requirements.txt       # Dependencias Python
├── .env.example           # Plantilla de variables de entorno
├── .env                   # Variables reales (ignorado por git)
└── .gitignore
```

---

## 🚀 Instalación

### Requisitos

- **Python 3.10+**
- Una **API key de Anthropic** (`sk-ant-...`)

### Pasos

```bash
cd modulo2_ia

# Crear entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar la clave de Anthropic
cp .env.example .env
# Editar .env y reemplazar el valor de ANTHROPIC_API_KEY
```

---

## ▶️ Ejecución

### 1. Levantar el servidor

```bash
uvicorn main:app --reload
```

El servicio queda disponible en `http://127.0.0.1:8000`. La documentación interactiva (Swagger) está en `http://127.0.0.1:8000/docs`.

### 2. Probar el endpoint manualmente

```bash
curl -X POST http://127.0.0.1:8000/responder \
  -H "Content-Type: application/json" \
  -d '{
    "motivo": "consulta",
    "detalle": "¿El café de Nariño es bueno para V60?"
  }'
```

## 📐 Diseño del prompt

El `SYSTEM_PROMPT` (en `main.py`) define:

| Elemento          | Valor                                                                                |
| ----------------- | ------------------------------------------------------------------------------------ |
| **Empresa**       | CafeAroma — tienda online de café de especialidad (8 años de trayectoria)            |
| **Idioma**        | Español neutro                                                                       |
| **Extensión**     | Máximo 3 oraciones                                                                   |
| **Tono**          | Profesional, empático, cálido. Sin sarcasmo ni excesiva coloquialidad                |
| **Estructura**    | Adaptada por motivo: queja, consulta o felicitación                                  |
| **Restricciones** | Sin emojis, sin signos múltiples, sin inventar datos, sin promesas no respaldadas    |

El mensaje del usuario se envía como un bloque user con el motivo y el detalle del cliente claramente etiquetados.

---

## 🛡️ Manejo de errores

| Situación                            | Código | Respuesta                                                        |
| ------------------------------------ | ------ | ---------------------------------------------------------------- |
| Timeout de la API (>20 s)            | `504`  | `La API de Anthropic tardó demasiado en responder.`             |
| Rate limit alcanzado                  | `429`  | `Se alcanzó el límite de peticiones de la API.`                 |
| Petición mal formada (400 desde API) | `400`  | Mensaje propagado desde la API                                   |
| Sin conexión con la API              | `502`  | `No se pudo conectar con la API de Anthropic.`                  |
| Respuesta truncada por `max_tokens`  | `502`  | `La respuesta excedió el límite de tokens configurado.`         |
| Respuesta vacía                       | `502`  | `La API devolvió una respuesta vacía.`                          |
| Validación de entrada (Pydantic)      | `422`  | Detalle automático del campo inválido                            |

---

## 📋 Resultados de prueba

Ver el archivo [`ejemplos.md`](./ejemplos.md) con los 3 casos generados:

1. **Queja** — pedido dañado por segunda vez
2. **Consulta** — recomendación de método de preparación y nivel de acidez
3. **Felicitación** — agradecimiento por un detalle de empaque

---
