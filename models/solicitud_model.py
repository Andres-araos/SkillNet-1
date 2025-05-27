from config import get_connection

# Crear una nueva solicitud
def crear_solicitud(solicitante_id, oferente_id, publicacion_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO solicitudes (solicitante_id, oferente_id, publicacion_id)
        VALUES (%s, %s, %s)
    """, (solicitante_id, oferente_id, publicacion_id))
    conexion.commit()
    cursor.close()
    conexion.close()

# Obtener solicitudes por usuario (como solicitante u oferente)
def obtener_solicitudes_por_usuario(usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM solicitudes
        WHERE solicitante_id = %s OR oferente_id = %s
        ORDER BY fecha_solicitud DESC
    """, (usuario_id, usuario_id))
    solicitudes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return solicitudes

# Actualizar estado de una solicitud (aceptar o rechazar)
def actualizar_estado_solicitud(solicitud_id, nuevo_estado):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE solicitudes
        SET estado = %s
        WHERE id = %s
    """, (nuevo_estado, solicitud_id))
    conexion.commit()
    cursor.close()
    conexion.close()

# Eliminar una solicitud 
def eliminar_solicitud(solicitud_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM solicitudes WHERE id = %s", (solicitud_id,))
    conexion.commit()
    cursor.close()
    conexion.close()

# Solicitudes maximas de 3
def contar_solicitudes_activas(solicitante_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM solicitudes
        WHERE solicitante_id = %s AND estado IN ('pendiente', 'aceptada')
    """, (solicitante_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado[0]

def obtener_historial_de_intercambios(usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id AS solicitud_id,
               s.solicitante_id, s.oferente_id,
               u1.nombre AS nombre_solicitante,
               u2.nombre AS nombre_oferente,
               p.titulo,
               s.fecha_solicitud
        FROM solicitudes s
        JOIN usuarios u1 ON s.solicitante_id = u1.id
        JOIN usuarios u2 ON s.oferente_id = u2.id
        JOIN publicaciones p ON s.publicacion_id = p.id
        WHERE (s.solicitante_id = %s OR s.oferente_id = %s)
          AND s.estado = 'aceptada'
        ORDER BY s.fecha_solicitud DESC
    """, (usuario_id, usuario_id))
    historial = cursor.fetchall()
    cursor.close()
    conexion.close()

    resultado = []
    for item in historial:
        otro_id = item["oferente_id"] if item["solicitante_id"] == usuario_id else item["solicitante_id"]
        otro_nombre = item["nombre_oferente"] if item["solicitante_id"] == usuario_id else item["nombre_solicitante"]
        resultado.append({
            "solicitud_id": item["solicitud_id"],
            "otro_usuario_id": otro_id,
            "otro_usuario_nombre": otro_nombre,
            "titulo": item["titulo"],
            "fecha_solicitud": item["fecha_solicitud"],
            "ya_calificado": False,
            "valoracion": None,
            "comentario": None
        })

    return resultado

def obtener_ofertas_activas(usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        # Enviadas por el usuario
        cursor.execute("""
            SELECT s.id, s.estado, s.fecha_solicitud, u.nombre AS oferente_nombre
            FROM solicitudes s
            JOIN usuarios u ON s.oferente_id = u.id
            WHERE s.solicitante_id = %s
        """, (usuario_id,))
        enviadas = cursor.fetchall()

        # Recibidas por el usuario
        cursor.execute("""
            SELECT s.id, s.estado, s.fecha_solicitud, u.nombre AS solicitante_nombre
            FROM solicitudes s
            JOIN usuarios u ON s.solicitante_id = u.id
            WHERE s.oferente_id = %s
        """, (usuario_id,))
        recibidas = cursor.fetchall()

        return {"enviadas": enviadas, "recibidas": recibidas}

    finally:
        cursor.close()
        conexion.close()
