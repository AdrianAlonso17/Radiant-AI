import subprocess
import os
import time
import sys

def ensure_psutil_installed():
    try:
        import psutil
    except ImportError:
        print("psutil no está instalado. Instalando psutil...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
    return psutil

def run_command(command, cwd=None):
    """
    Ejecuta un comando dentro de PowerShell y espera a que termine.
    """
    print(f"Ejecutando: {' '.join(command)} en {cwd or os.getcwd()}")
    command_str = ' '.join(command)
    powershell_cmd = ['powershell.exe', '-NoProfile', '-Command', command_str]
    result = subprocess.run(powershell_cmd, cwd=cwd, shell=False)
    if result.returncode != 0:
        raise RuntimeError(f"Error al ejecutar {command_str}")

def frontend_install_if_needed(frontend_dir):
    node_modules_path = os.path.join(frontend_dir, 'node_modules')
    if not os.path.exists(node_modules_path):
        print("Instalando dependencias frontend...")
        run_command(['npm', 'install'], cwd=frontend_dir)
        run_command(['npm', 'install', 'react-router-dom', 'axios'], cwd=frontend_dir)
    else:
        print("Dependencias frontend ya instaladas.")

def backend_install_always(backend_dir):
    print("Instalando dependencias backend (sin comprobación)...")
    run_command(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'], cwd=backend_dir)

def kill_processes_by_name(name_keywords, psutil):
    """
    Mata todos los procesos que contengan alguna de las palabras clave en su cmdline,
    excepto este proceso y sus hijos.
    """
    current_pid = os.getpid()
    current_process = psutil.Process(current_pid)
    children_pids = [p.pid for p in current_process.children(recursive=True)]

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.pid == current_pid or proc.pid in children_pids:
                continue  # No matar este proceso ni sus hijos

            cmdline = proc.info.get('cmdline')
            if not cmdline:
                continue
            cmd = ' '.join(cmdline).lower()

            if any(keyword.lower() in cmd for keyword in name_keywords):
                print(f"Terminando proceso: {cmd} (pid {proc.pid})")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except psutil.TimeoutExpired:
                    print(f"Proceso {proc.pid} no terminó, matando forzadamente")
                    proc.kill()
                    proc.wait(timeout=5)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def main():
    # Detectar directorio base
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    BACKEND_DIR = os.path.join(base_dir, 'backend')
    FRONTEND_DIR = os.path.join(base_dir, 'frontend')

    print(f"Directorio base: {base_dir}")
    print(f"Directorio backend: {BACKEND_DIR}")
    print(f"Directorio frontend: {FRONTEND_DIR}")

    # Instalar dependencias backend
    backend_install_always(BACKEND_DIR)

    # Asegurar psutil instalado antes de usarlo
    psutil = ensure_psutil_installed()

    # Cerrar procesos que puedan estar usando puertos o archivos
    kill_processes_by_name(['npm', 'react-scripts', 'webpack', 'uvicorn'], psutil)

    time.sleep(2)

    # Instalar frontend si es necesario
    frontend_install_if_needed(FRONTEND_DIR)

    print("Lanzando backend con uvicorn...")
    backend_cmd = f'{sys.executable} -m uvicorn main:app --reload'
    backend_process = subprocess.Popen(
        ['powershell.exe', '-NoProfile', '-Command', backend_cmd],
        cwd=BACKEND_DIR,
        shell=False
    )

    time.sleep(3)

    print("Lanzando frontend con npm start...")
    frontend_process = subprocess.Popen(
        ['powershell.exe', '-NoProfile', '-Command', 'npm start'],
        cwd=FRONTEND_DIR,
        shell=False
    )

    try:
        # Esperar procesos hasta Ctrl+C
        while True:
            if backend_process.poll() is not None:
                print("El backend terminó inesperadamente.")
                break
            if frontend_process.poll() is not None:
                print("El frontend terminó inesperadamente.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSe detectó interrupción por teclado. Cerrando procesos...")
    finally:
        for proc in (backend_process, frontend_process):
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()

if __name__ == "__main__":
    main()
