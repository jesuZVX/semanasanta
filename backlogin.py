from tkinter import messagebox
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from bd import Usuario  # Asegúrate que 'bd.py' tenga el modelo Usuario correctamente definido


# --- Configuración de conexión ---

DB_HOST = 'localhost'
DB_NAME = 'gestion_proyectos_db'
DB_USER = 'root'
DB_PASSWORD = ''

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Función para verificar inicio de sesión ---

def verificar_login(username, password):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.contraseña.encode('utf-8')):
            return usuario
        else:
            return None
    except SQLAlchemyError as e:
        messagebox.showerror("Error de Base de Datos", f"Hubo un problema al conectar o consultar la base de datos:\n{e}")
        return None
    finally:
        db.close()


# --- Función para crear un nuevo usuario ---

def crear_usuario(username, password, rol, correo_electronico, creador_admin=False):
    db = SessionLocal()
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if existing_user:
            return "El nombre de usuario ya está en uso."

        # Solo un administrador puede crear a otro administrador
        if rol == "administrador" and not creador_admin:
            return "No tienes permiso para crear un usuario administrador."

        # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = Usuario(
            nombre_usuario=username,
            contraseña=hashed_password.decode('utf-8'),
            rol=rol,
            correo_electronico=correo_electronico
        )

        db.add(new_user)
        db.commit()
        return "¡Usuario creado exitosamente!"

    except SQLAlchemyError as e:
        db.rollback()
        messagebox.showerror("Error de Base de Datos", f"Hubo un problema al crear el usuario en la base de datos:\n{e}")
        return f"Error al crear usuario: {e}"
    finally:
        db.close()


# --- Función para cambiar la contraseña ---

def cambiar_contraseña(username, new_password):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if usuario:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            usuario.contraseña = hashed_password.decode('utf-8')
            db.commit()
            return "¡Contraseña actualizada!"
        else:
            return "Usuario no encontrado."
    except SQLAlchemyError as e:
        db.rollback()
        messagebox.showerror("Error de Base de Datos", f"Hubo un problema al actualizar la contraseña en la base de datos:\n{e}")
        return f"Error al cambiar contraseña: {e}"
    finally:
        db.close()
