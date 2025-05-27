from config import get_connection
import bcrypt

def crear_usuario(nombre, email, contrasena, habilidades_ofrece, habilidades_busca, descripcion):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, contrasena, habilidades_ofrece, habilidades_busca, descripcion)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, email, contrasena, habilidades_ofrece, habilidades_busca, descripcion))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_usuario_por_email(email):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario

def verificar_contrasena(email, contrasena_plana):
    usuario = obtener_usuario_por_email(email)
    if usuario and bcrypt.checkpw(contrasena_plana.encode(), usuario['contrasena'].encode()):
        return usuario
    return None

def obtener_usuario_por_id(usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario

def actualizar_usuario(usuario_id, data):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nombre = %s, habilidades_ofrece = %s, habilidades_busca = %s, descripcion = %s
        WHERE id = %s
    """, (
        data.get("nombre"),
        data.get("habilidades_ofrece"),
        data.get("habilidades_busca"),
        data.get("descripcion"),
        usuario_id
    ))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_nombre_usuario(usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado[0] if resultado else None
