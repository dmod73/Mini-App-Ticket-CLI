# Mini-App Segura: Help Desk CLI

## 👤 Autor

**Dean M. Ortiz Díaz**  
📧 ortizdiazdeanm@gmail.com

---

## 📋 Descripción del Proyecto

**Mini-App Segura: Help Desk CLI** es una aplicación de línea de comandos diseñada para gestionar tickets de soporte técnico con enfoque en seguridad. El sistema incluye autenticación básica con hashing SHA-256, control de acceso basado en roles (RBAC), persistencia en archivos locales y un completo sistema de auditoría.

El proyecto fue desarrollado como demostración de buenas prácticas de seguridad en aplicaciones Python, incluyendo validación de entradas, sanitización de datos, prevención de errores lógicos y manejo seguro de información sensible.

---

## 🚀 Requisitos e Instalación

### Requisitos

- **Python 3.8 o superior**
- Solo se utiliza la librería estándar de Python (no requiere dependencias externas)

### Ejecución del Proyecto

```bash
cd helpdesk_cli
python app.py
```

---

## 📁 Estructura del Proyecto

```
helpdesk_cli/
├── app.py                      # Punto de entrada principal
├── core/                       # Módulos del núcleo del sistema
│   ├── __init__.py
│   ├── auth.py                 # Autenticación y gestión de usuarios
│   ├── security.py             # Hashing de contraseñas (SHA-256)
│   ├── storage.py              # Persistencia en archivos JSON
│   ├── logger.py               # Sistema de auditoría
│   ├── validation.py           # Validación y sanitización de entradas
│   ├── tickets.py              # Gestión de tickets (CRUD)
│   └── safety_demo.py          # Demostraciones de seguridad
├── models/                     # Modelos de datos
│   ├── __init__.py
│   ├── user.py                 # Modelo de usuario
│   └── ticket.py               # Modelo de ticket
├── data/                       # Archivos de datos (JSON por línea)
│   ├── users.txt               # Usuarios registrados
│   └── tickets.txt             # Tickets del sistema
└── logs/                       # Registros de auditoría
    └── audit.log               # Log de todas las acciones
```

---

## ✨ Funcionalidades Implementadas

### **Fase 1: Gestión de Usuarios**

- ✅ Registro de usuarios con validación estricta
- ✅ Inicio de sesión con credenciales
- ✅ Hashing seguro de contraseñas usando SHA-256
- ✅ Roles: `user` (usuario regular) y `agent` (agente de soporte)
- ✅ Persistencia en archivos de texto (JSON por línea)

### **Fase 2: Gestión de Tickets**

- ✅ **CRUD completo de tickets:**
  - Crear tickets con título, descripción y prioridad
  - Listar tickets (filtrado por rol)
  - Ver detalles de un ticket específico
  - Editar tickets (título, descripción, prioridad, estado)
  - Eliminar tickets (solo agentes, solo cerrados)
- ✅ **Control de acceso por rol:**
  - `user`: Puede crear y gestionar solo sus propios tickets
  - `agent`: Puede ver y gestionar todos los tickets
- ✅ **Sistema de estados con validación de transiciones:**
  - `open` → `in_progress` o `closed`
  - `in_progress` → `closed`
  - `closed` → sin retroceso (inmutable)
- ✅ **Prioridades:** `low`, `medium`, `high`
- ✅ **Asignación de tickets a agentes**

### **Fase 3: Seguridad y Demostraciones**

- ✅ Sanitización de campos de texto
- ✅ Demostración de prevención de índice fuera de rango
- ✅ Demostración de overflow lógico (límite de tickets)
- ✅ Demostración de inmunidad a SQL Injection
- ✅ Validación exhaustiva de todas las entradas

### **Auditoría y Logging**

- ✅ Registro de todas las acciones importantes:
  - Login/Logout
  - Registro de usuarios
  - Creación, modificación y eliminación de tickets
  - Cambios de estado, prioridad y asignación
  - Ejecución de demostraciones de seguridad
- ✅ Formato JSON estructurado con timestamps UTC
- ✅ No se registran contraseñas ni datos sensibles

---

## 🔒 Características de Seguridad

### **1. Validación de Entradas**

- Username: Solo letras, números, puntos y guiones bajos (3-30 caracteres)
- Contraseñas: Longitud mínima de 6 caracteres
- Roles: Lista blanca (`user`, `agent`)
- Estados: Lista blanca con transiciones válidas
- Prioridades: Lista blanca (`low`, `medium`, `high`)

### **2. Sanitización de Texto**

- Eliminación de saltos de línea en campos de texto
- Limitación de longitud máxima (prevención de overflow)
- Los textos se guardan como texto plano en JSON (sin ejecución de código)

### **3. Principio de Menor Privilegio**

