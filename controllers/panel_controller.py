from flask import Blueprint, jsonify
from models.publicaciones_model import obtener_publicaciones_por_usuario
from models.calificacion_model import obtener_calificaciones_para_usuario
from models.solicitud_model import obtener_historial_de_intercambios

panel_bp = Blueprint("panel", __name__)

@panel_bp.route("/api/panel/<int:usuario_id>", methods=["GET"])
def panel_usuario(usuario_id):
    ofertas = obtener_publicaciones_por_usuario(usuario_id)
    calificaciones = obtener_calificaciones_para_usuario(usuario_id)
    historial = obtener_historial_de_intercambios(usuario_id)

    return jsonify({
        "ofertas_activas": ofertas,
        "calificaciones_recibidas": calificaciones,
        "historial_intercambios": historial
    }), 200
