"""
Aplicación principal del sistema HelpDesk CLI.
Punto de entrada del programa - Fases 1, 2 y 3: Gestión de usuarios, tickets y seguridad.
"""
from core.auth import register_user, login_user
from core.logger import log_action
from core.validation import input_int_in_range, input_password, safe_input
from core.tickets import (
    create_ticket,
    list_tickets,
    view_ticket_detail,
    update_ticket,
    delete_ticket,
)
from core.safety_demo import run_safety_demo


def main_menu_not_logged():
    """
    Muestra el menú principal cuando no hay sesión activa.
    """
    print("\n" + "=" * 50)
    print("=== HelpDesk CLI - No autenticado ===")
    print("=" * 50)
    print("1) Registrarse")
    print("2) Iniciar sesión")
    print("0) Salir")
    print("=" * 50)


def main_menu_logged(current_user):
    """
    Muestra el menú principal cuando hay un usuario logueado.
    """
    print("\n" + "=" * 50)
    print(f"=== HelpDesk CLI - Usuario: {current_user.username} ({current_user.role}) ===")
    print("=" * 50)
    print("1) Crear ticket")
    print("2) Ver lista de tickets")
    print("3) Ver detalle de un ticket")
    print("4) Editar un ticket")
    print("5) Eliminar ticket (solo agentes)")
    print("6) Demostración de seguridad (overflow / underflow)")
    print("7) Cerrar sesión")
    print("0) Salir")
    print("=" * 50)


def main():
    """
    Función principal que controla el flujo del programa.
    """
    current_user = None
    
    try:
        print("\n¡Bienvenido al sistema HelpDesk CLI!")
        
        while True:
            # Mostrar menú según el estado de la sesión
            if current_user is None:
                # Usuario no autenticado
                main_menu_not_logged()
                option = input_int_in_range("Elige una opción: ", 0, 2)
                
                if option == 0:
                    # Salir del programa
                    print("\n¡Hasta luego!")
                    break
                
                elif option == 1:
                    # Flujo de registro
                    print("\n--- Registro de nuevo usuario ---")
                    username = safe_input("Nombre de usuario: ", field_type="username")
                    password = input_password("Contraseña: ").strip()
                    print("Roles disponibles: user, agent")
                    role = safe_input("Rol: ", field_type="choice")
                    
                    # Intentar registrar al usuario
                    user = register_user(username, password, role)
                    
                    if user:
                        print(f"\n✓ Usuario '{user.username}' registrado exitosamente con rol '{user.role}'.")
                        # Registrar en el log de auditoría
                        log_action(
                            user=None,
                            action="REGISTER",
                            entity="user",
                            entity_id=user.id,
                            status="success",
                            details=f"Nuevo usuario {user.username} con rol {user.role}"
                        )
                    # Si falla, register_user ya imprime el mensaje de error
                
                elif option == 2:
                    # Flujo de inicio de sesión
                    print("\n--- Inicio de sesión ---")
                    username = safe_input("Nombre de usuario: ", field_type="username")
                    password = input_password("Contraseña: ").strip()
                    
                    # Intentar iniciar sesión
                    user = login_user(username, password)
                    
                    if user:
                        current_user = user
                        print(f"\n✓ Inicio de sesión exitoso. Bienvenido, {current_user.username}!")
                        # Registrar login exitoso
                        log_action(
                            user=current_user,
                            action="LOGIN",
                            entity="user",
                            entity_id=current_user.id,
                            status="success",
                            details="Inicio de sesión correcto"
                        )
                    else:
                        print("\n✗ Credenciales inválidas.")
                        # Registrar intento fallido
                        log_action(
                            user=None,
                            action="LOGIN_FAILED",
                            entity="user",
                            entity_id="N/A",
                            status="failed",
                            details=f"Intento de login fallido para username={username}"
                        )
            
            else:
                # Usuario autenticado
                main_menu_logged(current_user)
                option = input_int_in_range("Elige una opción: ", 0, 7)
                
                if option == 0:
                    # Salir del programa
                    print("\n¡Hasta luego!")
                    break
                
                elif option == 1:
                    # Crear ticket
                    create_ticket(current_user)
                
                elif option == 2:
                    # Ver lista de tickets
                    list_tickets(current_user)
                
                elif option == 3:
                    # Ver detalle de un ticket
                    view_ticket_detail(current_user)
                
                elif option == 4:
                    # Editar un ticket
                    update_ticket(current_user)
                
                elif option == 5:
                    # Eliminar ticket
                    delete_ticket(current_user)
                
                elif option == 6:
                    # Demostración de seguridad (Fase 3)
                    run_safety_demo(current_user)
                
                elif option == 7:
                    # Cerrar sesión
                    print(f"\n✓ Sesión cerrada para {current_user.username}.")
                    # Registrar cierre de sesión
                    log_action(
                        user=current_user,
                        action="LOGOUT",
                        entity="user",
                        entity_id=current_user.id,
                        status="success",
                        details="Cierre de sesión"
                    )
                    current_user = None
    
    except KeyboardInterrupt:
        # Manejar Ctrl+C de forma amigable
        print("\n\nPrograma interrumpido por el usuario. ¡Hasta luego!")
    
    except Exception as e:
        # Capturar cualquier error inesperado sin mostrar detalles técnicos
        print("\nOcurrió un error inesperado. Intenta de nuevo.")


if __name__ == "__main__":
    main()
