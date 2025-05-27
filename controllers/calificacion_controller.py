from flask import Blueprint, request, jsonify
from models.calificacion_model import (
    crear_calificacion,
    obtener_calificaciones_para_usuario,
    ya_fue_calificado
)
from models.solicitud_model import obtener_solicitudes_por_usuario
from auth_middleware import token_requerido

calificacion_bp = Blueprint("calificacion", __name__)

# Ruta para crear una calificación
@calificacion_bp.route("/api/calificaciones", methods=["POST"])
@token_requerido
def api_crear_calificacion(usuario_token):
    data = request.json
    de_id = usuario_token  # ya que el token representa al usuario autenticado
    para_id = data["para_usuario_id"]

    # Evitar duplicado
    if ya_fue_calificado(de_id, para_id):
        return jsonify({"error": "Ya has calificado a este usuario"}), 400

    # Validar que hubo intercambio aceptado
    solicitudes = obtener_solicitudes_por_usuario(de_id)
    intercambio_valido = any(
        s["estado"] == "aceptada" and s["solicitante_id"] in [de_id, para_id] and s["oferente_id"] in [de_id, para_id]
        for s in solicitudes
    )

    if not intercambio_valido:
        return jsonify({"error": "Solo puedes calificar después de un intercambio aceptado"}), 403

    crear_calificacion(
        de_usuario_id=de_id,
        para_usuario_id=para_id,
        comentario=data["comentario"],
        valoracion=data["valoracion"]
    )
    return jsonify({"mensaje": "Calificación registrada"}), 201


# Ruta para ver las calificaciones recibidas
@calificacion_bp.route("/api/calificaciones/<int:usuario_id>", methods=["GET"])
def api_ver_calificaciones(usuario_id):
    calificaciones = obtener_calificaciones_para_usuario(usuario_id)
    return jsonify(calificaciones), 200
