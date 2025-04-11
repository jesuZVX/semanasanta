import tkinter as tk
from tkinter import ttk, messagebox
from backadmin import obtener_proyectos_y_tareas, crear_proyecto, crear_tarea
from bd import Usuario, SessionLocal  # Asegúrate de que la ruta sea correcta
import bcrypt
from backlogin import verificar_login, crear_usuario, cambiar_contraseña

def salir():
    if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
        root.quit()

# ------ INICIAR SESIÓN ------
def abrir_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Iniciar Sesión")
    login_window.geometry("400x400")
    login_window.configure(bg="#d9f4d0")

    tk.Label(login_window, text="Nombre de usuario:", font=("Arial", 14), bg="#d9f4d0", fg="#234e1b").pack(pady=5)
    entry_username_login = tk.Entry(login_window, font=("Arial", 12))
    entry_username_login.pack(pady=5)

    tk.Label(login_window, text="Contraseña:", font=("Arial", 14), bg="#d9f4d0", fg="#234e1b").pack(pady=5)
    entry_password_login = tk.Entry(login_window, font=("Arial", 12), show="*")
    entry_password_login.pack(pady=5)

    def intentar_login():
        username = entry_username_login.get()
        password = entry_password_login.get()
        user = verificar_login(username, password)  # Get the user object

        if user:
            messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
            login_window.destroy()
            root.destroy()
            # Import and call the function to show the main panel
            import administrador
            administrador.mostrar_panel_principal(user)
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    tk.Button(login_window, text="Entrar", command=intentar_login,
              font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

# ------ CREAR USUARIO ------
def crear_usuario_window():
    create_window = tk.Toplevel(root)
    create_window.title("Crear Nuevo Usuario")
    create_window.geometry("400x400")
    create_window.configure(bg="#d9f4d0")

    tk.Label(create_window, text="Nombre de usuario:", font=("Arial", 14), bg="#d9f4d0", fg="#234e1b").pack(pady=5)
    entry_new_username = tk.Entry(create_window, font=("Arial", 12))
    entry_new_username.pack(pady=5)

    tk.Label(create_window, text="Contraseña:", font=("Arial", 14), bg="#d9f4d0", fg="#234e1b").pack(pady=5)
    entry_new_password = tk.Entry(create_window, font=("Arial", 12), show="*")
    entry_new_password.pack(pady=5)

    tk.Label(create_window, text="Rol:", font=("Arial", 14), bg="#d9f4d0", fg="#234e1b").pack(pady=5)
    entry_new_role = tk.Entry(create_window, font=("Arial", 12))
    entry_new_role.pack(pady=5)

    def guardar_usuario():
        new_username = entry_new_username.get()
        new_password = entry_new_password.get()
        new_role = entry_new_role.get()

        if new_username and new_password and new_role:
            result = crear_usuario(new_username, new_password, new_role)
            if result == "¡Usuario creado exitosamente!":
                messagebox.showinfo("Éxito", result)
                create_window.destroy()
            else:
                messagebox.showerror("Error", result)
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    tk.Button(create_window, text="Guardar Usuario", command=guardar_usuario,
              font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

# ------ CAMBIAR CONTRASEÑA ------
def cambiar_contraseña_window():
    cambio_window = tk.Toplevel(root)
    cambio_window.title("Recuperar Contraseña")
    cambio_window.geometry("400x400")
    cambio_window.configure(bg="#d9f4d0")

    tk.Label(cambio_window, text="Nombre de usuario:", font=("Arial", 14), bg="#d9f4d0", fg="#234e1b").pack(pady=5)
    entry_user = tk.Entry(cambio_window, font=("Arial", 12))
    entry_user.pack(pady=5)

    tk.Label(cambio_window, text="Nueva contraseña:", font=("Arial", 14), bg="#d9f4d0", fg="#234e1b").pack(pady=5)
    entry_new_pass = tk.Entry(cambio_window, font=("Arial", 12), show="*")
    entry_new_pass.pack(pady=5)

    def cambiar():
        user = entry_user.get()
        new_pass = entry_new_pass.get()
        if user and new_pass:
            result = cambiar_contraseña(user, new_pass)
            if result == "¡Contraseña actualizada!":
                messagebox.showinfo("Éxito", result)
                cambio_window.destroy()
            else:
                messagebox.showerror("Error", result)
        else:
            messagebox.showerror("Error", "Por favor, complete los campos.")

    tk.Button(cambio_window, text="Actualizar", command=cambiar,
              font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)

root = tk.Tk()
root.title("Bienvenido")
root.geometry("800x600")
root.configure(bg="#c7f5cc")

tk.Label(root, text="Bienvenido a la aplicación", font=("Arial", 24, "bold"),
         bg="#c7f5cc", fg="#234e1b").pack(pady=60)

# Botón: REGISTRARSE
tk.Button(root, text="REGISTRARSE", command=crear_usuario_window,
         font=("Arial", 16, "bold"), bg="white", fg="#2d8f47",
         relief="flat", bd=3, padx=20, pady=10).pack(pady=10)

# Botón: INICIAR SESIÓN
tk.Button(root, text="INICIAR SESIÓN", command=abrir_login_window,
         font=("Arial", 16, "bold"), bg="white", fg="#2d8f47",
         relief="flat", bd=3, padx=20, pady=10).pack(pady=10)

# Botón: ¿Olvidaste tu contraseña?
tk.Button(root, text="¿Olvidaste tu contraseña?", command=cambiar_contraseña_window,
         font=("Arial", 12, "underline"), bg="#c7f5cc", fg="#234e1b",
         relief="flat", cursor="hand2").pack(pady=5)

# Botón: SALIR
tk.Button(root, text="SALIR", command=salir,
         font=("Arial", 12), bg="#a1a1a1", fg="white",
         relief="flat", padx=10, pady=5).pack(pady=30)

root.mainloop()