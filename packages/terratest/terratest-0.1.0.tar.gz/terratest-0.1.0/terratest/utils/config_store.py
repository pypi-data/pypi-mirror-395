"""
Sistema de persistencia temporal para configuraciones de Terratest.
Las configuraciones se guardan mientras el servicio está activo.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigStore:
    """Almacena configuración temporal mientras el servicio está activo."""
    
    def __init__(self, store_path: Optional[Path] = None):
        if store_path is None:
            store_path = Path.home() / ".terratest" / "temp_config.json"
        
        self.store_path = store_path
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file()
    
    def _ensure_file(self):
        """Crea el archivo si no existe."""
        if not self.store_path.exists():
            self.save({})
    
    def load(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo."""
        try:
            with open(self.store_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def save(self, config: Dict[str, Any]):
        """Guarda la configuración en el archivo."""
        config['_updated_at'] = datetime.utcnow().isoformat() + 'Z'
        with open(self.store_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor específico de la configuración."""
        config = self.load()
        return config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Establece un valor específico en la configuración."""
        config = self.load()
        config[key] = value
        self.save(config)
    
    def update(self, updates: Dict[str, Any]):
        """Actualiza múltiples valores a la vez."""
        config = self.load()
        config.update(updates)
        self.save(config)
    
    def delete(self, key: str):
        """Elimina un valor específico."""
        config = self.load()
        if key in config:
            del config[key]
            self.save(config)
    
    def clear(self):
        """Limpia toda la configuración."""
        self.save({})
    
    def cleanup(self):
        """Elimina el archivo de configuración temporal."""
        if self.store_path.exists():
            self.store_path.unlink()


# Instancia global del store
_config_store: Optional[ConfigStore] = None


def get_config_store() -> ConfigStore:
    """Obtiene la instancia global del config store."""
    global _config_store
    if _config_store is None:
        _config_store = ConfigStore()
    return _config_store
