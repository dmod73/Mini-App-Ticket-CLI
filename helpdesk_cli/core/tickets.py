"""
Módulo de gestión de tickets de soporte.
Maneja todas las operaciones CRUD sobre tickets con control de acceso por rol.
"""
import os
from datetime import datetime
from typing import List, Optional

from .storage import DATA_DIR, read_json_lines, write_json_lines
from .validation import input_int_in_range, sanitize_text_field
from .logger import log_action
from models.ticket import Ticket
from models.user import User

# Ruta del archivo donde se guardan los tickets
TICKETS_FILE = os.path.join(DATA_DIR, "tickets.txt")

# Valores válidos para status y priority
STATUS_VALUES = ("open", "in_progress", "closed")
PRIORITY_VALUES = ("low", "medium", "high")


def is_valid_status(status: str) -> bool:
    """
    Verifica que el estado sea uno de los permitidos.
    """
    return status in STATUS_VALUES


def is_valid_priority(priority: str) -> bool:
    """
    Verifica que la prioridad sea una de las permitidas.
    """
    return priority in PRIORITY_VALUES


def _load_tickets() -> List[Ticket]:
    """
    Carga todos los tickets desde el archivo.
    Ignora registros que estén incompletos o con errores.
    """
    records = read_json_lines(TICKETS_FILE)
    tickets = []
    
    for record in records:
        try:
            ticket = Ticket.from_dict(record)
            # Verificar que los campos obligatorios no estén vacíos
            if ticket.id and ticket.owner_id and ticket.title:
                tickets.append(ticket)
        except Exception:
            # Si hay algún problema al crear el Ticket, ignorarlo
            continue
    
    return tickets


def _save_tickets(tickets: List[Ticket]) -> None:
    """
    Guarda la lista completa de tickets al archivo.
    """
    records = [ticket.to_dict() for ticket in tickets]
    write_json_lines(TICKETS_FILE, records)


def _next_ticket_id(tickets: List[Ticket]) -> str:
    """
    Calcula el siguiente ID disponible para un nuevo ticket.
    Si no hay tickets, devuelve "1".
    """
    if not tickets:
        return "1"
    
    # Buscar el ID más alto y sumarle 1
    max_id = 0
    for ticket in tickets:
        try:
            ticket_id_int = int(ticket.id)
            if ticket_id_int > max_id:
                max_id = ticket_id_int
        except ValueError:
            # Si el ID no es un número, ignorarlo
            continue
    
    return str(max_id + 1)


def _find_ticket_by_id(ticket_id: str, tickets: List[Ticket]) -> Optional[Ticket]:
    """
    Busca un ticket por su ID.
    Devuelve None si no lo encuentra.
    """
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket
    return None


def create_ticket(current_user: User) -> None:
    """
    Crea un nuevo ticket de soporte.
    Cualquier usuario autenticado puede crear tickets.
    """
    print("\n--- Crear nuevo ticket ---")
    
    # Pedir título y sanitizarlo
    # Nota: aunque el usuario escriba "' OR 1=1 --", se guarda como texto normal
    # en el JSON y no se ejecuta como código porque no usamos SQL.
    title = sanitize_text_field(input("Título del ticket: "), max_length=100)
    if not title or len(title) < 3:
        print("Error: El título debe tener entre 3 y 100 caracteres.")
        return
    
    # Pedir descripción y sanitizarla
    description = sanitize_text_field(input("Descripción del problema: "), max_length=500)
    if not description or len(description) < 3:
        print("Error: La descripción debe tener al menos 3 caracteres.")
        return
    
    # Pedir prioridad
    print("Prioridades disponibles: low, medium, high")
    priority = input("Prioridad: ").strip().lower()
    if not is_valid_priority(priority):
        print("Error: Prioridad inválida. Debe ser: low, medium o high.")
        return
    
    # Crear el ticket
    tickets = _load_tickets()
    now = datetime.utcnow().isoformat() + "Z"
    
    new_ticket = Ticket(
        id=_next_ticket_id(tickets),
        owner_id=current_user.id,
        title=title,
        description=description,
        status="open",
        priority=priority,
        assignee_id="",  # Sin asignar inicialmente
        created_at=now,
        updated_at=now,
    )
    
    # Guardar
    tickets.append(new_ticket)
    _save_tickets(tickets)
    
    print(f"\n✓ Ticket #{new_ticket.id} creado exitosamente.")
    
    # Registrar en logs
    log_action(
        user=current_user,
        action="TICKET_CREATE",
        entity="ticket",
        entity_id=new_ticket.id,
        status="success",
        details=f"Título: {title[:50]}, Prioridad: {priority}"
    )


