from config import get_connection

# Crear conversación si no existe para una solicitud aceptada
def crear_conversacion_si_no_existe(solicitud_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM conversaciones WHERE solicitud_id = %s", (solicitud_id,))
    resultado = cursor.fetchone()
    
    if resultado:
        conversacion_id = resultado[0]
    else:
        cursor.execute("""
            INSERT INTO conversaciones (solicitud_id)
            VALUES (%s)
        """, (solicitud_id,))
        conexion.commit()
        conversacion_id = cursor.lastrowid

    cursor.close()
    conexion.close()
    return conversacion_id

# Obtener mensajes de una conversación
def obtener_mensajes(conversacion_id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, u.nombre AS emisor_nombre
        FROM mensajes m
        JOIN usuarios u ON m.emisor_id = u.id
        WHERE m.conversacion_id = %s
        ORDER BY m.fecha_envio ASC
    """, (conversacion_id,))
    mensajes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return mensajes

# Enviar mensaje
def enviar_mensaje(conversacion_id, emisor_id, mensaje):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO mensajes (conversacion_id, emisor_id, mensaje)
        VALUES (%s, %s, %s)
    """, (conversacion_id, emisor_id, mensaje))
    conexion.commit()
    cursor.close()
    conexion.close()
