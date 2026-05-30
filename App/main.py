"""
Programa didáctico:
Login con MSSQL + recuperación de clave por email + doble autenticación por email.

Curso: Construcción y Mantenimiento de Software

Requisitos:
    pip install pyodbc

Para enviar correos reales:
    Configurar variables de ambiente:
        SMTP_SERVER
        SMTP_PORT
        SMTP_USER
        SMTP_PASSWORD
        SMTP_FROM

Ejemplo en Windows PowerShell:
    setx SMTP_SERVER "smtp.gmail.com"
    setx SMTP_PORT "587"
    setx SMTP_USER "su_correo@gmail.com"
    setx SMTP_PASSWORD "clave_de_aplicacion"
    setx SMTP_FROM "su_correo@gmail.com"

Si no configura SMTP, el programa mostrará el token en consola.
"""

import ui

# Si prefiere usuario SQL Server, comente el CONNECTION_STRING anterior y use esto:
# DB_USER = os.getenv("DB_USER", "sa")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "SuClave")
# CONNECTION_STRING = (
#     f"DRIVER={{{DB_DRIVER}}};"
#     f"SERVER={DB_SERVER};"
#     f"DATABASE={DB_NAME};"
#     f"UID={DB_USER};"
#     f"PWD={DB_PASSWORD};"
#     "TrustServerCertificate=yes;"
# )




if __name__ == "__main__":
    App = ui.App()
    App.mainloop()
