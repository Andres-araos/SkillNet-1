from flask import Blueprint, request, jsonify
from models.usuario_model import (
    crear_usuario,
    obtener_usuario_por_email,
    verificar_contrasena as verificar_credenciales,
    obtener_usuario_por_id,
    actualizar_usuario
)
from models.publicaciones_model import obtener_publicaciones_por_usuario
from models.calificacion_model import obtener_calificaciones_para_usuario, ya_fue_calificado
from models.solicitud_model import obtener_solicitudes_por_usuario
from utils.seguridad import hash_contrasena
from utils.token import generar_token
from auth_middleware import token_requerido

usuario_bp = Blueprint("usuario", __name__)

# Registro
@usuario_bp.route("/api/registro", methods=["POST"])
def registro():
    data = request.json
    if obtener_usuario_por_email(data["email"]):
        return jsonify({"mensaje": "El correo ya está registrado"}), 400

    contrasena_hashed = hash_contrasena(data["contrasena"])
    crear_usuario(
        data["nombre"],
        data["email"],
        contrasena_hashed,
        data["habilidades_ofrece"],
        data["habilidades_busca"],
        data.get("descripcion", "")
    )
    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

# Login
@usuario_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    contrasena = data.get("contrasena")

    usuario = verificar_credenciales(email, contrasena)
    if usuario:
        token = generar_token(usuario["id"])
        return jsonify({
            "mensaje": "Login exitoso",
            "usuario_id": usuario["id"],
            "token": token
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# Obtener perfil del propio usuario
@usuario_bp.route("/api/perfil/<int:usuario_id>", methods=["GET"])
def obtener_perfil(usuario_id):
    usuario = obtener_usuario_por_id(usuario_id)
    if usuario:
        del usuario["contrasena"]
        return jsonify(usuario), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# Actualizar perfil del propio usuario
@usuario_bp.route("/api/perfil/<int:usuario_id>", methods=["PUT"])
def actualizar_perfil(usuario_id):
    data = request.get_json()
    actualizar_usuario(usuario_id, data)
    return jsonify({"mensaje": "Perfil actualizado correctamente"}), 200

# Perfil público de otro usuario (con publicaciones, calificaciones y permiso para calificar)
@usuario_bp.route("/api/usuarios/<int:usuario_id>/perfil", methods=["GET"])
@token_requerido
def perfil_publico(usuario_id, usuario_token=None):
    datos_usuario = obtener_usuario_por_id(usuario_id)
    if not datos_usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    publicaciones = obtener_publicaciones_por_usuario(usuario_id)
    calificaciones = obtener_calificaciones_para_usuario(usuario_id)

    solicitudes = obtener_solicitudes_por_usuario(usuario_token)
    ya_califico = ya_fue_calificado(usuario_token, usuario_id)

    puede_calificar = not ya_califico and any(
        s["estado"] == "aceptada" and (
            (s["solicitante_id"] == usuario_token and s["oferente_id"] == usuario_id) or
            (s["solicitante_id"] == usuario_id and s["oferente_id"] == usuario_token)
        )
        for s in solicitudes
    )

    return jsonify({
        "nombre": datos_usuario["nombre"],
        "descripcion": datos_usuario.get("descripcion"),
        "habilidades_ofrece": datos_usuario.get("habilidades_ofrece"),
        "habilidades_busca": datos_usuario.get("habilidades_busca"),
        "publicaciones": publicaciones,
        "calificaciones": calificaciones,
        "permite_calificar": puede_calificar
    }), 200
