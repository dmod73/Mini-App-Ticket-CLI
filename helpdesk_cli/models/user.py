"""
Modelo que representa un usuario en el sistema.
Usa dataclass para simplificar la definición de la clase.
"""
from dataclasses import dataclass


@dataclass
class User:
    """
    Representa un usuario con toda su información.
    """
    id: str
    username: str
    password_hash: str
    role: str  # "user" o "agent"
    created_at: str
    updated_at: str
    
    def to_dict(self) -> dict:
        """
        Convierte el usuario a un diccionario para guardarlo en archivo.
        """
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "User":
        """
        Crea un objeto User desde un diccionario.
        Convierte todos los campos a string para evitar errores.
        """
        return User(
            id=str(data.get("id", "")),
            username=str(data.get("username", "")),
            password_hash=str(data.get("password_hash", "")),
            role=str(data.get("role", "")),
            created_at=str(data.get("created_at", "")),
            updated_at=str(data.get("updated_at", "")),
        )
