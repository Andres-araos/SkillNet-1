# cifrado y manejo de contraseñas
import hashlib

import bcrypt

def hash_contrasena(contrasena_plana):
    return bcrypt.hashpw(contrasena_plana.encode(), bcrypt.gensalt()).decode()


def verificar_contrasena(contrasena_plana, contrasena_hashed):
    return hash_contrasena(contrasena_plana) == contrasena_hashed
