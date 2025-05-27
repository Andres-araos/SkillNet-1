const URL_BASE = window.location.origin;
let token = localStorage.getItem("token");
let usuario_id = localStorage.getItem("usuario_id");
let historialVistas = [];
let historialSecciones = []; 



document.addEventListener("DOMContentLoaded", () => {
  if (token) mostrarPanel();

  document.getElementById("login-form").addEventListener("submit", login);
  document.getElementById("registro-form").addEventListener("submit", registrar);
  document.getElementById("mostrar-registro").onclick = () => mostrarSeccion("registro-section");
  document.getElementById("volver-login").onclick = () => mostrarSeccion("login-section");
  document.getElementById("cerrar-sesion").onclick = cerrarSesion;

  document.getElementById("boton-atras").onclick = retrocederVista;
  document.getElementById("editar-descripcion").onclick = () => {
    document.getElementById("form-editar-descripcion").style.display = "block";
  };
  document.getElementById("guardar-descripcion").onclick = guardarDescripcion;
});

function mostrarSeccion(id) {
  document.querySelectorAll("section").forEach(s => s.style.display = "none");
  document.getElementById(id).style.display = "block";
  document.getElementById("boton-atras").style.display = "none";
}

function mostrarSeccionPanel(seccion) {
  document.querySelectorAll(".seccion-panel").forEach(div => div.style.display = "none");
  const actual = `seccion-${seccion}`;
  historialVistas.push(actual);
  document.getElementById(actual).style.display = "block";
  document.getElementById("boton-atras").style.display = "inline";

  if (seccion === "catalogo") cargarCatalogo();
  else if (seccion === "mis-publicaciones") cargarMisPublicaciones();
  else if (seccion === "ofertas-activas") cargarOfertasActivas();
  else if (seccion === "historial-intercambios") cargarHistorial();
  else if (seccion === "chat") document.getElementById("seccion-chat").style.display = "block";
}

function retrocederVista() {
  historialVistas.pop(); // actual
  const anterior = historialVistas.pop(); // anterior
  if (anterior) {
    document.querySelectorAll(".seccion-panel").forEach(div => div.style.display = "none");
    document.getElementById(anterior).style.display = "block";
    historialVistas.push(anterior); // lo volvemos a poner como actual
  } else {
    document.getElementById("boton-atras").style.display = "none";
  }
}


function retrocederSeccion() {
  if (historialSecciones.length > 1) {
    const actual = historialSecciones.pop();
    const anterior = historialSecciones[historialSecciones.length - 1];
    document.getElementById(actual).style.display = "none";
    document.getElementById(anterior).style.display = "block";
  } else {
    document.getElementById("boton-atras").style.display = "none";
  }
}

function cerrarSesion() {
  localStorage.removeItem("token");
  localStorage.removeItem("usuario_id");
  token = null;
  usuario_id = null;
  mostrarSeccion("login-section");
}

// --- LOGIN / REGISTRO ---
async function login(e) {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const contrasena = document.getElementById("password").value;

  const res = await fetch(`${URL_BASE}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, contrasena }),
  });

  const data = await res.json();
  if (res.ok) {
    token = data.token;
    usuario_id = data.usuario_id;
    localStorage.setItem("token", token);
    localStorage.setItem("usuario_id", usuario_id);
    mostrarPanel();
  } else {
    alert(data.error);
  }
}

async function registrar(e) {
  e.preventDefault();
  const data = {
    nombre: document.getElementById("reg-nombre").value,
    email: document.getElementById("reg-email").value,
    contrasena: document.getElementById("reg-password").value,
    habilidades_ofrece: document.getElementById("reg-ofrece").value,
    habilidades_busca: document.getElementById("reg-busca").value,
      descripcion: document.getElementById("reg-descripcion").value,
  };

  const res = await fetch(`${URL_BASE}/api/registro`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const response = await res.json();
  if (res.ok) {
    alert("Registrado correctamente. Ahora inicia sesión.");
    mostrarSeccion("login-section");
  } else {
    alert(response.mensaje || "Error al registrar.");
  }
}

// --- PANEL DE USUARIO ---
async function mostrarPanel() {
  mostrarSeccion("panel-usuario");

  const res = await fetch(`${URL_BASE}/api/perfil/${usuario_id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();

  document.getElementById("bienvenida").innerText = `Hola, Usuario ${usuario_id} - ${data.nombre}`;
  document.getElementById("descripcion-texto").innerText = data.descripcion || "(sin descripción)";
  const campoDescripcion = document.getElementById("descripcion-nueva");
if (campoDescripcion) {
  campoDescripcion.value = data.descripcion || "";
}

  document.getElementById("habilidades-ofrece").innerText = data.habilidades_ofrece || "(sin datos)";
  document.getElementById("habilidades-busca").innerText = data.habilidades_busca || "(sin datos)";

  historialSecciones = [];

  conectarSocket();  // ← importante para mantener el chat
}


async function guardarDescripcion() {
  const nueva = document.getElementById("descripcion-nueva").value;
  const res = await fetch(`${URL_BASE}/api/usuarios/${usuario_id}/descripcion`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ descripcion: nueva })
  });

  if (res.ok) {
    document.getElementById("descripcion-texto").innerText = nueva;
    document.getElementById("form-editar-descripcion").style.display = "none";
    alert("Descripción actualizada.");
  }
}

