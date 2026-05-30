import secrets
import smtplib
import os
import ssl
from email.message import EmailMessage

from datos import (
    hash_clave,
    buscar_usuario_por_email,
    guardar_token,
    validar_token,
    actualizar_clave as _actualizar_clave_db,
    incrementar_intentos,
    resetear_intentos,
    bloquear_usuario,
    desbloquear_usuario,
)

MAX_INTENTOS = 3


def validar_credenciales(email, clave):
    usuario = buscar_usuario_por_email(email)

    if usuario is None:
        return None, "Usuario o clave incorrectos."

    id_usuario, email_bd, clave_hash_bd, clave_salt, nombre, celular, activo, intentos_fallidos = usuario

    if not activo:
        return None, "La cuenta está bloqueada. Use recuperar clave para desbloquearla."

    if intentos_fallidos >= MAX_INTENTOS:
        bloquear_usuario(id_usuario)
        return None, "La cuenta está bloqueada. Use recuperar clave para desbloquearla."

    clave_hash_calculada = hash_clave(clave, bytes(clave_salt))

    if clave_hash_calculada != bytes(clave_hash_bd):
        incrementar_intentos(id_usuario)
        restantes = MAX_INTENTOS - (intentos_fallidos + 1)
        if restantes <= 0:
            bloquear_usuario(id_usuario)
            return None, "La cuenta ha sido bloqueada por exceder el máximo de intentos. Use recuperar clave para desbloquearla."
        return None, f"Usuario o clave incorrectos. Le quedan {restantes} intento(s)."

    resetear_intentos(id_usuario)
    return {
        "id_usuario": id_usuario,
        "email": email_bd,
        "nombre": nombre,
        "celular": celular
    }, None


def generar_token():
    return str(secrets.randbelow(900000) + 100000)


def actualizar_clave(id_usuario, nueva_clave):
    nuevo_salt = secrets.token_bytes(16)
    nuevo_hash = hash_clave(nueva_clave, nuevo_salt)
    _actualizar_clave_db(id_usuario, nuevo_hash, nuevo_salt)
    resetear_intentos(id_usuario)
    desbloquear_usuario(id_usuario)


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
