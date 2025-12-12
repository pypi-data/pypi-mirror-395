# 🚀 Terratest Web UI

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-beta-orange.svg)

**Terratest Web UI** es una interfaz web moderna y minimalista para ejecutar y gestionar tests de Terraform en contenedores Docker efímeros. Proporciona una experiencia visual intuitiva para desarrolladores que necesitan probar infraestructura como código de forma aislada y reproducible.

## ✨ Características

- 🎨 **Interfaz moderna** con diseño dark minimalista
- 🐳 **Ejecución en Docker** - Contenedores efímeros para cada test
- 📊 **Visualización de resultados** - Vista JSON raw + resumen visual
- 🔐 **Soporte para credenciales** - SSH, Terraform Cloud, AWS
- 📁 **Gestión de jobs** - Historial, navegación de archivos, logs con colores
- 🖼️ **Gestión de imágenes Docker** - Construir, seleccionar y eliminar imágenes
- ⚡ **API REST** con FastAPI para integración
- 🎯 **Modales personalizados** - Confirmaciones elegantes sin alerts nativos

## 📦 Instalación

### Desde PyPI (cuando se publique)

```bash
pip install terratest
```

### Desde código fuente

```bash
git clone https://github.com/yourusername/terratest.git
cd terratest
pip install -e .
```

### Con Poetry

```bash
poetry add terratest
```

## 🚀 Uso Rápido

### Iniciar Web UI

```bash
terratest web
```

Abre tu navegador en `http://localhost:8765`

### CLI

```bash
# Ejecutar un módulo de Terraform
terratest run ./examples/basic

# Ver ayuda
terratest --help
```

## 🐳 Requisitos

- Python 3.12+
- Docker instalado y corriendo
- (Opcional) Poetry para desarrollo

## 📖 Configuración

### SSH para Repositorios Privados

1. Click en el icono de configuración ⚙️
2. Habilita "Autenticación SSH"
3. Especifica el path a tus claves SSH (opcional, usa `~/.ssh` por defecto)

### Terraform Cloud

1. Abre configuración
2. Ingresa tu Token de Terraform Cloud
3. Especifica Organización y Workspace

### AWS Credentials

1. Abre configuración
2. Ingresa Access Key ID y Secret Access Key
3. (Opcional) Session Token para credenciales temporales

## 🏗️ Estructura del Proyecto

```
terratest/
├── terratest/
│   ├── cli/           # Comandos CLI
│   ├── core/          # Lógica de negocio
│   ├── web/           # Web UI
│   │   ├── static/    # HTML, CSS, JS
│   │   └── routes/    # API endpoints
│   ├── utils/         # Utilidades
│   └── models/        # Modelos de datos
├── docker/            # Dockerfiles
├── examples/          # Ejemplos de Terraform
└── tests/             # Tests unitarios
```

## 🎨 Capturas

### Dashboard Principal
- Lista de jobs ejecutados ordenados por fecha
- Botones para ejecutar, eliminar y refrescar
- Indicador de estado de imagen Docker

### Visualización de Resultados
- Split view: JSON raw a la izquierda, resumen visual a la derecha
- Plan summary con contadores (add/change/destroy)
- Lista de recursos con tipos y acciones
- Outputs de Terraform

### Navegación de Archivos
- Breadcrumb navigation
- Visor de logs con colores (errores en rojo, warnings en naranja)
- Limpieza automática de códigos ANSI

## 🛠️ Desarrollo

### Setup

```bash
# Clonar repositorio
git clone https://github.com/yourusername/terratest.git
cd terratest

# Instalar dependencias
poetry install

# Activar entorno virtual
poetry shell

# Correr en modo desarrollo
poetry run terratest web
```

### Construir Imagen Docker

```bash
docker build -t terratest/terraform:latest -f docker/Dockerfile.terraform .
```

### Tests

```bash
pytest tests/
```

## 📝 Roadmap

- [ ] Publicar en PyPI
- [ ] Tests de integración completos
- [ ] Soporte para múltiples versiones de Terraform
- [ ] Webhooks para notificaciones
- [ ] Exportar resultados a PDF/HTML
- [ ] Integración con CI/CD
- [ ] Soporte para providers adicionales (Azure, GCP)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

## 👤 Autor

**Yorlin**

## 🙏 Agradecimientos

- FastAPI por el framework web
- Typer por la CLI
- Docker SDK for Python
- Font Awesome por los iconos