// --- PUBLICACIONES / CATALOGO ---
async function cargarCatalogo() {
  const res = await fetch(`${URL_BASE}/api/catalogo`);
  const publicaciones = await res.json();

  const contenedor = document.getElementById("seccion-catalogo");
  contenedor.innerHTML = "";

  publicaciones
    .filter(pub => pub.usuario_id != usuario_id)
    .forEach(pub => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <h4>${pub.titulo}</h4>
        <p>${pub.descripcion}</p>
        <p><em>${pub.categoria} | ${pub.disponibilidad}</em></p>
        <button onclick="verPerfilUsuario(${pub.usuario_id})">Ver perfil</button>
      `;
      contenedor.appendChild(card);
    });
}

async function cargarMisPublicaciones() {
  const res = await fetch(`${URL_BASE}/api/panel/${usuario_id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();

  const contenedor = document.getElementById("seccion-mis-publicaciones");
  contenedor.innerHTML = "<h3>Mis publicaciones</h3>";
  data.ofertas_activas.forEach(pub => {
    const div = document.createElement("div");
    div.className = "card";
    div.innerHTML = `
      <h4>${pub.titulo}</h4>
      <p>${pub.descripcion}</p>
      <p><em>${pub.categoria} | ${pub.disponibilidad}</em></p>
      <button onclick="editarPublicacion(${pub.id})">Editar</button>
      <button onclick="eliminarPublicacion(${pub.id})">Eliminar</button>
    `;
    contenedor.appendChild(div);
  });
  // Aquí puedes agregar el botón para crear una nueva publicación
}

// --- PERFIL PÚBLICO ---
async function verPerfilUsuario(id) {
  const res = await fetch(`${URL_BASE}/api/usuarios/${id}/perfil`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  const data = await res.json();
  if (!res.ok) {
    alert("No se pudo cargar el perfil");
    return;
  }

  const contenedor = document.getElementById("seccion-catalogo");
  let html = `
    <h3>Perfil de ${data.nombre}</h3>
    <p><strong>Descripción:</strong> ${data.descripcion || "(sin descripción)"}</p>
    <p><strong>Habilidades que ofrece:</strong> ${data.habilidades_ofrece || "(sin datos)"}</p>
    <p><strong>Habilidades que busca:</strong> ${data.habilidades_busca || "(sin datos)"}</p>

    <h4>Publicaciones</h4>
    ${data.publicaciones.map(p => `
      <div class="card">
        <strong>${p.titulo}</strong>
        <p>${p.descripcion}</p>
        <p><em>${p.categoria} | ${p.disponibilidad}</em></p>
        <button onclick="enviarSolicitud(${id}, ${p.id})">Solicitar intercambio</button>
      </div>
    `).join("")}

    <h4>Calificaciones</h4>
    ${data.calificaciones.length > 0 
      ? data.calificaciones.map(c => `<div>⭐ ${c.valoracion} - ${c.comentario}</div>`).join("")
      : "<p>No tiene calificaciones aún.</p>"}
  `;

  if (data.permite_calificar) {
    html += `
      <div id="form-calificacion">
        <h4>Agregar calificación</h4>
        <select id="valoracion">
          <option value="1">⭐</option>
          <option value="2">⭐⭐</option>
          <option value="3">⭐⭐⭐</option>
          <option value="4">⭐⭐⭐⭐</option>
          <option value="5" selected>⭐⭐⭐⭐⭐</option>
        </select>
        <textarea id="comentario" placeholder="Comentario..."></textarea>
        <button onclick="enviarCalificacion(${id})">Enviar calificación</button>
      </div>
    `;
  }

contenedor.innerHTML = html;

// Mostrar solo la sección de catálogo sin recargarla
document.querySelectorAll(".seccion-panel").forEach(div => div.style.display = "none");
document.getElementById("seccion-catalogo").style.display = "block";

}



async function enviarCalificacion(para_id) {
  const valoracion = parseInt(document.getElementById("valoracion").value);
  const comentario = document.getElementById("comentario").value;

  const res = await fetch(`${URL_BASE}/api/calificaciones`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      de_usuario_id: parseInt(usuario_id),
      para_usuario_id: parseInt(para_id),
      comentario,
      valoracion
    })
  });

  const data = await res.json();
  if (res.ok) {
    alert("¡Calificación enviada!");
    mostrarSeccionPanel("catalogo"); // volver al catálogo
  } else {
    alert(data.error || "Error al enviar calificación");
  }
}




