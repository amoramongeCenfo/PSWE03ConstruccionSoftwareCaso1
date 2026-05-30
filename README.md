# Login 2FA con Python Tkinter y MSSQL

## Archivos

- `schema.sql`: crea la base de datos, tablas y usuario demo.
- `app.py`: aplicación Tkinter.
- `guia_revision.md`: guía de revisión para estudiantes.

## Usuario demo

- Email: `demo@fvncr.org`
- Clave: `demo`

## Instalación

```bash
pip install pyodbc
```

Debe tener instalado el driver ODBC de SQL Server.

## Ejecución

1. Ejecutar `schema.sql` en SQL Server Management Studio.
2. Ajustar en `app.py` el servidor SQL si no es `localhost`.
3. Ejecutar:

```bash
python app.py
```

## Email

Si no configura SMTP, el token se muestra en consola.

Para correo real, configurar variables de ambiente:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=correo@gmail.com
SMTP_PASSWORD=clave_de_aplicacion
SMTP_FROM=correo@gmail.com
```
