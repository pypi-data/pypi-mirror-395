import os
import sys
import typer
import signal
import subprocess
import shutil
from pathlib import Path
from .install_local_layers import install_layers
from .build_local_api import build_local_api
from .build_api_json import build_api_json
from ...globals import Config

def on_cancel():
    typer.echo("\n[+] Cancelado por el usuario. Ejecutando limpieza…")
def on_error(code: int):
    typer.echo(f"[!] El servidor terminó con error (código {code}).")

def on_ok():
    typer.echo("[✓] El servidor terminó normalmente.")

def main(project_config: Config):
    lambdas_path = Path(os.getcwd()).joinpath(project_config.project.folders.lambdas)
    api_path = Path(os.getcwd()).joinpath(project_config.project.folders.root).parent.joinpath('api.yaml')
    base_path = Path(os.getcwd()).joinpath(project_config.project.folders.root).parent

    typer.echo('Instalando bibliotecas locales…')
    build_local_api(lambdas_path, base_path)

    typer.echo('Generando definición OpenAPI…')
    build_api_json(api_path, lambdas_path, base_path)
    shutil.copy(Path(__file__).parent / "main_server.py", base_path / "src/api_local/main_server.py")
    cmd = [sys.executable, "-m", "fastapi", "dev", base_path / "src/api_local/main_server.py"]

    # Lanzamos el proceso para poder controlarlo en Ctrl+C
    proc = subprocess.Popen(cmd)

    try:
        proc.wait()  # Espera a que termine
    except KeyboardInterrupt:
        # Usuario presionó Ctrl+C: pedimos al hijo que se cierre y corremos tu bloque
        typer.echo("\n[!] Ctrl+C detectado. Deteniendo servidor…")
        if os.name == "nt":
            # En Windows manda CTRL_BREAK (más fiable que CTRL_C a veces)
            proc.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        on_cancel()
        return

    # Si no fue KeyboardInterrupt, revisamos cómo terminó
    rc = proc.returncode
    if rc == 0:
        on_ok()
    elif rc < 0 and abs(rc) == signal.SIGINT:
        # Algunos entornos devuelven código negativo si terminó por SIGINT
        on_cancel()
    else:
        on_error(rc)
