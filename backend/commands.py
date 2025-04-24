import subprocess
import pyautogui
import time
import webbrowser
import os

# Función para ejecutar comandos locales
def ejecutar_comando_local(texto: str) -> str:
    texto = texto.lower()

    # Comando para mostrar la ayuda
    if texto == "/help":
        return (
        "Aquí tienes una lista de los comandos disponibles:\n\n"
        "1. /calculadora: Abre la calculadora.\n"
        "2. /bloc de notas: Abre el Bloc de Notas.\n"
        "3. /explorador de archivos: Abre el explorador de archivos.\n"
        "4. /escribir [texto]: Escribe el texto proporcionado en el Bloc de Notas.\n"
        "5. /abrir navegador [url]: Abre el navegador y carga la URL proporcionada.\n"
        "6. /captura: Toma una captura de pantalla.\n"
        "7. /buscar [término]: Realiza una búsqueda en Google del término proporcionado.\n"
        "8. /cerrar [nombre de la aplicación]: Cierra la aplicación proporcionada (por ejemplo, 'notepad.exe').\n\n"
        "Para ejecutar un comando, solo debes escribirlo en la conversación.\n"
        "Recuerda que los comandos deben empezar con el carácter '/'."
        )

    # Comando para abrir la calculadora
    elif "calculadora" in texto:
        subprocess.Popen("calc.exe")
        return "🧮 Calculadora abierta."

    # Comando para abrir el Bloc de Notas
    elif "bloc de notas" in texto or "notas" in texto:
        subprocess.Popen("notepad.exe")
        return "📓 Bloc de notas abierto."

    # Comando para abrir el explorador de archivos
    elif "explorador de archivos" in texto:
        subprocess.Popen("explorer.exe")
        return "🗂️ Explorador de archivos abierto."

    # Comando para escribir en el Bloc de Notas
    elif texto.startswith("/escribir "):
        texto_a_escribir = texto[len("/escribir "):].strip()
        if texto_a_escribir:
            subprocess.Popen("notepad.exe")
            time.sleep(1)
            pyautogui.typewrite(texto_a_escribir)
            return f"✍️ Escribí en el Bloc de Notas: {texto_a_escribir}"

    # Comando para abrir el navegador y cargar una URL
    elif texto.startswith("/abrir navegador "):
        url = texto[len("/abrir navegador "):].strip()
        if url:
            webbrowser.open(url)
            return f"🌐 Abriendo navegador con la URL: {url}"

    # Comando para tomar una captura de pantalla
    elif texto == "/captura":
        screenshot = pyautogui.screenshot()
        screenshot.save("captura.png")  # Guarda la captura como "captura.png"
        return "📸 Captura de pantalla tomada y guardada como 'captura.png'."

    # Comando para realizar una búsqueda en Google
    elif texto.startswith("/buscar "):
        search_term = texto[len("/buscar "):].strip()
        if search_term:
            search_url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(search_url)
            return f"🔍 Buscando en Google: {search_term}"

    # Comando para cerrar una aplicación
    elif texto.startswith("/cerrar "):
        app_name = texto[len("/cerrar "):].strip()
        try:
            # Esto cierra una aplicación por su nombre (por ejemplo: "notepad.exe")
            subprocess.Popen(f"taskkill /f /im {app_name}")
            return f"❌ Aplicación {app_name} cerrada."
        except Exception as e:
            return f"⚠️ No se pudo cerrar la aplicación {app_name}. Error: {str(e)}"

    return None  # No es un comando local reconocido
