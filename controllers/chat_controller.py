from flask import Blueprint, request, jsonify
from models.chat_model import (
    crear_conversacion_si_no_existe,
    obtener_mensajes,
    enviar_mensaje
)
from models.solicitud_model import obtener_solicitudes_por_usuario
from auth_middleware import token_requerido

chat_bp = Blueprint("chat", __name__)

# Obtener mensajes de una conversación (si el usuario está involucrado)
@chat_bp.route("/api/chat/<int:solicitud_id>/<int:usuario_id>", methods=["GET"])
def ver_chat(solicitud_id, usuario_id):
    solicitudes = obtener_solicitudes_por_usuario(usuario_id)
    permitido = any(
        s["id"] == solicitud_id and s["estado"] == "aceptada"
        for s in solicitudes
    )

    if not permitido:
        return jsonify({"error": "No tienes acceso a esta conversación"}), 403

    conversacion_id = crear_conversacion_si_no_existe(solicitud_id)
    mensajes = obtener_mensajes(conversacion_id)
    return jsonify({"conversacion_id": conversacion_id, "mensajes": mensajes}), 200

# Enviar mensaje en conversación
@chat_bp.route("/api/chat", methods=["POST"])
@token_requerido
def enviar():
    data = request.get_json()
    solicitud_id = data["solicitud_id"]
    emisor_id = data["emisor_id"]
    mensaje = data["mensaje"]

    conversacion_id = crear_conversacion_si_no_existe(solicitud_id)
    enviar_mensaje(conversacion_id, emisor_id, mensaje)
    return jsonify({"mensaje": "Mensaje enviado"}), 201
