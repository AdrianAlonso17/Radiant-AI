import torch
import torch.nn as nn
import subprocess
import pyautogui
import time
import webbrowser
import datetime
from sklearn.feature_extraction.text import CountVectorizer


class CommandClassifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super().__init__()
        self.linear = nn.Linear(input_size, num_classes)

    def forward(self, x):
        return self.linear(x)


class AsistenteComandosIA:
    def __init__(self):
        self.train_data = [
            ("abre la calculadora", "abrir_calculadora"),
            ("inicia la calculadora", "abrir_calculadora"),
            ("quiero usar la calculadora", "abrir_calculadora"),
            ("abre el bloc de notas", "abrir_bloc"),
            ("inicia el bloc de notas", "abrir_bloc"),
            ("abre el bloc", "abrir_bloc"),
            ("haz una captura", "captura_pantalla"),
            ("haz una captura de pantalla", "captura_pantalla"),
            ("saca una captura", "captura_pantalla"),
            ("busca gatos en google", "buscar_en_google"),
            ("búscame gatos en google", "buscar_en_google"),
            ("quiero ver gatos en internet", "buscar_en_google"),
            ("cierra el bloc de notas", "cerrar_bloc"),
            ("sal del bloc de notas", "cerrar_bloc"),
            ("cierra el bloc", "cerrar_bloc"),
            ("abre el explorador de archivos", "abrir_explorador"),
            ("abre el explorador", "abrir_explorador"),
            ("quiero ver mis carpetas", "abrir_explorador"),
            ("escribe hola mundo", "escribir_texto"),
            ("pon hola mundo", "escribir_texto"),
            ("escribe el texto hola mundo", "escribir_texto"),
            ("bloquea la pantalla", "bloquear_pantalla"),
            ("bloquear pantalla", "bloquear_pantalla"),
            ("bloquea el ordenador", "bloquear_pantalla"),
            ("reinicia", "reiniciar_pc"),
            ("reinicia el ordenador", "reiniciar_pc"),
            ("reinicia el sistema", "reiniciar_pc"),
            ("apaga", "apagar_pc"),
            ("apaga el ordenador", "apagar_pc"),
            ("quiero apagar el PC", "apagar_pc"),
            ("abre paint", "abrir_paint"),
            ("inicia paint", "abrir_paint"),
            ("abre el programa de dibujo", "abrir_paint"),
            ("abre cmd", "abrir_cmd"),
            ("abre la consola", "abrir_cmd"),
            ("abre el símbolo del sistema", "abrir_cmd"),
            ("abre powershell", "abrir_powershell"),
            ("inicia powershell", "abrir_powershell"),
            ("ejecuta powershell", "abrir_powershell"),
            ("cierra la calculadora", "cerrar_calculadora"),
            ("sal de la calculadora", "cerrar_calculadora"),
            ("termina la calculadora", "cerrar_calculadora"),
            ("muestra la hora", "mostrar_hora"),
            ("qué hora es", "mostrar_hora"),
            ("dime la hora", "mostrar_hora"),
            ("vacía la papelera", "vaciar_papelera"),
            ("vaciar la papelera", "vaciar_papelera"),
            ("quiero vaciar la papelera", "vaciar_papelera"),
        ]

        texts, labels = zip(*self.train_data)
        self.vectorizer = CountVectorizer()
        X = self.vectorizer.fit_transform(texts).toarray()

        self.label_to_idx = {label: i for i, label in enumerate(set(labels))}
        self.idx_to_label = {i: label for label, i in self.label_to_idx.items()}
        y = torch.tensor([self.label_to_idx[label] for label in labels])

        self.model = CommandClassifier(input_size=X.shape[1], num_classes=len(self.label_to_idx))
        loss_fn = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)

        for _ in range(100):
            inputs = torch.tensor(X).float()
            outputs = self.model(inputs)
            loss = loss_fn(outputs, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    def interpretar(self, texto_usuario):
        texto_usuario = texto_usuario.lower()
        vect = self.vectorizer.transform([texto_usuario]).toarray()
        with torch.no_grad():
            output = self.model(torch.tensor(vect).float())
            predicted_idx = torch.argmax(output, dim=1).item()
            return self.idx_to_label[predicted_idx]

    def ejecutar(self, texto_usuario):
        texto_usuario = texto_usuario.strip()
        intencion = self.interpretar(texto_usuario)

        try:
            if intencion == "abrir_calculadora":
                subprocess.Popen("calc.exe")
                return "🧮 Calculadora abierta."

            elif intencion == "abrir_bloc":
                subprocess.Popen("notepad.exe")
                return "📓 Bloc de notas abierto."

            elif intencion == "captura_pantalla":
                screenshot = pyautogui.screenshot()
                screenshot.save("captura.png")
                return "📸 Captura guardada como 'captura.png'."

            elif intencion == "buscar_en_google":
                termino = texto_usuario.replace("busca", "").strip()
                url = f"https://www.google.com/search?q={termino}"
                webbrowser.open(url)
                return f"🔍 Buscando: {termino}"

            elif intencion == "cerrar_bloc":
                subprocess.Popen("taskkill /f /im notepad.exe")
                return "❌ Bloc de notas cerrado."

            elif intencion == "abrir_explorador":
                subprocess.Popen("explorer.exe")
                return "🗂️ Explorador de archivos abierto."

            elif intencion == "escribir_texto":
                texto = texto_usuario.replace("escribe", "").strip()
                subprocess.Popen("notepad.exe")
                time.sleep(1)
                pyautogui.typewrite(texto)
                return f"✍️ Texto escrito: {texto}"

            elif intencion == "bloquear_pantalla":
                subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")
                return "🔒 Pantalla bloqueada."

            elif intencion == "reiniciar_pc":
                subprocess.Popen("shutdown /r /t 0")
                return "🔁 Reiniciando el equipo..."

            elif intencion == "apagar_pc":
                subprocess.Popen("shutdown /s /t 0")
                return "⏻ Apagando el equipo..."

            elif intencion == "abrir_paint":
                subprocess.Popen("mspaint.exe")
                return "🎨 Paint abierto."

            elif intencion == "abrir_cmd":
                subprocess.Popen("cmd.exe", creationflags=subprocess.CREATE_NEW_CONSOLE)
                return "🖥️ CMD abierto."

            elif intencion == "cerrar_calculadora":
                subprocess.Popen("taskkill /f /im calc.exe")
                return "❌ Calculadora cerrada."

            elif intencion == "mostrar_hora":
                return f"🕒 Hora actual: {datetime.datetime.now().strftime('%H:%M:%S')}"

            elif intencion == "vaciar_papelera":
                subprocess.call(['powershell', '-command', 'Clear-RecycleBin', '-Force'])
                return "🗑️ Papelera vaciada."

            return "🤖 Comando no reconocido."
        
        except Exception as e:
            return f"❌ Error al ejecutar el comando: {str(e)}"

asistente_ia = AsistenteComandosIA()

def ejecutar_comando_local(texto: str) -> str:
    return asistente_ia.ejecutar(texto)
