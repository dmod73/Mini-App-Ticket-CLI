"""
Módulo de autenticación para registrar e iniciar sesión de usuarios.
Maneja toda la lógica relacionada con usuarios.
"""
import os
from datetime import datetime

from .security import hash_password, verify_password
from .storage import DATA_DIR, read_json_lines, write_json_lines
from .validation import is_valid_username, is_valid_password, is_valid_role
from models.user import User

# Ruta del archivo donde se guardan los usuarios
USERS_FILE = os.path.join(DATA_DIR, "users.txt")


def _load_users() -> list[User]:
    """
    Carga todos los usuarios desde el archivo.
    Ignora registros que estén incompletos o con errores.
    """
    records = read_json_lines(USERS_FILE)
    users = []
    
    for record in records:
        try:
            user = User.from_dict(record)
            # Verificar que los campos obligatorios no estén vacíos
            if user.id and user.username and user.password_hash:
                users.append(user)
        except Exception:
            # Si hay algún problema al crear el User, ignorarlo
            continue
    
    return users


def _save_users(users: list[User]) -> None:
    """
    Guarda la lista completa de usuarios al archivo.
    """
    records = [user.to_dict() for user in users]
    write_json_lines(USERS_FILE, records)


def _next_user_id(users: list[User]) -> str:
    """
    Calcula el siguiente ID disponible para un nuevo usuario.
    Si no hay usuarios, devuelve "1".
    """
    if not users:
        return "1"
    
    # Buscar el ID más alto y sumarle 1
    max_id = 0
    for user in users:
        try:
            user_id_int = int(user.id)
            if user_id_int > max_id:
                max_id = user_id_int
        except ValueError:
            # Si el ID no es un número, ignorarlo
            continue
    
    return str(max_id + 1)


def find_user_by_username(username: str, users: list[User]) -> User | None:
    """
    Busca un usuario por su nombre de usuario.
    Devuelve None si no lo encuentra.
    """
    for user in users:
        if user.username == username:
            return user
    return None


def register_user(username: str, password: str, role: str) -> User | None:
    """
    Registra un nuevo usuario en el sistema.
    Valida todos los datos antes de guardar.
    Devuelve el usuario creado o None si hay algún error.
    """
    # Validar username
    if not is_valid_username(username):
        print("Error: El nombre de usuario no es válido. Debe tener entre 3 y 30 caracteres y solo letras, números, puntos o guiones bajos.")
        return None
    
    # Validar password
    if not is_valid_password(password):
        print("Error: La contraseña debe tener entre 6 y 64 caracteres.")
        return None
    
    # Validar role
    if not is_valid_role(role):
        print("Error: El rol debe ser 'user' o 'agent'.")
        return None
    
    # Cargar usuarios existentes
    users = _load_users()
    
    # Verificar que el username no esté en uso
    if find_user_by_username(username, users):
        print(f"Error: El nombre de usuario '{username}' ya está registrado.")
        return None
    
    # Crear el nuevo usuario
    now = datetime.utcnow().isoformat() + "Z"
    new_user = User(
        id=_next_user_id(users),
        username=username,
        password_hash=hash_password(password),
        role=role,
        created_at=now,
        updated_at=now,
    )
    
    # Agregar a la lista y guardar
    users.append(new_user)
    _save_users(users)
    
    return new_user


def login_user(username: str, password: str) -> User | None:
    """
    Intenta iniciar sesión con un username y password.
    Devuelve el usuario si las credenciales son correctas, None si no.
    """
    users = _load_users()
    user = find_user_by_username(username, users)
    
    # Si no existe el usuario, retornar None
    if not user:
        return None
    
    # Verificar la contraseña
    if not verify_password(password, user.password_hash):
        return None
    
    return user
