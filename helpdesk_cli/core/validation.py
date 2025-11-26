"""
Módulo para validar las entradas del usuario.
Asegura que los datos sean correctos antes de procesarlos.
"""
import re


def is_valid_username(username: str) -> bool:
    """
    Valida que el nombre de usuario cumpla los requisitos:
    - No vacío
    - Entre 3 y 30 caracteres
    - Solo letras, números, puntos y guiones bajos
    """
    if not username or len(username) < 3 or len(username) > 30:
        return False
    
    # Solo permitir letras, números, punto y guion bajo
    if not re.match(r'^[a-zA-Z0-9._]+$', username):
        return False
    
    return True


def is_valid_password(password: str) -> bool:
    """
    Valida que la contraseña tenga entre 6 y 64 caracteres.
    """
    return 6 <= len(password) <= 64


def is_valid_role(role: str) -> bool:
    """
    Valida que el rol sea uno de los permitidos: user o agent.
    """
    return role in ["user", "agent"]


def input_int_in_range(prompt: str, min_value: int, max_value: int) -> int:
    """
    Pide al usuario un número entero que esté dentro de un rango.
    Si el usuario ingresa algo incorrecto, vuelve a preguntar.
    """
    while True:
        try:
            value = input(prompt).strip()
            num = int(value)
            
            # Verificar que esté en el rango
            if min_value <= num <= max_value:
                return num
            else:
                print(f"El número debe estar entre {min_value} y {max_value}.")
        except ValueError:
            print("Por favor ingresa un número válido.")


def sanitize_text_field(text: str, max_length: int = 300) -> str:
    """
    Limpia y normaliza un campo de texto para evitar entradas mal formadas.
    Ayuda a prevenir textos demasiado largos y saltos de línea en archivos JSON.
    Aunque el usuario escriba cosas como "' OR 1=1 --", solo se guarda como texto
    normal porque no construimos consultas SQL ni ejecutamos comandos.
    """
    # Eliminar espacios al inicio y final
    text = text.strip()
    
    # Reemplazar saltos de línea por espacios para mantener el formato JSON
    text = text.replace("\n", " ").replace("\r", " ")
    
    # Limitar la longitud máxima
    if len(text) > max_length:
        text = text[:max_length]
    
    return text
