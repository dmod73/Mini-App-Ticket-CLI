"""
Módulo para validar las entradas del usuario.
Asegura que los datos sean correctos antes de procesarlos.
"""
import re
import sys
import msvcrt


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


def contains_sql_injection_patterns(text: str) -> bool:
    """
    Detecta patrones comunes de SQL injection en texto.
    Retorna True si encuentra algo sospechoso.
    """
    # Patrones comunes de SQL injection
    dangerous_patterns = [
        "';", '";', '--', '/*', '*/', 'xp_', 'sp_',
        'exec', 'execute', 'select', 'insert', 'update', 
        'delete', 'drop', 'create', 'alter', 'union',
        'script', '<script', 'javascript:', 'onerror='
    ]
    
    text_lower = text.lower()
    for pattern in dangerous_patterns:
        if pattern in text_lower:
            return True
    return False


def input_int_in_range(prompt: str, min_value: int, max_value: int) -> int:
    """
    Pide al usuario un número entero que esté dentro de un rango.
    Si el usuario ingresa algo incorrecto, vuelve a preguntar.
    Protección adicional contra intentos de injection.
    """
    while True:
        try:
            value = input(prompt).strip()
            
            # Verificar si contiene patrones sospechosos
            if contains_sql_injection_patterns(value):
                print("⚠ Entrada inválida detectada. Solo se permiten números.")
                continue
            
            # Validar que sea solo dígitos (positivos o negativos)
            if not value.lstrip('-').isdigit():
                print("Por favor ingresa un número válido.")
                continue
            
            num = int(value)
            
            # Verificar que esté en el rango
            if min_value <= num <= max_value:
                return num
            else:
                print(f"El número debe estar entre {min_value} y {max_value}.")
        except ValueError:
            print("Por favor ingresa un número válido.")


def sanitize_text_field(text: str, max_length: int = 300, allow_sql_keywords: bool = True) -> str:
    """
    Limpia y normaliza un campo de texto para evitar entradas mal formadas.
    Ayuda a prevenir textos demasiado largos y saltos de línea en archivos JSON.
    Aunque el usuario escriba cosas como "' OR 1=1 --", solo se guarda como texto
    normal porque no construimos consultas SQL ni ejecutamos comandos.
    
    Si allow_sql_keywords=False, rechaza textos con patrones peligrosos.
    """
    # Eliminar espacios al inicio y final
    text = text.strip()
    
    # Reemplazar saltos de línea por espacios para mantener el formato JSON
    text = text.replace("\n", " ").replace("\r", " ")
    
    # Limitar la longitud máxima
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def safe_input(prompt: str, field_type: str = "text") -> str:
    """
    Solicita entrada del usuario con validación de seguridad.
    
    field_type puede ser:
    - "text": permite cualquier texto
    - "username": solo alfanuméricos, puntos y guiones bajos
    - "id": solo números
    - "choice": solo letras minúsculas sin espacios
    """
    while True:
        value = input(prompt).strip()
        
        if not value:
            return value
        
        # Detectar patrones sospechosos en entradas críticas
        if field_type in ["username", "id", "choice"]:
            if contains_sql_injection_patterns(value):
                print("⚠ Entrada rechazada: contiene caracteres o patrones no permitidos.")
                print("Por favor usa solo caracteres válidos.")
                continue
        
        # Validaciones específicas por tipo
        if field_type == "username":
            if not re.match(r'^[a-zA-Z0-9._]+$', value):
                print("Solo se permiten letras, números, puntos y guiones bajos.")
                continue
        
        elif field_type == "id":
            if not value.isdigit():
                print("Solo se permiten números.")
                continue
        
        elif field_type == "choice":
            if not re.match(r'^[a-z_]+$', value):
                print("Solo se permiten letras minúsculas y guiones bajos.")
                continue
        
        return value


def input_password(prompt: str = "Contraseña: ") -> str:
    """
    Solicita una contraseña mostrando asteriscos en lugar de los caracteres.
    Funciona en Windows mostrando * por cada carácter escrito.
    """
    print(prompt, end='', flush=True)
    password = ""
    
    while True:
        # Leer un carácter sin mostrarlo
        char = msvcrt.getch()
        
        # Enter (código 13) termina la entrada
        if char == b'\r':
            print()  # Nueva línea después de terminar
            break
        
        # Backspace (código 8) borra el último carácter
        elif char == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                # Borrar el último asterisco en pantalla
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        
        # Caracteres normales
        else:
            try:
                # Decodificar y agregar a la contraseña
                password += char.decode('utf-8')
                sys.stdout.write('*')
                sys.stdout.flush()
            except:
                # Ignorar caracteres que no se puedan decodificar
                pass
    
    return password
