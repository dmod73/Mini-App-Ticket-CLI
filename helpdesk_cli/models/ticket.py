"""
Modelo que representa un ticket de soporte en el sistema.
Contiene toda la información relacionada con las solicitudes de ayuda.
"""
from dataclasses import dataclass


@dataclass
class Ticket:
    """
    Representa un ticket de soporte con toda su información.
    Los tickets son creados por usuarios y pueden ser asignados a agentes.
    """
    id: str
    owner_id: str  # Usuario que creó el ticket
    title: str
    description: str
    status: str  # "open", "in_progress" o "closed"
    priority: str  # "low", "medium" o "high"
    assignee_id: str  # ID del agente asignado o "" si no tiene
    created_at: str
    updated_at: str
    
    def to_dict(self) -> dict:
        """
        Convierte el ticket a un diccionario para guardarlo en archivo.
        """
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assignee_id": self.assignee_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Ticket":
        """
        Crea un objeto Ticket desde un diccionario.
        Convierte todos los campos a string para evitar errores.
        """
        return Ticket(
            id=str(data.get("id", "")),
            owner_id=str(data.get("owner_id", "")),
            title=str(data.get("title", "")),
            description=str(data.get("description", "")),
            status=str(data.get("status", "")),
            priority=str(data.get("priority", "")),
            assignee_id=str(data.get("assignee_id", "")),
            created_at=str(data.get("created_at", "")),
            updated_at=str(data.get("updated_at", "")),
        )
