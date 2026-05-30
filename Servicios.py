import hashlib
import secrets
import smtplib
import os
import ssl
import pyodbc
from email.message import EmailMessage
from datetime import datetime, timedelta




###
#CONFIG 
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



# ==========================================================
# ACCESO A DATOS
# ==========================================================


def obtener_conexion():
    return pyodbc.connect(CONNECTION_STRING)


def hash_clave(clave, salt):
    return hashlib.sha256(salt + clave.encode("utf-8")).digest()


def buscar_usuario_por_email(email):
    sql = """
    SELECT id_usuario, email, clave_hash, clave_salt, nombre, celular, activo
    FROM dbo.Usuario
    WHERE email = ?
    """
    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, email)
        return cursor.fetchone()


def validar_credenciales(email, clave):
    usuario = buscar_usuario_por_email(email)

    if usuario is None:
        return None

    id_usuario, email_bd, clave_hash_bd, clave_salt, nombre, celular, activo = usuario

    if not activo:
        return None

    clave_hash_calculada = hash_clave(clave, bytes(clave_salt))

    if clave_hash_calculada == bytes(clave_hash_bd):
        return {
            "id_usuario": id_usuario,
            "email": email_bd,
            "nombre": nombre,
            "celular": celular
        }

    return None


def guardar_token(id_usuario, token, tipo, minutos=5):
    sql = """
    INSERT INTO dbo.Token2FA(id_usuario, token, tipo, fecha_expira, usado)
    VALUES (?, ?, ?, DATEADD(MINUTE, ?, SYSDATETIME()), 0)
    """
    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, id_usuario, token, tipo, minutos)
        cn.commit()


def validar_token(id_usuario, token, tipo):
    sql_buscar = """
    SELECT TOP 1 id_token
    FROM dbo.Token2FA
    WHERE id_usuario = ?
      AND token = ?
      AND tipo = ?
      AND usado = 0
      AND fecha_expira >= SYSDATETIME()
    ORDER BY fecha_creacion DESC
    """

    sql_usar = """
    UPDATE dbo.Token2FA
    SET usado = 1
    WHERE id_token = ?
    """

    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql_buscar, id_usuario, token, tipo)
        row = cursor.fetchone()

        if row is None:
            return False

        id_token = row[0]
        cursor.execute(sql_usar, id_token)
        cn.commit()
        return True


def actualizar_clave(id_usuario, nueva_clave):
    nuevo_salt = secrets.token_bytes(16)
    nuevo_hash = hash_clave(nueva_clave, nuevo_salt)

    sql = """
    UPDATE dbo.Usuario
    SET clave_hash = ?, clave_salt = ?
    WHERE id_usuario = ?
    """

    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, nuevo_hash, nuevo_salt, id_usuario)
        cn.commit()


# ==========================================================
# EMAIL
# ==========================================================

def generar_token():
    return str(secrets.randbelow(900000) + 100000)


def enviar_email(destinatario, asunto, cuerpo):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)

    if not smtp_server or not smtp_user or not smtp_password:
        print("\n=== MODO DEMO: EMAIL NO CONFIGURADO ===")
        print(f"Para: {destinatario}")
        print(f"Asunto: {asunto}")
        print(cuerpo)
        print("======================================\n")
        return

    mensaje = EmailMessage()
    mensaje["From"] = smtp_from
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

    contexto = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=contexto)
        server.login(smtp_user, smtp_password)
        server.send_message(mensaje)



