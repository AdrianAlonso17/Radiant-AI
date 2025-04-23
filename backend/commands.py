import subprocess

def ejecutar_comando_local(texto: str) -> str:
    texto = texto.lower()

    if "calculadora" in texto:
        subprocess.Popen("calc.exe")
        return "🧮 Calculadora abierta."

    elif "bloc de notas" in texto or "notas" in texto:
        subprocess.Popen("notepad.exe")
        return "📓 Bloc de notas abierto."

    elif "explorador de archivos" in texto:
        subprocess.Popen("explorer.exe")
        return "🗂️ Explorador de archivos abierto."

    return None  # No es un comando local reconocido
