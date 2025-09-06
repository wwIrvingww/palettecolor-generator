# 🎨 PaletteColor Generator MCP

Este proyecto implementa un **servidor MCP (Model Context Protocol)** sencillo que genera paletas de color a partir de un color base y un modo de combinación cromática.

## 🚀 Funcionalidad

El servidor expone dos herramientas principales:

* **remote\_hello**: responde con un saludo de prueba.
* **palette\_generator**: recibe un color base en HEX y un tipo de paleta, devolviendo una lista de colores calculados.

### Modos soportados

* `complementary` → Color opuesto en el círculo cromático.
* `analogous` → Colores cercanos al tono base.
* `triadic` → Tres colores espaciados a 120°.
* `split_complementary` → Opuesto ±30°.
* `tetradic` → Dos pares de colores complementarios.

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/palettecolor-generator.git
cd palettecolor-generator

# Crear entorno virtual (opcional)
python -m venv .venv
.venv\Scripts\activate  # En Windows
source .venv/bin/activate  # En Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Uso

### 1. Levantar el servidor

```bash
python server.py
```

El servidor quedará en `http://127.0.0.1:8000/`.

### 2. Listar herramientas disponibles

```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/tools"
```

### 3. Probar **remote\_hello**

```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/mcp/run" -Method Post -ContentType "application/json" -Body '{"tool":"remote_hello","input":{"name":"Irving"}}'
```

### 4. Probar **palette\_generator**

```bash
Invoke-RestMethod -Uri "http://127.0.0.1:8000/mcp/run" -Method Post -ContentType "application/json" -Body '{"tool":"palette_generator","input":{"base_color":"#3498db","mode":"triadic"}}'
```

Respuesta esperada (ejemplo):

```json
{"palette": ["#3498DB", "#DB3498", "#98DB34"]}
```

## 📑 Licencia

MIT