def list_tickets(current_user: User) -> None:
    """
    Muestra una lista de tickets.
    Los usuarios ven solo sus tickets, los agentes ven todos.
    """
    print("\n--- Lista de tickets ---")
    
    tickets = _load_tickets()
    
    # Filtrar según el rol
    if current_user.role == "user":
        # Los usuarios solo ven sus propios tickets
        tickets = [t for t in tickets if t.owner_id == current_user.id]
    # Los agentes ven todos los tickets
    
    if not tickets:
        print("No hay tickets para mostrar.")
        return
    
    # Mostrar tabla de tickets
    print(f"\n{'ID':<5} {'Título':<30} {'Estado':<15} {'Prioridad':<10} {'Dueño':<10} {'Asignado':<10}")
    print("-" * 90)
    
    for ticket in tickets:
        assignee_display = ticket.assignee_id if ticket.assignee_id else "Sin asignar"
        print(f"{ticket.id:<5} {ticket.title[:28]:<30} {ticket.status:<15} {ticket.priority:<10} {ticket.owner_id:<10} {assignee_display:<10}")


def view_ticket_detail(current_user: User) -> None:
    """
    Muestra los detalles completos de un ticket específico.
    Los usuarios solo pueden ver sus propios tickets.
    """
    print("\n--- Ver detalle de ticket ---")
    
    ticket_id = input("ID del ticket: ").strip()
    
    tickets = _load_tickets()
    ticket = _find_ticket_by_id(ticket_id, tickets)
    
    if not ticket:
        print(f"Error: No existe un ticket con ID {ticket_id}.")
        return
    
    # Verificar permisos
    if current_user.role == "user" and ticket.owner_id != current_user.id:
        print("No tienes permiso para ver este ticket.")
        return
    
    # Mostrar detalles
    print("\n" + "=" * 60)
    print(f"ID:           {ticket.id}")
    print(f"Título:       {ticket.title}")
    print(f"Descripción:  {ticket.description}")
    print(f"Estado:       {ticket.status}")
    print(f"Prioridad:    {ticket.priority}")
    print(f"Dueño:        {ticket.owner_id}")
    print(f"Asignado a:   {ticket.assignee_id if ticket.assignee_id else 'Sin asignar'}")
    print(f"Creado:       {ticket.created_at}")
    print(f"Actualizado:  {ticket.updated_at}")
    print("=" * 60)


