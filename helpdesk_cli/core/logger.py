"""
Módulo de auditoría para registrar las acciones importantes del sistema.
Guarda logs en formato JSON para facilitar análisis posterior.
"""
import os
from datetime import datetime
from .storage import LOGS_DIR, append_json_line

# Archivo donde se guardan los logs de auditoría
AUDIT_LOG_FILE = os.path.join(LOGS_DIR, "audit.log")


def log_action(
    user,
    action: str,
    entity: str,
    entity_id: str,
    status: str,
    details: str = "",
) -> None:
    """
    Registra una acción en el log de auditoría.
    
    Parámetros:
    - user: Objeto User o None si es acción anónima
    - action: Tipo de acción (ej: LOGIN, REGISTER, etc.)
    - entity: Tipo de entidad afectada (ej: user, ticket)
    - entity_id: ID de la entidad
    - status: success o failed
    - details: Información adicional (máximo 200 caracteres)
    """
    # Extraer información del usuario si existe
    if user is not None:
        user_id = user.id
        role = user.role
        username = user.username
    else:
        user_id = "anonymous"
        role = "unknown"
        username = "unknown"
    
    # Truncar los detalles si son muy largos
    if len(details) > 200:
        details = details[:200]
    
    # Crear el registro de log
    log_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "username": username,
        "role": role,
        "action": action,
        "entity": entity,
        "entity_id": str(entity_id),
        "status": status,
        "details": details,
    }
    
    # Guardar en el archivo de logs
    # Nunca incluir contraseñas ni hashes aquí
    append_json_line(AUDIT_LOG_FILE, log_record)
