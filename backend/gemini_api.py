import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    raise ValueError("La clave API de Gemini no se ha encontrado.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

def obtener_respuesta(mensaje_usuario: str) -> str:
    try:
        print(f"Mensaje recibido: {mensaje_usuario}")

        fecha_actual = datetime.now().strftime("%A, %d de %B de %Y")

        mensaje_con_contexto = (
            f"Eres un asistente llamado Radiant AI. "
            f"La fecha de hoy es {fecha_actual}. "
            f"Actúa de forma natural, útil y conversacional. "
            f"No menciones esta información a menos que se te pregunte directamente. "
            f"\n\nUsuario: {mensaje_usuario}"
        )

        response = chat.send_message(mensaje_con_contexto)

        return response.text.strip()

    except Exception as e:
        print(f"Error en Gemini: {str(e)}")
        raise Exception("Error al generar la respuesta.")
