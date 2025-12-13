import json
from pathlib import Path
from typing import Optional, Literal

ConfigType = Literal["project", "global", "custom"]


class OkoConfig:
    def __init__(self):
        self.config_type: Optional[ConfigType] = None
        self.config_dir: Optional[Path] = None
        self.config_file: Optional[Path] = None
        self.endpoints_file: Optional[Path] = None

    def find_config(self) -> bool:
        """
        Buscar configuración jerárquicamente:
        1. Directorio actual o padres (.oko/)
        2. Global (~/.oko/)
        3. Si no existe, retornar False
        """
        # Buscar .oko/ en directorio actual o padres
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            oko_dir = parent / ".oko"
            if oko_dir.exists() and (oko_dir / "config.json").exists():
                self.config_type = "project"
                self.config_dir = oko_dir
                self.config_file = oko_dir / "config.json"
                self.endpoints_file = oko_dir / "endpoints.json"
                return True

        # Buscar global
        global_dir = Path.home() / ".oko"
        if global_dir.exists() and (global_dir / "config.json").exists():
            self.config_type = "global"
            self.config_dir = global_dir
            self.config_file = global_dir / "config.json"
            self.endpoints_file = global_dir / "endpoints.json"
            return True

        return False

    def load_config(self):
        """Cargar configuración si existe"""
        if self.config_file and self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if not content.strip():
                        return {"version": "1.0", "type": self.config_type or "unknown"}
                    return json.loads(content)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {"version": "1.0", "type": self.config_type or "unknown"}

    def save_config(self, config_type: ConfigType, config_dir: Path, data: dict = None):
        """Guardar nueva configuración"""
        self.config_type = config_type
        self.config_dir = config_dir
        self.config_file = config_dir / "config.json"
        self.endpoints_file = config_dir / "endpoints.json"

        # Crear directorio
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Guardar config
        config_data = {
            "version": "1.0",
            "type": config_type,
            "created_at": data.get("created_at") if data else None,
            "project_name": data.get("project_name") if data else None,
        }

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)

        # Crear endpoints.json vacío si no existe
        if not self.endpoints_file.exists():
            with open(self.endpoints_file, "w", encoding="utf-8") as f:
                json.dump({"endpoints": {}}, f, indent=2)

    def get_endpoints_file(self) -> Path:
        """Obtener archivo de endpoints (con fallback)"""
        if self.endpoints_file and self.endpoints_file.exists():
            return self.endpoints_file

        # Si no hay config, usar global como fallback
        if not self.find_config():
            global_dir = Path.home() / ".oko"
            global_dir.mkdir(parents=True, exist_ok=True)
            return global_dir / "endpoints.json"

        return self.endpoints_file


# Instancia global
config = OkoConfig()


def ensure_config():
    """Versión simple para compatibilidad"""
    return config.get_endpoints_file().parent.mkdir(parents=True, exist_ok=True)


def load_endpoints():
    """Cargar endpoints desde la ubicación activa"""
    endpoints_file = config.get_endpoints_file()

    try:
        if endpoints_file.exists():
            with open(endpoints_file, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    return {"endpoints": {}}
                return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[yellow]⚠ Error loading endpoints: {e}. Creating new.[/yellow]")

    # Crear nuevo si hay error
    with open(endpoints_file, "w", encoding="utf-8") as f:
        json.dump({"endpoints": {}}, f, indent=2)
    return {"endpoints": {}}


def save_endpoints(data: dict):
    """Guardar endpoints en la ubicación activa"""
    endpoints_file = config.get_endpoints_file()
    endpoints_file.parent.mkdir(parents=True, exist_ok=True)

    with open(endpoints_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
