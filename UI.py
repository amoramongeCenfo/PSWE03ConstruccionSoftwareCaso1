
import tkinter as tk
from tkinter import messagebox
import app
from app import (
    validar_login_form,
    validar_credenciales,
    generar_token,
    guardar_token,
    enviar_email,
    validar_token,
    email_valido,
    buscar_usuario_por_email,
    clave_valida,
    actualizar_clave
)

# ==========================================================
# INTERFAZ TKINTER
# ==========================================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema Demo - Login 2FA")
        self.geometry("500x350")
        self.resizable(False, False)

        self.usuario_actual = None

        self.mostrar_login()

    def limpiar(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_error(self, mensaje):
        self.limpiar()

        tk.Label(self, text="Pantalla de error", font=("Arial", 18, "bold")).pack(pady=25)
        tk.Label(self, text=mensaje, fg="red", wraplength=420).pack(pady=10)

        tk.Button(self, text="Volver al login", command=self.mostrar_login, width=20).pack(pady=20)

    def mostrar_login(self):
        self.limpiar()

        tk.Label(self, text="Inicio de sesión", font=("Arial", 18, "bold")).pack(pady=20)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Email:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_email = tk.Entry(frame, width=35)
        entry_email.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Clave:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_clave = tk.Entry(frame, width=35, show="*")
        entry_clave.grid(row=1, column=1, pady=5)

        def login():
            email = entry_email.get().strip()
            clave = entry_clave.get().strip()

            valido, mensaje = validar_login_form(email, clave)
            if not valido:
                self.mostrar_error(mensaje)
                return

            try:
                usuario = validar_credenciales(email, clave)
            except Exception as ex:
                self.mostrar_error(f"Error conectando con la base de datos: {ex}")
                return

            if usuario is None:
                self.mostrar_error("Usuario o clave incorrectos.")
                return

            token = app.generar_token()
            guardar_token(usuario["id_usuario"], token, "LOGIN_2FA", minutos=5)

            enviar_email(
                usuario["email"],
                "Token de doble autenticación",
                f"Hola {usuario['nombre']}, su token de acceso es: {token}. Expira en 5 minutos."
            )

            self.usuario_actual = usuario
            self.mostrar_2fa()

        tk.Button(self, text="Ingresar", command=login, width=20).pack(pady=10)
        tk.Button(self, text="Recuperar clave", command=self.mostrar_recuperar_clave, width=20).pack()

    def mostrar_2fa(self):
        self.limpiar()

        tk.Label(self, text="Doble autenticación", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self, text="Digite el token enviado por email.").pack(pady=5)

        entry_token = tk.Entry(self, width=20)
        entry_token.pack(pady=10)

        def verificar():
            token = entry_token.get().strip()

            if not token:
                self.mostrar_error("Debe digitar el token.")
                return

            if validar_token(self.usuario_actual["id_usuario"], token, "LOGIN_2FA"):
                self.mostrar_menu()
            else:
                self.mostrar_error("Token inválido, expirado o ya utilizado.")

        tk.Button(self, text="Verificar token", command=verificar, width=20).pack(pady=10)
        tk.Button(self, text="Cancelar", command=self.mostrar_login, width=20).pack()

    def mostrar_recuperar_clave(self):
        self.limpiar()

        tk.Label(self, text="Recuperación de clave", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self, text="Digite su email registrado.").pack(pady=5)

        entry_email = tk.Entry(self, width=35)
        entry_email.pack(pady=10)

        def enviar_token_recuperacion():
            email = entry_email.get().strip()

            if not email:
                self.mostrar_error("El email es obligatorio.")
                return

            if not email_valido(email):
                self.mostrar_error("El formato del email no es válido.")
                return

            usuario = buscar_usuario_por_email(email)

            if usuario is None:
                self.mostrar_error("No existe un usuario con ese email.")
                return

            id_usuario = usuario[0]
            nombre = usuario[4]

            token = generar_token()
            guardar_token(id_usuario, token, "RECUPERACION", minutos=5)

            enviar_email(
                email,
                "Token de recuperación de clave",
                f"Hola {nombre}, su token de recuperación es: {token}. Expira en 5 minutos."
            )

            self.mostrar_cambiar_clave(id_usuario)

        tk.Button(self, text="Enviar token", command=enviar_token_recuperacion, width=20).pack(pady=10)
        tk.Button(self, text="Volver", command=self.mostrar_login, width=20).pack()

    def mostrar_cambiar_clave(self, id_usuario):
        self.limpiar()

        tk.Label(self, text="Cambiar clave", font=("Arial", 18, "bold")).pack(pady=20)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Token:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_token = tk.Entry(frame, width=30)
        entry_token.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Nueva clave:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        entry_clave = tk.Entry(frame, width=30, show="*")
        entry_clave.grid(row=1, column=1, pady=5)

        def cambiar():
            token = entry_token.get().strip()
            nueva_clave = entry_clave.get().strip()

            if not token:
                self.mostrar_error("Debe digitar el token.")
                return

            if not nueva_clave:
                self.mostrar_error("Debe digitar la nueva clave.")
                return

            if not clave_valida(nueva_clave):
                self.mostrar_error("La clave solo puede contener letras, números y el caracter especial #.")
                return

            if not validar_token(id_usuario, token, "RECUPERACION"):
                self.mostrar_error("Token inválido, expirado o ya utilizado.")
                return

            actualizar_clave(id_usuario, nueva_clave)
            messagebox.showinfo("Clave actualizada", "La clave fue actualizada correctamente.")
            self.mostrar_login()

        tk.Button(self, text="Cambiar clave", command=cambiar, width=20).pack(pady=10)
        tk.Button(self, text="Cancelar", command=self.mostrar_login, width=20).pack()

    def mostrar_menu(self):
        self.limpiar()

        nombre = self.usuario_actual["nombre"] if self.usuario_actual else "Usuario"

        tk.Label(self, text=f"Menú principal - {nombre}", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(self, text="Inicio", width=25, command=lambda: messagebox.showinfo("Inicio", "Pantalla de inicio")).pack(pady=5)
        tk.Button(self, text="Opción 1", width=25, command=lambda: messagebox.showinfo("Opción 1", "Funcionalidad en construcción")).pack(pady=5)
        tk.Button(self, text="Opción 2", width=25, command=lambda: messagebox.showinfo("Opción 2", "Funcionalidad en construcción")).pack(pady=5)
        tk.Button(self, text="Opción 3", width=25, command=lambda: messagebox.showinfo("Opción 3", "Funcionalidad en construcción")).pack(pady=5)
        tk.Button(self, text="Salir", width=25, command=self.mostrar_login).pack(pady=20)
