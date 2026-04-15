# NEXUS.services — Plataforma de Gestión de Servicios
## Proyecto Educativo: Sistemas y Gestión de Data

---

## 🗂 Estructura de Archivos

```
flask_app/
│
├── app.py                          # Lógica central Flask + rutas
├── requirements.txt                # Dependencias Python
├── servicios.db                    # Base de datos SQLite (se crea al iniciar)
│
├── static/
│   ├── css/
│   │   └── master.css              # Estilos "Premium Tech" con variables CSS
│   ├── img/
│   │   └── default.svg             # Imagen por defecto si no se sube ninguna
│   └── uploads/                    # Imágenes subidas por el administrador
│
└── templates/
    ├── layout.html                 # Master Layout (padre de todas las páginas)
    ├── index.html                  # Catálogo público (solo servicios activos)
    └── admin/
        ├── dashboard.html          # Panel de gestión (CRUD completo)
        └── form_servicio.html      # Formulario crear/editar (reutilizable)
```

---

## ⚙️ Instalación y Ejecución

### Paso 1 — Crear entorno virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### Paso 2 — Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 3 — Ejecutar la aplicación
```bash
python app.py
```

### Paso 4 — Abrir en el navegador
- **Catálogo público:** http://localhost:5000/
- **Panel admin:**      http://localhost:5000/admin

---

## 🗄️ Esquema de Base de Datos

**Tabla: `servicios`**

| Columna     | Tipo    | Restricción | Descripción                          |
|-------------|---------|-------------|--------------------------------------|
| id          | INTEGER | PK, AUTO    | Identificador único auto-incremental |
| nombre      | TEXT    | NOT NULL    | Nombre del servicio (obligatorio)    |
| precio      | REAL    | NOT NULL    | Precio en formato decimal            |
| descripcion | TEXT    | NULL        | Descripción opcional                 |
| imagen_url  | TEXT    | DEFAULT     | Ruta imagen (/static/img/default.svg)|
| estado      | INTEGER | DEFAULT 1   | 1=activo/visible, 0=inactivo/oculto  |

---

## 🚀 Rutas de la Aplicación

| Método | Ruta                        | Función               | Descripción                     |
|--------|-----------------------------|-----------------------|---------------------------------|
| GET    | `/`                         | `index()`             | Catálogo público (estado=1)     |
| GET    | `/admin`                    | `admin_dashboard()`   | Panel de gestión                |
| GET/POST | `/admin/nuevo`            | `admin_nuevo()`       | Crear nuevo servicio            |
| GET/POST | `/admin/editar/<id>`      | `admin_editar()`      | Editar servicio existente       |
| POST   | `/admin/eliminar/<id>`      | `admin_eliminar()`    | Eliminar servicio               |
| POST   | `/admin/toggle/<id>`        | `admin_toggle_estado()` | Activar/Desactivar servicio   |

---

## 🔐 Notas de Seguridad (para Producción)

1. **Autenticación**: Agregar Flask-Login para proteger `/admin`
2. **Secret Key**: Cambiar `app.secret_key` por una clave segura aleatoria
3. **Validación de archivos**: Considerar validar el contenido MIME, no solo la extensión
4. **Variables de entorno**: Mover configuración sensible a `.env` con python-dotenv
5. **HTTPS**: Usar certificado SSL en producción

---

## 📚 Conceptos Clave Cubiertos

- **Flask**: Micro-framework web Python
- **Jinja2**: Motor de plantillas (herencia, filtros, condicionales)
- **SQLite**: Base de datos embebida (sin servidor separado)
- **CRUD**: Create, Read, Update, Delete
- **CSS Variables**: Sistema de diseño escalable
- **Responsive Design**: Grid y media queries
- **File Upload**: Manejo seguro de archivos con UUID
