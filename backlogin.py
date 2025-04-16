from tkinter import messagebox
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from bd import Usuario  # Asegúrate que 'bd.py' tenga el modelo Usuario definido correctamente


# --- Configuración de conexión ---
DB_HOST = 'localhost'
DB_NAME = 'gestion_proyectos_db'
DB_USER = 'root'
DB_PASSWORD = ''

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Motor y sesión
engine = create_engine(DATABASE_URL, echo=False)  # echo=True para ver SQL en consola (útil para debug)
SessionLocal = sessionmaker(bind=engine)


# --- Función para verificar inicio de sesión ---
def verificar_login(username: str, password: str):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.contraseña.encode('utf-8')):
            return usuario
        return None
    except SQLAlchemyError as e:
        messagebox.showerror("Error de Base de Datos", f"Hubo un problema al verificar el inicio de sesión:\n{e}")
        return None
    finally:
        db.close()


# --- Función para crear un nuevo usuario ---
def crear_usuario(username: str, password: str, rol: str, correo_electronico: str, creador_admin=False):
    db = SessionLocal()
    try:
        # Validación: Usuario existente
        if db.query(Usuario).filter(Usuario.nombre_usuario == username).first():
            return "El nombre de usuario ya está en uso."

        # Restricción para crear administradores
        if rol == "administrador" and not creador_admin:
            return "No tienes permiso para crear un usuario administrador."

        # Encriptar contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Crear y guardar nuevo usuario
        nuevo_usuario = Usuario(
            nombre_usuario=username,
            contraseña=hashed_password,
            rol=rol,
            correo_electronico=correo_electronico
        )

        db.add(nuevo_usuario)
        db.commit()
        return "¡Usuario creado exitosamente!"

    except SQLAlchemyError as e:
        db.rollback()
        messagebox.showerror("Error de Base de Datos", f"No se pudo crear el usuario:\n{e}")
        return "Error al crear usuario."
    finally:
        db.close()


# --- Función para cambiar la contraseña ---
def cambiar_contraseña(username: str, new_password: str):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if not usuario:
            return "Usuario no encontrado."

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario.contraseña = hashed_password
        db.commit()
        return "¡Contraseña actualizada!"

    except SQLAlchemyError as e:
        db.rollback()
        messagebox.showerror("Error de Base de Datos", f"No se pudo actualizar la contraseña:\n{e}")
        return "Error al cambiar contraseña."
    finally:
        db.close()