// --- SOLICITUD ---
async function enviarSolicitud(oferente_id, publicacion_id) {
  const res = await fetch(`${URL_BASE}/api/solicitudes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      solicitante_id: parseInt(usuario_id),
      oferente_id: parseInt(oferente_id),
      publicacion_id: parseInt(publicacion_id)
    })
  });

  const data = await res.json();
  alert(data.mensaje || data.error);
}

// --- CHAT EN TIEMPO REAL ---
let socket;

function conectarSocket() {
  socket = io(URL_BASE);

  socket.on("connect", () => {
    console.log("Conectado al servidor en tiempo real");
  });

  socket.on("mensaje", (data) => {
    const contenedor = document.getElementById("chat-mensajes");
    const div = document.createElement("div");
    div.innerText = `${data.emisor_id}: ${data.mensaje}`;
    contenedor.appendChild(div);
  });

  document.getElementById("form-chat").addEventListener("submit", e => {
    e.preventDefault();
    const input = document.getElementById("mensaje-input");
    const mensaje = input.value;
    input.value = "";

    socket.emit("mensaje", {
      emisor_id: usuario_id,
      mensaje: mensaje
    });

    fetch(`${URL_BASE}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        solicitud_id: prompt("ID de la solicitud aceptada:"),
        emisor_id: usuario_id,
        mensaje: mensaje
      })
    });
  });
}

function mostrarFormularioPublicacion() {
  const form = document.getElementById("form-nueva-publicacion");
  form.style.display = form.style.display === "none" ? "block" : "none";
}

async function crearPublicacion() {
  const titulo = document.getElementById("nueva-titulo").value;
  const descripcion = document.getElementById("nueva-descripcion").value;
  const categoria = document.getElementById("nueva-categoria").value;
  const disponibilidad = document.getElementById("nueva-disponibilidad").value;

  const res = await fetch(`${URL_BASE}/api/publicaciones`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      usuario_id: usuario_id,
      titulo,
      descripcion,
      categoria,
      disponibilidad
    })
  });

  if (res.ok) {
    alert("Publicación creada.");
    cargarMisPublicaciones();
    document.getElementById("form-nueva-publicacion").style.display = "none";
  } else {
    alert("Error al crear la publicación.");
  }
}

async function eliminarPublicacion(id) {
  if (!confirm("¿Seguro que deseas eliminar esta publicación?")) return;

  const res = await fetch(`${URL_BASE}/api/publicaciones/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });

  if (res.ok) {
    alert("Publicación eliminada.");
    cargarMisPublicaciones();
  } else {
    alert("Error al eliminar.");
  }
}

async function editarPublicacion(id) {
  const nuevoTitulo = prompt("Nuevo título:");
  const nuevaDescripcion = prompt("Nueva descripción:");
  const nuevaCategoria = prompt("Nueva categoría:");
  const nuevaDisponibilidad = prompt("Nueva disponibilidad:");

  const res = await fetch(`${URL_BASE}/api/publicaciones/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      titulo: nuevoTitulo,
      descripcion: nuevaDescripcion,
      categoria: nuevaCategoria,
      disponibilidad: nuevaDisponibilidad
    })
  });

  if (res.ok) {
    alert("Publicación actualizada.");
    cargarMisPublicaciones();
  } else {
    alert("Error al actualizar.");
  }
}

