from fastapi import APIRouter, HTTPException, Body
from terratest.core.image_manager import ImageManager
from terratest.constants import DEFAULT_TERRAFORM_IMAGE
from terratest.utils.config_store import get_config_store

router = APIRouter()

@router.get("/status")
def get_image_status():
    """Verifica si la imagen Docker existe y obtiene su información."""
    # Obtener imagen configurada o usar la por defecto
    config_store = get_config_store()
    selected_image = config_store.get('selected_docker_image', DEFAULT_TERRAFORM_IMAGE)
    
    manager = ImageManager(selected_image)
    
    exists = manager.check_image_exists()
    info = manager.get_image_info() if exists else None
    dockerfile_path = manager.get_dockerfile_path()
    
    return {
        "exists": exists,
        "image_name": selected_image,
        "default_image": DEFAULT_TERRAFORM_IMAGE,
        "info": info,
        "dockerfile_found": dockerfile_path is not None,
        "dockerfile_path": str(dockerfile_path) if dockerfile_path else None
    }

@router.get("/list")
def list_all_images():
    """Lista todas las imágenes Docker disponibles localmente."""
    manager = ImageManager()
    images = manager.list_all_images()
    
    # Obtener imagen seleccionada actualmente
    config_store = get_config_store()
    selected_image = config_store.get('selected_docker_image', DEFAULT_TERRAFORM_IMAGE)
    
    return {
        "images": images,
        "selected_image": selected_image,
        "default_image": DEFAULT_TERRAFORM_IMAGE
    }

@router.post("/select")
def select_image(image_name: str = Body(..., embed=True)):
    """Selecciona una imagen Docker existente para usar."""
    manager = ImageManager(image_name)
    
    # Verificar que la imagen existe
    if not manager.check_image_exists():
        raise HTTPException(status_code=404, detail=f"Imagen '{image_name}' no encontrada")
    
    # Guardar en config store
    config_store = get_config_store()
    config_store.set('selected_docker_image', image_name)
    
    return {
        "status": "success",
        "message": f"Imagen '{image_name}' seleccionada",
        "image_name": image_name
    }

@router.post("/build")
def build_image():
    """Construye la imagen Docker de Terraform."""
    manager = ImageManager(DEFAULT_TERRAFORM_IMAGE)
    
    # Verificar si ya existe
    if manager.check_image_exists():
        # Seleccionarla automáticamente
        config_store = get_config_store()
        config_store.set('selected_docker_image', DEFAULT_TERRAFORM_IMAGE)
        
        return {
            "status": "already_exists",
            "message": f"La imagen {DEFAULT_TERRAFORM_IMAGE} ya existe",
            "info": manager.get_image_info()
        }
    
    # Construir la imagen
    result = manager.build_image()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    # Seleccionarla automáticamente si se construyó exitosamente
    if result["status"] == "success":
        config_store = get_config_store()
        config_store.set('selected_docker_image', DEFAULT_TERRAFORM_IMAGE)
    
    return result

@router.post("/rebuild")
def rebuild_image(force: bool = False):
    """Reconstruye la imagen Docker (elimina y construye de nuevo)."""
    manager = ImageManager(DEFAULT_TERRAFORM_IMAGE)
    
    # Eliminar imagen existente si force=True
    if force and manager.check_image_exists():
        remove_result = manager.remove_image(force=True)
        if remove_result["status"] == "error":
            raise HTTPException(status_code=500, detail=remove_result["message"])
    
    # Construir la imagen
    result = manager.build_image()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result

@router.delete("/")
def delete_image():
    """Elimina la imagen Docker."""
    manager = ImageManager(DEFAULT_TERRAFORM_IMAGE)
    
    if not manager.check_image_exists():
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    result = manager.remove_image(force=True)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result
