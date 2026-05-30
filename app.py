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

import os
import re
import ssl



import UI
# ==========================================================
# CONFIGURACIÓN
# ==========================================================

DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "CMSoftwareDemo")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

# Si usa autenticación integrada de Windows:
CONNECTION_STRING = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

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


# ==========================================================
# VALIDACIONES
# ==========================================================

def email_valido(email):
    patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(patron, email) is not None


def clave_valida(clave):
    """
    Regla didáctica:
    - No vacía
    - Solo letras, números y el caracter especial #
    """
    if not clave:
        return False
    return re.match(r"^[A-Za-z0-9#]+$", clave) is not None


def validar_login_form(email, clave):
    if not email.strip():
        return False, "El email es obligatorio."
    if not clave.strip():
        return False, "La clave es obligatoria."
    if not email_valido(email):
        return False, "El formato del email no es válido."
    if not clave_valida(clave):
        return False, "La clave solo puede contener letras, números y el caracter especial #."
    return True, ""


if __name__ == "__main__":
    app = UI.App()
    app.mainloop()