async function cargarOfertasActivas() {
  const res = await fetch(`${URL_BASE}/api/ofertas-activas/${usuario_id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();

  const contenedor = document.getElementById("seccion-ofertas-activas");
  contenedor.innerHTML = "<h3>Ofertas activas</h3>";

  contenedor.innerHTML += "<h4>Solicitudes enviadas</h4>";
  if (data.enviadas.length === 0) {
    contenedor.innerHTML += "<p>No has enviado solicitudes aún.</p>";
  } else {
    data.enviadas.forEach(s => {
      contenedor.innerHTML += `
        <div class="card">
          <p><strong>Para:</strong> ${s.oferente_nombre}</p>
          <p><strong>Estado:</strong> ${estadoConIcono(s.estado)} - ${s.fecha_solicitud}</p>
        </div>
      `;
    });
  }

  contenedor.innerHTML += "<h4>Solicitudes recibidas</h4>";
  if (data.recibidas.length === 0) {
    contenedor.innerHTML += "<p>No has recibido solicitudes aún.</p>";
  } else {
    data.recibidas.forEach(s => {
      let botones = "";
      if (s.estado === "pendiente") {
        botones = `
          <button onclick="responderSolicitud(${s.id}, 'aceptada')">✅ Aceptar</button>
          <button onclick="responderSolicitud(${s.id}, 'rechazada')">❌ Rechazar</button>
        `;
      }

      contenedor.innerHTML += `
        <div class="card">
          <p><strong>De:</strong> ${s.solicitante_nombre}</p>
          <p><strong>Estado:</strong> ${estadoConIcono(s.estado)} - ${s.fecha_solicitud}</p>
          ${botones}
        </div>
      `;
    });
  }
}

//a yuda visual para el estado
function estadoConIcono(estado) {
  switch (estado) {
    case "pendiente": return "Pendiente";
    case "aceptada": return "Aceptada";
    case "rechazada": return "Rechazada";
    default: return estado;
  }
}


async function responderSolicitud(id, estado) {
  const res = await fetch(`${URL_BASE}/api/solicitudes/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ estado })
  });

  if (res.ok) {
    alert(`Solicitud ${estado}.`);
    cargarOfertasActivas();
  } else {
    alert("Error al actualizar solicitud.");
  }
}


async function cargarHistorial() {
  const res = await fetch(`${URL_BASE}/api/historial/${usuario_id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();

  const contenedor = document.getElementById("seccion-historial-intercambios");
  contenedor.innerHTML = "<h3>Historial de Intercambios</h3>";

  if (data.length === 0) {
    contenedor.innerHTML += "<p>No tienes intercambios aceptados aún.</p>";
    return;
  }

  data.forEach(s => {
    let calificacionHTML = "";
    if (s.ya_calificado) {
      calificacionHTML = `<p>⭐ ${s.valoracion} - ${s.comentario}</p>`;
    } else {
      calificacionHTML = ``;
    }


    contenedor.innerHTML += `
      <div class="card">
        <p><strong>Con:</strong> ${s.otro_usuario_nombre}</p>
        <p><strong>Publicación:</strong> ${s.titulo}</p>
        <p><em>${s.fecha_solicitud}</em></p>
        ${calificacionHTML}
      </div>
    `;
  });
}

async function calificarIntercambio(solicitud_id, calificado_id) {
  const valoracion = prompt("Calificación (1 a 5 estrellas):");
  const comentario = prompt("Comentario:");

  if (!valoracion || !comentario) {
    alert("Debes completar ambos campos.");
    return;
  }

  const res = await fetch(`${URL_BASE}/api/calificaciones`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      solicitud_id,
      calificado_id,
      valoracion: parseInt(valoracion),
      comentario
    })
  });

  const data = await res.json();
  if (res.ok) {
    alert("Calificación enviada.");
    cargarHistorial();
  } else {
    alert(data.error || "Error al calificar.");
  }
}


window.verPerfilUsuario = verPerfilUsuario;
