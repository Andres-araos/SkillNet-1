from flask import request, jsonify
from functools import wraps
from utils.token import verificar_token

def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[-1]  # Bearer <token>

        if not token:
            return jsonify({"error": "Token no proporcionado"}), 401

        usuario_id = verificar_token(token)
        if not usuario_id:
            return jsonify({"error": "Token inválido o expirado"}), 401

 
        kwargs["usuario_token"] = usuario_id
        return f(*args, **kwargs)


    return decorador
