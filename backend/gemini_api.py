# backend/gemini_api.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave API de la variable de entorno
api_key = os.getenv("GEMINI_API_KEY")

# Verificar si la clave API se cargó correctamente
if api_key is None:
    raise ValueError("La clave API de Gemini no se ha encontrado. Asegúrate de que esté en el archivo .env")

# Crear el cliente con la clave API de Gemini
client = genai.Client(api_key=api_key)

def obtener_respuesta(mensaje_usuario: str) -> str:
    try:
        print(f"Solicitando respuesta para el mensaje: {mensaje_usuario}")
        respuesta = genai.generate_text(
            model="gemini-2.0-flash",  # Modelo adecuado (ajusta si es necesario)
            prompt=mensaje_usuario
        )
        print(f"Respuesta obtenida: {respuesta.text}")
        return respuesta.text  # Devuelve el texto generado por Gemini
    except Exception as e:
        print(f"Error al obtener respuesta de Gemini: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al procesar la solicitud con Gemini.")


