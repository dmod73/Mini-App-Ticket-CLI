"""
Módulo de demostración de seguridad.
Muestra cómo se previenen errores de overflow/underflow lógico
y otros problemas comunes mediante validaciones.
"""
from typing import List
from .validation import input_int_in_range
from .logger import log_action

# Límite máximo de tickets permitidos en el sistema (ejemplo de límite de negocio)
MAX_TICKETS_ALLOWED = 100000


def demo_index_out_of_range() -> None:
    """
    Demuestra cómo se evitan errores de índice fuera de rango.
    Sin validación adecuada, acceder a una posición inválida
    causaría un IndexError y rompería el programa.
    """
    print("\n--- Demostración: Índice fuera de rango ---")
    print("Tenemos una lista de números: [10, 20, 30]")
    
    numeros = [10, 20, 30]
    
    print(f"Índices válidos: 0 a {len(numeros) - 1}")
    
    # Usar validación para asegurar que el índice esté en rango
    indice = input_int_in_range(
        "Elige un índice para ver el valor: ",
        0,
        len(numeros) - 1
    )
    
    # Como validamos el rango, podemos acceder de forma segura
    print(f"✓ Valor en posición {indice}: {numeros[indice]}")
    print("\nNota: Si no validáramos el rango, un índice como 5 o -10")
    print("causaría un IndexError y el programa se rompería.")


def demo_ticket_limit() -> None:
    """
    Demuestra cómo se previene el overflow lógico de negocio.
    Aunque Python maneja enteros grandes sin problema técnico,
    a nivel de negocio podemos definir límites razonables.
    """
    print("\n--- Demostración: Límite máximo de tickets ---")
    print(f"El sistema tiene un límite de {MAX_TICKETS_ALLOWED:,} tickets.")
    print("Esto evita que alguien abuse del sistema creando millones de registros.")
    
    # Pedir cantidad actual de tickets
    while True:
        cantidad_actual_str = input("\n¿Cuántos tickets hay actualmente? ").strip()
        if cantidad_actual_str.isdigit():
            cantidad_actual = int(cantidad_actual_str)
            if cantidad_actual >= 0:
                break
        print("Por favor ingresa un número entero positivo.")
    
    # Pedir cuántos tickets nuevos se quieren crear
    while True:
        nuevos_tickets_str = input("¿Cuántos tickets nuevos quieres crear? ").strip()
        if nuevos_tickets_str.isdigit():
            nuevos_tickets = int(nuevos_tickets_str)
            if nuevos_tickets >= 0:
                break
        print("Por favor ingresa un número entero positivo.")
    
    # Calcular el total
    suma = cantidad_actual + nuevos_tickets
    
    print(f"\nCálculo: {cantidad_actual:,} + {nuevos_tickets:,} = {suma:,}")
    
    # Validar contra el límite de negocio
    if suma > MAX_TICKETS_ALLOWED:
        print(f"✗ ERROR: La suma supera el límite permitido de {MAX_TICKETS_ALLOWED:,} tickets.")
        print("Operación cancelada para prevenir overflow lógico.")
    else:
        print(f"✓ Operación aceptada. Total de tickets: {suma:,}")
        print("El límite no se ha superado.")
    
    print("\nNota: Aunque Python permite números más grandes, validamos")
    print("el límite de negocio ANTES de procesar para evitar abusos.")


def demo_sql_injection_prevention() -> None:
    """
    Demuestra que el sistema es seguro contra intentos de SQL injection.
    Como no usamos SQL, cualquier texto peligroso se guarda como texto normal.
    """
    print("\n--- Demostración: Prevención de SQL Injection ---")
    print("Este sistema NO usa bases de datos SQL, solo archivos JSON.")
    print("Por eso, textos como \"' OR 1=1 --\" se guardan como texto normal")
    print("y no pueden alterar la lógica del programa.\n")
    
    print("Intenta escribir algo \"peligroso\" (o presiona Enter para ejemplo):")
    texto_peligroso = input("Texto: ").strip()
    
    if not texto_peligroso:
        texto_peligroso = "'; DROP TABLE users; --"
    
    print(f"\n✓ Texto recibido: \"{texto_peligroso}\"")
    print("✓ Se guardará como texto plano en el archivo JSON.")
    print("✓ Nunca se ejecuta como código ni altera consultas.")
    print("\nAdemás, los campos críticos (username, rol, priority, status)")
    print("tienen validaciones estrictas que rechazan valores no permitidos.")


def run_safety_demo(current_user) -> None:
    """
    Menú principal de demostraciones de seguridad.
    Permite al usuario ver ejemplos de cómo se previenen errores comunes.
    """
    while True:
        print("\n" + "=" * 60)
        print("=== Demostración de Seguridad ===")
        print("=" * 60)
        print("1) Ejemplo de índice fuera de rango (prevención de crashes)")
        print("2) Ejemplo de límite máximo de tickets (overflow lógico)")
        print("3) Prevención de SQL Injection")
        print("0) Volver al menú anterior")
        print("=" * 60)
        
        option = input_int_in_range("Elige una opción: ", 0, 3)
        
        if option == 0:
            break
        elif option == 1:
            demo_index_out_of_range()
        elif option == 2:
            demo_ticket_limit()
        elif option == 3:
            demo_sql_injection_prevention()
        
        # Registrar en logs que se ejecutó una demo
        if option > 0:
            log_action(
                user=current_user,
                action="SECURITY_DEMO",
                entity="demo",
                entity_id=f"demo_{option}",
                status="success",
                details=f"Usuario ejecutó demostración de seguridad opción {option}"
            )
