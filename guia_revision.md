# Guía de revisión para estudiantes

Curso: Construcción y Mantenimiento de Software  
Práctica: Login con recuperación de clave, 2FA por email y MSSQL

## 1. Objetivo

El estudiante debe revisar, ejecutar, mejorar y justificar un programa Python con Tkinter y SQL Server que implementa:

- Login contra base de datos.
- Validación de campos.
- Validación de formato de email.
- Restricción de caracteres en clave.
- Clave protegida en base de datos mediante hash + salt.
- Recuperación de clave vía email.
- Doble autenticación por token vía email.
- Pantalla de error.
- Menú principal.

## 2. Actividades esperadas

### Actividad 1. Construcción

El estudiante debe ejecutar el programa y validar que:

- La pantalla de login carga correctamente.
- El usuario demo puede autenticarse.
- El sistema genera token 2FA.
- El token permite ingresar al menú principal.
- La recuperación de clave genera un token.
- La nueva clave se guarda correctamente.
- La pantalla de error aparece ante entradas incorrectas.

### Actividad 2. Validación

Probar como mínimo los siguientes casos:

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Email vacío | email vacío | Error |
| Clave vacía | clave vacía | Error |
| Email inválido | abc | Error |
| Clave con carácter no permitido | demo* | Error |
| Usuario inexistente | noexiste@x.com | Error |
| Clave incorrecta | demo@fvncr.org / mala | Error |
| Login correcto | demo@fvncr.org / demo | Solicita token |
| Token incorrecto | 123456 | Error |
| Token correcto | token generado | Menú principal |
| Recuperación de clave | email válido | Envía token |
| Cambio de clave válido | token + nueva clave | Clave actualizada |

### Actividad 3. Mantenimiento

El estudiante debe proponer al menos 3 mejoras al programa.

Ejemplos:

- Separar el código en capas: UI, lógica, datos y servicios.
- Agregar bloqueo por intentos fallidos.
- Agregar expiración configurable de tokens.
- Registrar auditoría de login.
- Usar variables de entorno para toda configuración.
- Crear pruebas unitarias para validaciones.
- Agregar logging.
- Evitar mostrar detalles técnicos de errores al usuario final.

## 3. Guía de revisión basada en la clase anterior

### Métodos de construcción

Revisar si el programa muestra:

| Criterio | Evidencia esperada |
|---|---|
| Construcción incremental | Login, luego 2FA, luego recuperación, luego menú |
| Construcción basada en componentes | Funciones separadas para BD, validación, email y UI |
| Construcción dirigida por pruebas | Validaciones probables de probar |
| Construcción mantenible | Código legible y organizado |

### Planificación de la construcción

El estudiante debe identificar tareas como:

| Tarea | Producto |
|---|---|
| Crear DDL de base de datos | script SQL |
| Crear conexión MSSQL | función obtener_conexion |
| Crear validaciones | funciones email_valido y clave_valida |
| Crear login | pantalla y validación contra BD |
| Crear token 2FA | tabla Token2FA y funciones |
| Crear recuperación de clave | pantalla y actualización |
| Crear menú principal | pantalla final |
| Crear pruebas manuales | tabla de casos |

### Medición de la construcción

El estudiante debe reportar:

| Métrica | Resultado |
|---|---|
| Cantidad de pantallas |  |
| Cantidad de funciones |  |
| Cantidad de validaciones |  |
| Cantidad de tablas |  |
| Casos de prueba ejecutados |  |
| Casos exitosos |  |
| Casos fallidos |  |
| Defectos encontrados |  |
| Defectos corregidos |  |

## 4. Entregables

Cada grupo debe entregar:

1. Captura de la base de datos creada.
2. Captura del login.
3. Captura de token enviado o mostrado en consola.
4. Captura del menú principal.
5. Tabla de pruebas ejecutadas.
6. Lista de defectos encontrados.
7. Tres mejoras propuestas.
8. Breve reflexión sobre construcción y mantenimiento.
9.preguntas de reflexión (responder)
	1. ¿Qué parte del programa sería más difícil de mantener si creciera el sistema?
	2. ¿Qué riesgos existen si se guarda la clave en texto plano?
	3. ¿Por qué conviene separar la interfaz gráfica del acceso a datos?
	4. ¿Qué parte debería automatizarse con pruebas unitarias?
	5. ¿Qué cambiaría si este sistema fuera para producción real?
