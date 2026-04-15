"""
app.py — Lógica Central de la Plataforma de Servicios
======================================================
Autor: Generado con arquitectura Flask + SQLite
Objetivo Educativo: Curso de Sistemas y Gestión de Data

Este archivo es el "cerebro" de la aplicación:
- Define las RUTAS (URLs) que el usuario puede visitar
- Contiene la LÓGICA para leer y escribir en la base de datos
- Maneja la SUBIDA de imágenes de forma segura
"""

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

# ─────────────────────────────────────────────
# CONFIGURACIÓN INICIAL DE LA APLICACIÓN
# ─────────────────────────────────────────────

app = Flask(__name__)

# Clave secreta para que Flask pueda enviar mensajes flash (alertas)
app.secret_key = "clave_super_secreta_cambiar_en_produccion"

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
# Esta llave cifra la información de la sesión. ¡No la compartas!
app.secret_key = 'nexus_ultra_secret_key_2026'

# Ruta donde se guardarán las imágenes subidas por el administrador
UPLOAD_FOLDER = os.path.join("static", "uploads")

# Solo permitimos subir estos tipos de archivo (seguridad básica)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

# Imagen por defecto si el admin no sube ninguna
DEFAULT_IMAGE = "/static/img/default.svg"

# Nombre del archivo de la base de datos SQLite
DATABASE = "servicios.db"

# Creamos el directorio de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join("static", "img"), exist_ok=True)

# ─────────────────────────────────────────────
# FUNCIONES AUXILIARES (HELPERS)
# ─────────────────────────────────────────────

def get_db_connection():
    """
    Abre una conexión a la base de datos SQLite.
    
    ¿Por qué row_factory? Permite acceder a las columnas por nombre
    (ej: fila['nombre']) en vez de por índice (fila[1]).
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Acceso por nombre de columna
    return conn


def init_db():
    """
    Crea la tabla 'servicios' si no existe.
    
    Se ejecuta UNA SOLA VEZ al iniciar la app.
    Si la tabla ya existe, SQLite la ignora (IF NOT EXISTS).
    
    Columnas:
    - id: Número único auto-incremental (clave primaria)
    - nombre: Texto obligatorio (NOT NULL)
    - precio: Número decimal obligatorio
    - descripcion: Texto opcional (puede ser NULL)
    - imagen_url: Ruta de la imagen (tiene valor por defecto)
    - estado: 1 = activo/visible, 0 = inactivo/oculto
    """
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT    NOT NULL,
            precio      REAL    NOT NULL,
            descripcion TEXT,
            imagen_url  TEXT    DEFAULT '/static/img/default.jpg',
            estado      INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()


def allowed_file(filename):
    """
    Verifica que el archivo tenga una extensión permitida.
    
    Ejemplo: 'foto.jpg' → True | 'virus.exe' → False
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_uploaded_image(file_obj):
    """
    Guarda una imagen subida de forma SEGURA y devuelve su URL.
    
    ¿Por qué UUID? Para generar nombres de archivo únicos y evitar
    que alguien sobreescriba archivos existentes con el mismo nombre.
    
    Ejemplo de resultado: '/static/uploads/a3f9c1b2-foto.jpg'
    """
    if file_obj and file_obj.filename and allowed_file(file_obj.filename):
        # Obtenemos la extensión original (.jpg, .png, etc.)
        extension = file_obj.filename.rsplit(".", 1)[1].lower()
        
        # Creamos un nombre único usando UUID (identificador universal)
        unique_name = f"{uuid.uuid4().hex}.{extension}"
        
        # Construimos la ruta completa donde se guardará en el servidor
        save_path = os.path.join(UPLOAD_FOLDER, unique_name)
        
        # Guardamos el archivo en el disco
        file_obj.save(save_path)
        
        # Devolvemos la URL pública del archivo
        return f"/static/uploads/{unique_name}"
    
    # Si no se subió imagen, devolvemos la imagen por defecto
    return DEFAULT_IMAGE


# ─────────────────────────────────────────────
# RUTAS PÚBLICAS
# ─────────────────────────────────────────────
"""
@app.route("/")
def index():
    
    Página principal — Catálogo público de servicios.
    
    Solo muestra servicios con estado = 1 (activos).
    El cliente (visitante) no puede ver los servicios desactivados.
    
    conn = get_db_connection()
    
    # Consulta SQL: traer solo los servicios activos, ordenados por nombre
    servicios = conn.execute(
        "SELECT * FROM servicios WHERE estado = 1 ORDER BY nombre ASC"
    ).fetchall()
    
    conn.close()
    
    # Enviamos los datos a la plantilla HTML
    return render_template("index.html", servicios=servicios)
"""

@app.route("/")
def index():
    conn = get_db_connection()
    servicios = conn.execute(
        "SELECT * FROM servicios WHERE estado = 1 ORDER BY nombre ASC"
    ).fetchall()
    conn.close()
    
    # Esta es la línea que debes dejar activa:
    return render_template("index.html", servicios=servicios)

# ─────────────────────────────────────────────
# RUTAS DEL PANEL ADMINISTRADOR
# ─────────────────────────────────────────────

@app.route("/admin")
def admin_dashboard():
    """
    Dashboard del administrador.
    
    Muestra TODOS los servicios (activos e inactivos)
    para que el admin pueda gestionarlos.
    
    NOTA: En producción real, esta ruta necesitaría
    autenticación (login). Por ahora es un prototipo.
    """
    conn = get_db_connection()
    servicios = conn.execute(
        "SELECT * FROM servicios ORDER BY id DESC"
    ).fetchall()
    conn.close()
    
    return render_template("admin/dashboard.html", servicios=servicios)


