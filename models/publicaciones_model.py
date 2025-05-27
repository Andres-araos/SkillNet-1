from config import get_connection

def crear_publicacion(usuario_id, titulo, descripcion, categoria, disponibilidad):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO publicaciones (usuario_id, titulo, descripcion, categoria, disponibilidad)
        VALUES (%s, %s, %s, %s, %s)
    """, (usuario_id, titulo, descripcion, categoria, disponibilidad))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_publicaciones():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, u.nombre AS nombre_usuario
        FROM publicaciones p
        JOIN usuarios u ON p.usuario_id = u.id
        ORDER BY fecha_publicacion DESC
    """)
    publicaciones = cursor.fetchall()
    cursor.close()
    conexion.close()
    return publicaciones


def obtener_publicacion_por_id(id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM publicaciones WHERE id = %s", (id,))
    publicacion = cursor.fetchone()
    cursor.close()
    conexion.close()
    return publicacion

def actualizar_publicacion(id, titulo, descripcion, categoria, disponibilidad):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE publicaciones
        SET titulo = %s, descripcion = %s, categoria = %s, disponibilidad = %s
        WHERE id = %s
    """, (titulo, descripcion, categoria, disponibilidad, id))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_publicacion(id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM publicaciones WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    
def obtener_publicaciones_por_usuario(usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM publicaciones
        WHERE usuario_id = %s
        ORDER BY fecha_publicacion DESC
    """, (usuario_id,))
    publicaciones = cursor.fetchall()
    cursor.close()
    conexion.close()
    return publicaciones