- Control de acceso basado en roles (RBAC)
- Usuarios solo acceden a sus propios recursos
- Agentes tienen permisos elevados pero limitados

### **4. Hashing Seguro**

- Contraseñas hasheadas con SHA-256
- Nunca se almacenan contraseñas en texto plano
- Verificación mediante comparación de hashes

### **5. Manejo de Errores**

- Mensajes de error informativos sin exponer detalles técnicos
- No se muestran stack traces al usuario final
- Captura de excepciones con manejo adecuado

### **6. Prevención de Errores Lógicos**

- Validación de rangos antes de acceder a índices
- Límites de negocio definidos y validados
- Prevención de transiciones de estado inválidas

### **7. Inmunidad a SQL Injection**

- No se utiliza SQL ni bases de datos
- Persistencia en archivos JSON (texto plano)
- Textos maliciosos se guardan como contenido, no se ejecutan

---

## 🎯 Ejemplo de Flujo de Uso

### **Escenario 1: Usuario Regular**

```
1. Registrarse como usuario con rol "user"
2. Iniciar sesión
3. Crear un ticket con descripción del problema
4. Ver lista de tickets propios
5. Editar ticket (cambiar estado de "open" a "in_progress")
6. Ver detalle del ticket actualizado
7. Cerrar sesión
```

### **Escenario 2: Agente de Soporte**

```
1. Registrarse como agente con rol "agent"
2. Iniciar sesión
3. Ver lista de todos los tickets del sistema
4. Asignar un ticket a sí mismo
5. Cambiar estado del ticket a "in_progress"
6. Resolver el problema y cambiar estado a "closed"
7. Eliminar el ticket cerrado
8. Cerrar sesión
```

### **Escenario 3: Demostración de Seguridad**

```
1. Iniciar sesión con cualquier usuario
2. Seleccionar opción "Demostración de seguridad"
3. Ejecutar demo de índice fuera de rango
4. Ejecutar demo de overflow lógico
5. Ejecutar demo de prevención de SQL Injection
6. Revisar logs de auditoría generados
```

---

## 📊 Formato de Log de Auditoría

Cada acción genera una entrada en `logs/audit.log` con el siguiente formato JSON:

```json
{
  "timestamp": "2025-11-26T15:30:45.123456Z",
  "user_id": "1",
  "username": "Dean",
  "role": "user",
  "action": "TICKET_CREATE",
  "entity": "ticket",
  "entity_id": "1",
  "status": "success",
  "details": "Título: Fallo en API, Prioridad: high"
}
```

### **Tipos de Acciones Registradas:**

- `REGISTER` - Registro de nuevo usuario
- `LOGIN` - Inicio de sesión exitoso
- `LOGIN_FAILED` - Intento de login fallido
- `LOGOUT` - Cierre de sesión
- `TICKET_CREATE` - Creación de ticket
- `TICKET_STATUS_CHANGE` - Cambio de estado
- `TICKET_PRIORITY_CHANGE` - Cambio de prioridad
- `TICKET_ASSIGNEE_CHANGE` - Reasignación de ticket
- `TICKET_DELETE` - Eliminación de ticket
- `SECURITY_DEMO` - Ejecución de demo de seguridad

---

## 🧪 Pruebas y Validación

Para validar el correcto funcionamiento del sistema:

1. **Crear usuarios con diferentes roles**
2. **Intentar acciones no permitidas** (verificar control de acceso)
3. **Intentar transiciones de estado inválidas** (verificar validación)
4. **Ejecutar demos de seguridad** (verificar prevención de errores)
5. **Revisar logs de auditoría** (verificar trazabilidad)
6. **Intentar crear tickets con textos "peligrosos"** (verificar sanitización)

---

## 📝 Notas Técnicas

- **Persistencia:** Formato JSON por línea permite lectura incremental y recuperación ante errores
- **Seguridad:** SHA-256 es suficiente para fines demostrativos (en producción se recomendaría bcrypt o Argon2)
- **Portabilidad:** Compatible con Windows, Linux y macOS
- **Simplicidad:** Solo usa librería estándar de Python para facilitar comprensión y despliegue

---

## 🎓 Propósito Académico

Este proyecto fue desarrollado con fines educativos para demostrar:

- Implementación de autenticación básica segura
- Control de acceso basado en roles (RBAC)
- Validación y sanitización de entradas
- Prevención de errores lógicos comunes
- Buenas prácticas de logging y auditoría
- Diseño de aplicaciones seguras sin frameworks

---

## 📞 Contacto

Para consultas o comentarios sobre el proyecto:

**Dean M. Ortiz Díaz**  
📧 ortizdiazdeanm@gmail.com

---

**Proyecto desarrollado como parte del curso de Ciberseguridad - Universidad 2025-2026**
