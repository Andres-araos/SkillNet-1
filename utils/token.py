import jwt
from datetime import datetime, timedelta

CLAVE_SECRETA = "clave_super_secreta_123"
TIEMPO_EXPIRACION_MINUTOS = 60

# Crear token
def generar_token(usuario_id):
    payload = {
        "usuario_id": usuario_id,
        "exp": datetime.utcnow() + timedelta(minutes=TIEMPO_EXPIRACION_MINUTOS)
    }
    token = jwt.encode(payload, CLAVE_SECRETA, algorithm="HS256")
    return token

# Verificar token
def verificar_token(token):
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=["HS256"])
        return payload["usuario_id"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
