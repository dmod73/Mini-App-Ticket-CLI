"""
Módulo para manejar la lectura y escritura de archivos de datos.
Usa formato JSON por línea para guardar registros de forma simple.
"""
import os
import json

# Detectar la raíz del proyecto (donde está app.py)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# Crear las carpetas si no existen
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)


def read_json_lines(path: str) -> list[dict]:
    """
    Lee un archivo donde cada línea es un JSON independiente.
    Ignora líneas vacías y líneas con errores de formato.
    """
    records = []
    
    # Si el archivo no existe, devolver lista vacía
    if not os.path.exists(path):
        return records
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Ignorar líneas vacías
            if not line:
                continue
            try:
                # Intentar convertir la línea a dict
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                # Si hay error, simplemente ignorar esa línea
                continue
    
    return records


def write_json_lines(path: str, records: list[dict]) -> None:
    """
    Escribe una lista de registros al archivo, cada uno en su propia línea.
    Usa un archivo temporal para evitar corrupción si algo falla.
    """
    temp_path = path + ".tmp"
    
    # Escribir primero al archivo temporal
    with open(temp_path, "w", encoding="utf-8") as f:
        for record in records:
            json_line = json.dumps(record, ensure_ascii=False)
            f.write(json_line + "\n")
    
    # Reemplazar el archivo original con el temporal
    if os.path.exists(path):
        os.remove(path)
    os.rename(temp_path, path)


def append_json_line(path: str, record: dict) -> None:
    """
    Agrega un nuevo registro al final del archivo.
    Si el archivo no existe, lo crea.
    """
    with open(path, "a", encoding="utf-8") as f:
        json_line = json.dumps(record, ensure_ascii=False)
        f.write(json_line + "\n")
