"""
Gestor de imágenes Docker para Terratest.
Verifica y construye la imagen de Terraform si no existe.
"""
import docker
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ImageManager:
    """Gestiona la imagen Docker de Terraform."""
    
    def __init__(self, image_name: str = "terratest/terraform:latest"):
        self.client = docker.from_env()
        self.image_name = image_name
    
    def check_image_exists(self) -> bool:
        """Verifica si la imagen existe localmente."""
        try:
            self.client.images.get(self.image_name)
            return True
        except docker.errors.ImageNotFound:
            return False
        except Exception as e:
            logger.error(f"Error al verificar imagen: {e}")
            return False
    
    def list_all_images(self) -> list[Dict[str, Any]]:
        """Lista todas las imágenes Docker disponibles localmente."""
        try:
            images = self.client.images.list()
            result = []
            
            for image in images:
                # Obtener tags (nombres) de la imagen
                tags = image.tags if image.tags else ["<none>:<none>"]
                
                for tag in tags:
                    result.append({
                        "id": image.short_id.replace('sha256:', ''),
                        "tag": tag,
                        "created": image.attrs.get('Created', 'Unknown'),
                        "size_mb": round(image.attrs.get('Size', 0) / (1024 * 1024), 2)
                    })
            
            # Ordenar por fecha de creación (más reciente primero)
            result.sort(key=lambda x: x['created'], reverse=True)
            
            return result
        except Exception as e:
            logger.error(f"Error al listar imágenes: {e}")
            return []
    
    def get_dockerfile_path(self) -> Optional[Path]:
        """Obtiene la ruta al Dockerfile."""
        # Desde terratest/core/image_manager.py subir a terratest/ y luego a docker/
        current_file = Path(__file__)
        terratest_root = current_file.parent.parent
        dockerfile = terratest_root.parent / "docker" / "Dockerfile.terraform"
        
        if dockerfile.exists():
            return dockerfile
        
        # Intentar buscar en otras ubicaciones comunes
        alternatives = [
            Path.cwd() / "docker" / "Dockerfile.terraform",
            Path.cwd() / "Dockerfile.terraform",
        ]
        
        for alt in alternatives:
            if alt.exists():
                return alt
        
        return None
    
    def build_image(self, dockerfile_path: Optional[Path] = None, dockerfile_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Construye la imagen Docker.
        
        Args:
            dockerfile_path: Ruta al Dockerfile (opcional)
            dockerfile_content: Contenido del Dockerfile como string (opcional)
        
        Returns:
            Dict con status, message, y logs de la construcción
        """
        try:
            build_logs = []
            
            # Si se proporciona contenido directamente, usarlo
            if dockerfile_content:
                logger.info(f"Construyendo imagen {self.image_name} desde contenido proporcionado...")
                
                import io
                import tarfile
                
                # Crear un contexto tar en memoria con el Dockerfile
                tar_stream = io.BytesIO()
                tar = tarfile.open(fileobj=tar_stream, mode='w')
                
                # Agregar el Dockerfile al tar
                dockerfile_data = dockerfile_content.encode('utf-8')
                tarinfo = tarfile.TarInfo(name='Dockerfile')
                tarinfo.size = len(dockerfile_data)
                tar.addfile(tarinfo, io.BytesIO(dockerfile_data))
                tar.close()
                
                # Volver al inicio del stream
                tar_stream.seek(0)
                
                image, logs = self.client.images.build(
                    fileobj=tar_stream,
                    tag=self.image_name,
                    rm=True,
                    forcerm=True,
                    custom_context=True,
                )
            
            # Si no hay contenido, buscar archivo
            else:
                if dockerfile_path is None:
                    dockerfile_path = self.get_dockerfile_path()
                
                if dockerfile_path is None or not dockerfile_path.exists():
                    # Proporcionar Dockerfile por defecto
                    default_dockerfile = """FROM hashicorp/terraform:latest

# Instalar herramientas adicionales
RUN apk add --no-cache git openssh-client

# Configurar SSH
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

WORKDIR /workspace
"""
                    logger.info(f"No se encontró Dockerfile, usando configuración por defecto...")
                    
                    import io
                    import tarfile
                    
                    # Crear contexto tar con Dockerfile por defecto
                    tar_stream = io.BytesIO()
                    tar = tarfile.open(fileobj=tar_stream, mode='w')
                    
                    dockerfile_data = default_dockerfile.encode('utf-8')
                    tarinfo = tarfile.TarInfo(name='Dockerfile')
                    tarinfo.size = len(dockerfile_data)
                    tar.addfile(tarinfo, io.BytesIO(dockerfile_data))
                    tar.close()
                    
                    tar_stream.seek(0)
                    
                    image, logs = self.client.images.build(
                        fileobj=tar_stream,
                        tag=self.image_name,
                        rm=True,
                        forcerm=True,
                        custom_context=True,
                    )
                else:
                    # Usar archivo encontrado
                    context_path = dockerfile_path.parent.parent
                    dockerfile_rel = dockerfile_path.relative_to(context_path)
                    dockerfile_rel_str = str(dockerfile_rel).replace('\\', '/')
                    
                    logger.info(f"Construyendo imagen {self.image_name}...")
                    logger.info(f"Context: {context_path}")
                    logger.info(f"Dockerfile: {dockerfile_rel_str}")
                    
                    image, logs = self.client.images.build(
                        path=str(context_path),
                        dockerfile=dockerfile_rel_str,
                        tag=self.image_name,
                        rm=True,
                        forcerm=True,
                    )
            
            # Capturar logs
            for chunk in logs:
                if 'stream' in chunk:
                    log_line = chunk['stream'].strip()
                    if log_line:
                        build_logs.append(log_line)
                        logger.info(log_line)
                elif 'error' in chunk:
                    error_msg = chunk['error'].strip()
                    build_logs.append(f"ERROR: {error_msg}")
                    logger.error(error_msg)
            
            return {
                "status": "success",
                "message": f"Imagen {self.image_name} construida exitosamente",
                "image_id": image.id,
                "logs": build_logs
            }
            
        except docker.errors.BuildError as e:
            logger.error(f"Error al construir imagen: {e}")
            return {
                "status": "error",
                "message": f"Error al construir imagen: {str(e)}",
                "logs": [str(e)]
            }
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return {
                "status": "error",
                "message": f"Error inesperado: {str(e)}",
                "logs": [str(e)]
            }
    
    def get_image_info(self) -> Optional[Dict[str, Any]]:
        """Obtiene información de la imagen si existe."""
        try:
            image = self.client.images.get(self.image_name)
            return {
                "id": image.id,
                "short_id": image.short_id,
                "tags": image.tags,
                "created": image.attrs.get('Created', 'Unknown'),
                "size": image.attrs.get('Size', 0),
                "size_mb": round(image.attrs.get('Size', 0) / (1024 * 1024), 2)
            }
        except docker.errors.ImageNotFound:
            return None
        except Exception as e:
            logger.error(f"Error al obtener info de imagen: {e}")
            return None
    
    def remove_image(self, force: bool = False) -> Dict[str, Any]:
        """Elimina la imagen Docker."""
        try:
            self.client.images.remove(self.image_name, force=force)
            return {
                "status": "success",
                "message": f"Imagen {self.image_name} eliminada"
            }
        except docker.errors.ImageNotFound:
            return {
                "status": "error",
                "message": "Imagen no encontrada"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al eliminar imagen: {str(e)}"
            }
