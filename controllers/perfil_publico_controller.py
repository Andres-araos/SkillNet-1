from flask import Blueprint, jsonify
from models.usuario_model import obtener_nombre_usuario
from models.publicaciones_model import obtener_publicaciones_por_usuario
from models.calificacion_model import obtener_calificaciones_para_usuario

perfil_publico_bp = Blueprint("perfil_publico", __name__)

@perfil_publico_bp.route("/api/usuarios/<int:usuario_id>/perfil", methods=["GET"])
def ver_perfil_publico(usuario_id):
    nombre = obtener_nombre_usuario(usuario_id)
    if not nombre:
        return jsonify({"error": "Usuario no encontrado"}), 404

    publicaciones = obtener_publicaciones_por_usuario(usuario_id)
    calificaciones = obtener_calificaciones_para_usuario(usuario_id)

    return jsonify({
        "nombre": nombre,
        "publicaciones": publicaciones,
        "calificaciones": calificaciones
    }), 200
