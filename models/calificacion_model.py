from config import get_connection

# Crear una nueva calificación
def crear_calificacion(de_usuario_id, para_usuario_id, comentario, valoracion):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO calificaciones (de_usuario_id, para_usuario_id, comentario, valoracion)
        VALUES (%s, %s, %s, %s)
    """, (de_usuario_id, para_usuario_id, comentario, valoracion))
    conexion.commit()
    cursor.close()
    conexion.close()

# Obtener calificaciones recibidas por un usuario
def obtener_calificaciones_para_usuario(para_usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id, c.comentario, c.valoracion, c.fecha_calificacion,
               u.nombre AS de_usuario_nombre
        FROM calificaciones c
        JOIN usuarios u ON c.de_usuario_id = u.id
        WHERE c.para_usuario_id = %s
        ORDER BY c.fecha_calificacion DESC
    """, (para_usuario_id,))
    calificaciones = cursor.fetchall()
    cursor.close()
    conexion.close()
    return calificaciones

# Verifica si ya existe una calificación de un usuario a otro
def ya_fue_calificado(de_usuario_id, para_usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM calificaciones
        WHERE de_usuario_id = %s AND para_usuario_id = %s
    """, (de_usuario_id, para_usuario_id))
    resultado = cursor.fetchone()[0]
    cursor.close()
    conexion.close()
    return resultado > 0
