from flask import Flask
from flask_socketio import SocketIO
from controllers.usuario_controller import usuario_bp
from controllers.publicaciones_controller import publicaciones_bp
from controllers.solicitud_controller import solicitud_bp
from controllers.calificacion_controller import calificacion_bp
from controllers.panel_controller import panel_bp
from controllers.perfil_publico_controller import perfil_publico_bp
from controllers.chat_controller import chat_bp
from flask import render_template


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
#Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(publicaciones_bp)
app.register_blueprint(solicitud_bp)
app.register_blueprint(calificacion_bp)
app.register_blueprint(panel_bp)
app.register_blueprint(perfil_publico_bp)
app.register_blueprint(chat_bp)


#chat
@socketio.on('mensaje')
def manejar_mensaje(data):
    print(f"Nuevo mensaje de {data['emisor_id']}: {data['mensaje']}")
    socketio.emit('mensaje', data, broadcast=True)

#ruta para el frontend
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)


