"""
Módulo para el manejo seguro de contraseñas.
Usa SHA-256 para hashear las contraseñas antes de guardarlas.
"""
import hashlib


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en texto plano a un hash SHA-256.
    Devuelve el hash en formato hexadecimal.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con un hash guardado.
    Retorna True si coinciden, False si no.
    """
    return hash_password(password) == password_hash
