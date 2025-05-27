from flask import Blueprint, request, jsonify
from models.publicaciones_model import (
    crear_publicacion,
    obtener_publicaciones,
    obtener_publicacion_por_id,
    actualizar_publicacion,
    eliminar_publicacion
)
from auth_middleware import token_requerido

publicaciones_bp = Blueprint("publicaciones", __name__)


@publicaciones_bp.route("/api/publicaciones", methods=["POST"])
@token_requerido
def crear(usuario_token):
    data = request.json
    crear_publicacion(
        usuario_token,
        data["titulo"],
        data["descripcion"],
        data["categoria"],
        data["disponibilidad"]
)

    return jsonify({"mensaje": "Publicación creada correctamente"}), 201

@publicaciones_bp.route("/api/publicaciones", methods=["GET"])
def listar():
    publicaciones = obtener_publicaciones()
    return jsonify(publicaciones), 200

@publicaciones_bp.route("/api/publicaciones/<int:id>", methods=["GET"])
def obtener(id):
    publicacion = obtener_publicacion_por_id(id)
    if publicacion:
        return jsonify(publicacion), 200
    return jsonify({"error": "Publicación no encontrada"}), 404

@publicaciones_bp.route("/api/publicaciones/<int:id>", methods=["PUT"])
@token_requerido
def actualizar(id):
    data = request.json
    actualizar_publicacion(
        id,
        data["titulo"],
        data["descripcion"],
        data["categoria"],
        data["disponibilidad"]
    )
    return jsonify({"mensaje": "Publicación actualizada correctamente"}), 200

@publicaciones_bp.route("/api/publicaciones/<int:id>", methods=["DELETE"])
@token_requerido
def eliminar(id):
    eliminar_publicacion(id)
    return jsonify({"mensaje": "Publicación eliminada correctamente"}), 200

@publicaciones_bp.route("/api/catalogo", methods=["GET"])
def ver_catalogo():
    palabra_clave = request.args.get("q", "").lower()
    categoria = request.args.get("categoria", "").lower()
    disponibilidad = request.args.get("disponibilidad", "").lower()

    publicaciones = obtener_publicaciones()
    resultado = []

    for p in publicaciones:
        if (
            (not palabra_clave or palabra_clave in p["titulo"].lower() or palabra_clave in p["descripcion"].lower())
            and (not categoria or categoria in p["categoria"].lower())
            and (not disponibilidad or disponibilidad in p["disponibilidad"].lower())
        ):
            resultado.append(p)

    return jsonify(resultado), 200
