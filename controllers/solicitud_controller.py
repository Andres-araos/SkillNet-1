from flask import Blueprint, request, jsonify
from config import get_connection
from models.solicitud_model import (crear_solicitud, obtener_solicitudes_por_usuario, 
                                    actualizar_estado_solicitud, eliminar_solicitud, 
                                    contar_solicitudes_activas, obtener_historial_de_intercambios,
                                    obtener_ofertas_activas)
from auth_middleware import token_requerido

solicitud_bp = Blueprint('solicitud', __name__)

@solicitud_bp.route('/api/solicitudes', methods=['POST'])
@token_requerido
def api_crear_solicitud(usuario_token):
    data = request.json
    try:
        activas = contar_solicitudes_activas(usuario_token)
        if activas >= 3:
            return jsonify({"error": "No puedes tener más de 3 solicitudes activas"}), 400

        crear_solicitud(
            usuario_token,  # solicitante_id desde el token
            data['oferente_id'],
            data['publicacion_id']
        )
        return jsonify({"mensaje": "Solicitud creada correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@solicitud_bp.route('/api/solicitudes/<int:usuario_id>', methods=['GET'])
def api_obtener_solicitudes(usuario_id):
    try:
        solicitudes = obtener_solicitudes_por_usuario(usuario_id)
        return jsonify(solicitudes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@solicitud_bp.route('/api/solicitudes/<int:solicitud_id>', methods=['PUT'])
def api_actualizar_estado(solicitud_id):
    data = request.json
    nuevo_estado = data.get('estado')
    if nuevo_estado not in ['pendiente', 'aceptada', 'rechazada']:
        return jsonify({"error": "Estado inválido"}), 400
    try:
        actualizar_estado_solicitud(solicitud_id, nuevo_estado)
        return jsonify({"mensaje": "Estado actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@solicitud_bp.route('/api/solicitudes/<int:solicitud_id>', methods=['DELETE'])
def api_eliminar_solicitud(solicitud_id):
    try:
        eliminar_solicitud(solicitud_id)
        return jsonify({"mensaje": "Solicitud eliminada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@solicitud_bp.route('/api/ofertas-activas/<int:usuario_id>', methods=['GET'])
@token_requerido
def api_ofertas_activas(usuario_id, usuario_token=None):
    try:
        data = obtener_ofertas_activas(usuario_id)
        return jsonify(data), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@solicitud_bp.route('/api/historial/<int:usuario_id>', methods=['GET'])
@token_requerido
def api_historial(usuario_id, usuario_token=None):
    try:
        historial = obtener_historial_de_intercambios(usuario_id)
        return jsonify(historial), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
