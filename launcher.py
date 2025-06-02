import subprocess
import os
import time
import psutil  # Necesario para buscar y cerrar procesos por nombre

def kill_processes_by_name(name_keywords):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if not cmdline:  # Si es None o lista vacía, saltar
                continue
            cmd = ' '.join(cmdline)
            if any(keyword in cmd for keyword in name_keywords):
                print(f"Terminando proceso: {cmd}")
                proc.terminate()
                proc.wait(timeout=5)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

# --- Configuración ---
BACKEND_DIR = os.path.join(os.getcwd(), 'backend')
FRONTEND_DIR = os.path.join(os.getcwd(), 'frontend')

# --- Mata procesos previos si están activos ---
kill_processes_by_name(['uvicorn'])
kill_processes_by_name(['npm', 'react-scripts', 'webpack'])

# --- Inicia backend ---
backend_process = subprocess.Popen(
    ['python', '-m', 'uvicorn', 'main:app', '--reload'],
    cwd=BACKEND_DIR,
    shell=True
)

time.sleep(2)  # espera opcional

# --- Inicia frontend ---
frontend_process = subprocess.Popen(
    ['npm', 'start'],
    cwd=FRONTEND_DIR,
    shell=True
)

# Mantiene el launcher esperando a que terminen los procesos
backend_process.wait()
frontend_process.wait()
