import hashlib
import os
import pyodbc


DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "CMSoftwareDemo")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

CONNECTION_STRING = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


def obtener_conexion():
    return pyodbc.connect(CONNECTION_STRING)


def hash_clave(clave, salt):
    return hashlib.sha256(salt + clave.encode("utf-8")).digest()


def buscar_usuario_por_email(email):
    sql = """
    SELECT id_usuario, email, clave_hash, clave_salt, nombre, celular, activo, intentos_fallidos
    FROM dbo.Usuario
    WHERE email = ?
    """
    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, email)
        return cursor.fetchone()


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


def incrementar_intentos(id_usuario):
    sql = "UPDATE dbo.Usuario SET intentos_fallidos = intentos_fallidos + 1 WHERE id_usuario = ?"
    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, id_usuario)
        cn.commit()


def resetear_intentos(id_usuario):
    sql = "UPDATE dbo.Usuario SET intentos_fallidos = 0 WHERE id_usuario = ?"
    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, id_usuario)
        cn.commit()


def bloquear_usuario(id_usuario):
    sql = "UPDATE dbo.Usuario SET activo = 0 WHERE id_usuario = ?"
    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, id_usuario)
        cn.commit()


def desbloquear_usuario(id_usuario):
    sql = "UPDATE dbo.Usuario SET activo = 1 WHERE id_usuario = ?"
    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, id_usuario)
        cn.commit()


def actualizar_clave(id_usuario, nuevo_hash, nuevo_salt):
    sql = """
    UPDATE dbo.Usuario
    SET clave_hash = ?, clave_salt = ?
    WHERE id_usuario = ?
    """
    with obtener_conexion() as cn:
        cursor = cn.cursor()
        cursor.execute(sql, nuevo_hash, nuevo_salt, id_usuario)
        cn.commit()
