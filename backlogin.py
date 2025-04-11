from tkinter import messagebox
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from bd import Usuario


DB_HOST = 'localhost'
DB_NAME = 'gestion_proyectos_db'
DB_USER = 'root'
DB_PASSWORD = ''

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funciones Login
def verificar_login(username, password):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.contraseña.encode('utf-8')):
            return usuario  # Return the Usuario object on success
        else:
            return None     # Return None on failure
    except SQLAlchemyError as e:
        messagebox.showerror("Error de Base de Datos", f"Hubo un problema al conectar o consultar la base de datos: {e}")
        return None
    finally:
        db.close()

def crear_usuario(username, password, rol, email):
    db = SessionLocal()
    try:
        existing_user = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
        if existing_user:
            return "El nombre de usuario ya está en uso."
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = Usuario(nombre_usuario=username, contraseña=hashed_password.decode('utf-8'), rol=rol, correo_electronico=email)
            db.add(new_user)
            db.commit()
            return "¡Usuario creado exitosamente!"
    except SQLAlchemyError as e:
        db.rollback()
        messagebox.showerror("Error de Base de Datos", f"Hubo un problema al crear el usuario en la base de datos: {e}")
        return f"Error al crear usuario: {e}"
    finally:
        db.close()

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
        messagebox.showerror("Error de Base de Datos", f"Hubo un problema al actualizar la contraseña en la base de datos: {e}")
        return f"Error al cambiar contraseña: {e}"
    finally:
        db.close()