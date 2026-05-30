import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from anthropic import Anthropic, APITimeoutError, RateLimitError, BadRequestError, APIStatusError, APIConnectionError

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise RuntimeError("Falta ANTHROPIC_API_KEY en el archivo .env")

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
client = Anthropic(api_key=API_KEY, timeout=20.0)
app = FastAPI(title="Asistente de Respuestas a Clientes", version="1.0.0")

class MensajeCliente(BaseModel):
    motivo: str = Field(..., min_length=2, max_length=120, description="Motivo del contacto: queja, consulta, felicitación, etc.")
    detalle: str = Field(..., min_length=5, max_length=2000, description="Texto del cliente con el detalle del mensaje")

class RespuestaGenerada(BaseModel):
    motivo: str
    respuesta: str
    modelo: str
    tokens_entrada: int
    tokens_salida: int

SYSTEM_PROMPT = """Eres el asistente virtual de atención al cliente de "CaféAroma", una tienda online colombiana con 8 años de trayectoria, especializada en café de origen único y accesorios para baristas caseros. Nuestros valores de marca son cercanía, transparencia y pasión por el café de especialidad.

Tu tarea es redactar la respuesta al mensaje de un cliente. Debes cumplir estrictamente con las siguientes reglas de formato, tono y contenido:

[REGLAS CRÍTICAS DE FORMATO Y TONO]
1. Idioma: Español neutro y natural (evita regionalismos marcados).
2. Extensión: MÁXIMO 3 oraciones. Sé directo y conciso.
3. Tono: Profesional, empático y cálido. Queda prohibido el sarcasmo, la condescendencia o el lenguaje excesivamente informal.
4. Restricción de salida: Devuelve ÚNICAMENTE el texto de la respuesta. No incluyas introducciones, ni saludos del tipo "Hola,", ni firmas al final, ni comillas, ni etiquetas de sistema.

[REGLAS DE CONTENIDO Y CONTROL DE ALUCINACIONES]
1. No inventes datos específicos (números de pedido, fechas, nombres de empleados o plazos exactos) que no estén explícitos en el mensaje del cliente.
2. No prometas reembolsos automáticos ni soluciones comerciales definitivas si no tienes la información para confirmarlo.
3. No utilices emojis ni signos de exclamación múltiples (¡!).

[ESTRUCTURA SEGÚN EL TIPO DE MENSAJE]
Identifica el motivo del cliente y aplica la estructura correspondiente en tus 3 oraciones:
- Si es una QUEJA: 1) Reconoce e internaliza el inconveniente con empatía, 2) Ofrece una acción concreta de seguimiento o solución, 3) Agradece la paciencia del cliente.
- Si es una CONSULTA: 1) Responde directamente a la duda o indica el siguiente paso exacto, 2) Invita cordialmente a continuar la conversación o profundizar.
- Si es una FELICITACIÓN: 1) Agradece de forma sincera, 2) Refuerza el compromiso de CaféAroma con la calidad de nuestro café de especialidad."""


def construir_prompt_usuario(motivo: str, detalle: str) -> str:
    return (
        f"Motivo del mensaje: {motivo.strip()}\n"
        f"Mensaje del cliente:\n\"\"\"\n{detalle.strip()}\n\"\"\"\n\n"
        "Redacta la respuesta cumpliendo las reglas indicadas."
    )

@app.get("/")
def home():
    return {"servicio": "Asistente de Respuestas a Clientes", "modelo": MODEL, "endpoint": "POST /responder"}

@app.post("/responder", response_model=RespuestaGenerada)
def responder(mensaje: MensajeCliente):
    try:
        resultado = client.messages.create(
            model=MODEL,
            max_tokens=300,
            temperature=0.4,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": construir_prompt_usuario(mensaje.motivo, mensaje.detalle)}],
        )
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="La API de Anthropic tardó demasiado en responder.")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Se alcanzó el límite de peticiones de la API. Intenta más tarde.")
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Petición inválida hacia la API: {e.message}")
    except APIConnectionError:
        raise HTTPException(status_code=502, detail="No se pudo conectar con la API de Anthropic.")
    except APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"Error de la API ({e.status_code}): {e.message}")

    if resultado.stop_reason == "max_tokens":
        raise HTTPException(status_code=502, detail="La respuesta excedió el límite de tokens configurado.")

    texto = "".join(bloque.text for bloque in resultado.content if bloque.type == "text").strip()
    if not texto:
        raise HTTPException(status_code=502, detail="La API devolvió una respuesta vacía.")

    return RespuestaGenerada(
        motivo=mensaje.motivo,
        respuesta=texto,
        modelo=resultado.model,
        tokens_entrada=resultado.usage.input_tokens,
        tokens_salida=resultado.usage.output_tokens,
    )