@app.route("/admin/nuevo", methods=["GET", "POST"])
def admin_nuevo():
    """
    Formulario para CREAR un nuevo servicio.
    
    GET  → Muestra el formulario vacío
    POST → Procesa los datos del formulario y guarda en DB
    """
    if request.method == "POST":
        # ── Paso 1: Leer los datos del formulario ──
        nombre      = request.form.get("nombre", "").strip()
        precio_raw  = request.form.get("precio", "0").strip()
        descripcion = request.form.get("descripcion", "").strip() or None
        estado      = 1 if request.form.get("estado") == "on" else 0
        imagen_file = request.files.get("imagen")
        
        # ── Paso 2: Validación básica ──
        errores = []
        if not nombre:
            errores.append("El nombre del servicio es obligatorio.")
        
        try:
            precio = float(precio_raw)
            if precio < 0:
                errores.append("El precio no puede ser negativo.")
        except ValueError:
            errores.append("El precio debe ser un número válido.")
            precio = 0.0
        
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("admin/form_servicio.html", servicio=None, accion="nuevo")
        
        # ── Paso 3: Manejar imagen ──
        imagen_url = save_uploaded_image(imagen_file)
        
        # ── Paso 4: Insertar en la base de datos ──
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO servicios (nombre, precio, descripcion, imagen_url, estado)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, precio, descripcion, imagen_url, estado)
        )
        conn.commit()
        conn.close()
        
        flash(f"✅ Servicio '{nombre}' creado exitosamente.", "success")
        return redirect(url_for("admin_dashboard"))
    
    # GET: mostrar formulario vacío
    return render_template("admin/form_servicio.html", servicio=None, accion="nuevo")


@app.route("/admin/editar/<int:servicio_id>", methods=["GET", "POST"])
def admin_editar(servicio_id):
    """
    Formulario para EDITAR un servicio existente.
    
    <int:servicio_id> → Flask convierte automáticamente el parámetro a entero.
    """
    conn = get_db_connection()
    servicio = conn.execute(
        "SELECT * FROM servicios WHERE id = ?", (servicio_id,)
    ).fetchone()
    conn.close()
    
    # Si el ID no existe en la DB, redirigimos al dashboard
    if servicio is None:
        flash("❌ Servicio no encontrado.", "error")
        return redirect(url_for("admin_dashboard"))
    
    if request.method == "POST":
        nombre      = request.form.get("nombre", "").strip()
        precio_raw  = request.form.get("precio", "0").strip()
        descripcion = request.form.get("descripcion", "").strip() or None
        estado      = 1 if request.form.get("estado") == "on" else 0
        imagen_file = request.files.get("imagen")
        
        errores = []
        if not nombre:
            errores.append("El nombre es obligatorio.")
        
        try:
            precio = float(precio_raw)
            if precio < 0:
                errores.append("El precio no puede ser negativo.")
        except ValueError:
            errores.append("Precio inválido.")
            precio = 0.0
        
        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("admin/form_servicio.html", servicio=servicio, accion="editar")
        
        # Si se subió nueva imagen, la usamos; si no, conservamos la anterior
        if imagen_file and imagen_file.filename:
            imagen_url = save_uploaded_image(imagen_file)
        else:
            imagen_url = servicio["imagen_url"]  # Mantener imagen actual
        
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE servicios
            SET nombre=?, precio=?, descripcion=?, imagen_url=?, estado=?
            WHERE id=?
            """,
            (nombre, precio, descripcion, imagen_url, estado, servicio_id)
        )
        conn.commit()
        conn.close()
        
        flash(f"✅ Servicio '{nombre}' actualizado.", "success")
        return redirect(url_for("admin_dashboard"))
    
    # GET: mostrar formulario con datos actuales
    return render_template("admin/form_servicio.html", servicio=servicio, accion="editar")


@app.route("/admin/eliminar/<int:servicio_id>", methods=["POST"])
def admin_eliminar(servicio_id):
    """
    Elimina un servicio de la base de datos.
    
    Solo acepta POST (no GET) para evitar eliminaciones accidentales
    si alguien visita la URL directamente.
    """
    conn = get_db_connection()
    servicio = conn.execute(
        "SELECT nombre FROM servicios WHERE id = ?", (servicio_id,)
    ).fetchone()
    
    if servicio:
        conn.execute("DELETE FROM servicios WHERE id = ?", (servicio_id,))
        conn.commit()
        flash(f"🗑️ Servicio '{servicio['nombre']}' eliminado.", "success")
    else:
        flash("❌ Servicio no encontrado.", "error")
    
    conn.close()
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/toggle/<int:servicio_id>", methods=["POST"])
def admin_toggle_estado(servicio_id):
    """
    Activa o desactiva un servicio (cambia estado 0↔1).
    
    Útil para ocultar/mostrar servicios temporalmente
    sin necesidad de eliminarlos.
    """
    conn = get_db_connection()
    servicio = conn.execute(
        "SELECT id, nombre, estado FROM servicios WHERE id = ?", (servicio_id,)
    ).fetchone()
    
    if servicio:
        nuevo_estado = 0 if servicio["estado"] == 1 else 1
        conn.execute(
            "UPDATE servicios SET estado = ? WHERE id = ?",
            (nuevo_estado, servicio_id)
        )
        conn.commit()
        estado_texto = "activado" if nuevo_estado == 1 else "desactivado"
        flash(f"🔄 Servicio '{servicio['nombre']}' {estado_texto}.", "success")
    
    conn.close()
    return redirect(url_for("admin_dashboard"))


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Mantenemos la inicialización de la DB
    init_db()
    
    # CAMBIO: Solo cambiamos el 5000 por el 5050 para forzar una nueva conexión
    app.run(debug=True, host="0.0.0.0", port=5050)