def update_ticket(current_user: User) -> None:
    """
    Permite editar un ticket existente.
    Los usuarios solo pueden editar sus propios tickets.
    Los agentes pueden editar cualquier ticket.
    """
    print("\n--- Editar ticket ---")
    
    ticket_id = input("ID del ticket a editar: ").strip()
    
    tickets = _load_tickets()
    ticket = _find_ticket_by_id(ticket_id, tickets)
    
    if not ticket:
        print(f"Error: No existe un ticket con ID {ticket_id}.")
        return
    
    # Verificar permisos
    if current_user.role == "user" and ticket.owner_id != current_user.id:
        print("No tienes permiso para editar este ticket.")
        return
    
    # Variables para rastrear cambios importantes
    changes_made = False
    old_status = ticket.status
    old_priority = ticket.priority
    old_assignee = ticket.assignee_id
    
    # Menú de edición
    while True:
        print(f"\n--- Editando ticket #{ticket.id} ---")
        print(f"Título actual: {ticket.title}")
        print(f"Descripción actual: {ticket.description[:50]}...")
        print(f"Prioridad actual: {ticket.priority}")
        print(f"Estado actual: {ticket.status}")
        print(f"Asignado a: {ticket.assignee_id if ticket.assignee_id else 'Sin asignar'}")
        print("\nOpciones:")
        print("1) Cambiar título")
        print("2) Cambiar descripción")
        print("3) Cambiar prioridad")
        print("4) Cambiar estado")
        
        # Opción de reasignar solo para agentes
        if current_user.role == "agent":
            print("5) Reasignar ticket")
            max_option = 5
        else:
            max_option = 4
        
        print("0) Guardar y volver")
        
        option = input_int_in_range("Elige una opción: ", 0, max_option)
        
        if option == 0:
            break
        
        elif option == 1:
            # Cambiar título (sanitizar entrada)
            new_title = sanitize_text_field(input("Nuevo título: "), max_length=100)
            if new_title and len(new_title) >= 3:
                ticket.title = new_title
                changes_made = True
                print("✓ Título actualizado.")
            else:
                print("Error: El título debe tener entre 3 y 100 caracteres.")
        
        elif option == 2:
            # Cambiar descripción (sanitizar entrada)
            new_description = sanitize_text_field(input("Nueva descripción: "), max_length=500)
            if new_description and len(new_description) >= 3:
                ticket.description = new_description
                changes_made = True
                print("✓ Descripción actualizada.")
            else:
                print("Error: La descripción debe tener al menos 3 caracteres.")
        
        elif option == 3:
            # Cambiar prioridad
            print("Prioridades: low, medium, high")
            new_priority = input("Nueva prioridad: ").strip().lower()
            if is_valid_priority(new_priority):
                ticket.priority = new_priority
                changes_made = True
                print("✓ Prioridad actualizada.")
            else:
                print("Error: Prioridad inválida.")
        
        elif option == 4:
            # Cambiar estado
            print("Estados: open, in_progress, closed")
            print(f"Estado actual: {ticket.status}")
            new_status = input("Nuevo estado: ").strip().lower()
            
            if not is_valid_status(new_status):
                print("Error: Estado inválido.")
                continue
            
            # Validar transiciones de estado
            valid_transition = False
            
            if ticket.status == "open" and new_status in ["in_progress", "closed"]:
                valid_transition = True
            elif ticket.status == "in_progress" and new_status == "closed":
                valid_transition = True
            elif ticket.status == new_status:
                print("El ticket ya tiene ese estado.")
                continue
            elif ticket.status == "closed":
                print("Error: Un ticket cerrado no puede reabrirse.")
                continue
            
            if valid_transition:
                ticket.status = new_status
                changes_made = True
                print("✓ Estado actualizado.")
            else:
                print(f"Error: No se puede cambiar de '{ticket.status}' a '{new_status}'.")
        
        elif option == 5 and current_user.role == "agent":
            # Reasignar ticket (solo agentes)
            print("Ingresa el ID del agente a asignar (o deja vacío para desasignar):")
            new_assignee = input("ID del agente: ").strip()
            ticket.assignee_id = new_assignee
            changes_made = True
            print("✓ Asignación actualizada.")
    
    # Si hubo cambios, guardar y registrar en logs
    if changes_made:
        # Actualizar timestamp
        ticket.updated_at = datetime.utcnow().isoformat() + "Z"
        _save_tickets(tickets)
        print("\n✓ Ticket actualizado exitosamente.")
        
        # Registrar cambios importantes en logs
        if ticket.status != old_status:
            log_action(
                user=current_user,
                action="TICKET_STATUS_CHANGE",
                entity="ticket",
                entity_id=ticket.id,
                status="success",
                details=f"Ticket {ticket.id}: {old_status} -> {ticket.status}"
            )
        
        if ticket.priority != old_priority:
            log_action(
                user=current_user,
                action="TICKET_PRIORITY_CHANGE",
                entity="ticket",
                entity_id=ticket.id,
                status="success",
                details=f"Ticket {ticket.id}: {old_priority} -> {ticket.priority}"
            )
        
        if ticket.assignee_id != old_assignee:
            log_action(
                user=current_user,
                action="TICKET_ASSIGNEE_CHANGE",
                entity="ticket",
                entity_id=ticket.id,
                status="success",
                details=f"Ticket {ticket.id}: {old_assignee if old_assignee else 'Sin asignar'} -> {ticket.assignee_id if ticket.assignee_id else 'Sin asignar'}"
            )
    else:
        print("\nNo se realizaron cambios.")


def delete_ticket(current_user: User) -> None:
    """
    Elimina un ticket del sistema.
    Solo los agentes pueden eliminar tickets, y solo si están cerrados.
    """
    print("\n--- Eliminar ticket ---")
    
    # Verificar que sea agente
    if current_user.role != "agent":
        print("No tienes permiso para eliminar tickets. Solo los agentes pueden hacerlo.")
        return
    
    ticket_id = input("ID del ticket a eliminar: ").strip()
    
    tickets = _load_tickets()
    ticket = _find_ticket_by_id(ticket_id, tickets)
    
    if not ticket:
        print(f"Error: No existe un ticket con ID {ticket_id}.")
        return
    
    # Verificar que el ticket esté cerrado
    if ticket.status != "closed":
        print(f"Error: Solo se pueden eliminar tickets cerrados. Este ticket tiene estado '{ticket.status}'.")
        return
    
    # Confirmar eliminación
    print(f"\n⚠ Vas a eliminar el ticket #{ticket.id}: {ticket.title}")
    confirm = input("¿Estás seguro? (s/n): ").strip().lower()
    
    if confirm != "s":
        print("Eliminación cancelada.")
        return
    
    # Eliminar el ticket
    tickets = [t for t in tickets if t.id != ticket_id]
    _save_tickets(tickets)
    
    print(f"\n✓ Ticket #{ticket_id} eliminado exitosamente.")
    
    # Registrar en logs
    log_action(
        user=current_user,
        action="TICKET_DELETE",
        entity="ticket",
        entity_id=ticket_id,
        status="success",
        details="Ticket eliminado"
    )
