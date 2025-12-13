"""
Configuration Management

Handles loading and managing QALDRON configuration from YAML files
and environment variables.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict


class Config:
    """
    Configuration manager for QALDRON
    
    Loads configuration from YAML file and allows environment variable overrides.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config.yaml file. If None, searches standard locations.
        """
        if config_path is None:
            config_path = self._find_config_file()
        
        self.config_path = config_path
        self.config = self._load_config()
        self._apply_env_overrides()
    
    def _find_config_file(self) -> str:
        """Find config.yaml in standard locations"""
        search_paths = [
            Path(__file__).parent / "config.yaml",
            Path.cwd() / "config.yaml",
            Path.cwd() / "qaldron" / "config" / "config.yaml",
            Path("/etc/qaldron/config.yaml"),
        ]
        
        for path in search_paths:
            if path.exists():
                return str(path)
        
        # Return default location if not found
        return str(Path(__file__).parent / "config.yaml")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found at {self.config_path}, using defaults")
            return self._get_defaults()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "layer1": {
                "n_qubits": 12,
                "layers": 4,
                "authentication_key": "OrthogonalKey_2025"
            },
            "layer2": {
                "entropy_rotation_interval": 300,
                "message_timeout": 60,
                "max_message_size": 1048576,
                "default_encryption": True
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8080,
                "enable_https": False
            },
            "logging": {
                "level": "INFO",
                "format": "json"
            }
        }
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides"""
        # Layer 1 overrides
        if os.getenv("QALDRON_AUTH_KEY"):
            self.config["layer1"]["authentication_key"] = os.getenv("QALDRON_AUTH_KEY")
        
        # API overrides
        if os.getenv("QALDRON_API_HOST"):
            self.config["api"]["host"] = os.getenv("QALDRON_API_HOST")
        
        if os.getenv("QALDRON_API_PORT"):
            self.config["api"]["port"] = int(os.getenv("QALDRON_API_PORT"))
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Configuration key path (e.g., "layer1.n_qubits")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_layer1_config(self) -> Dict[str, Any]:
        """Get Layer 1 configuration"""
        return self.config.get("layer1", {})
    
    def get_layer2_config(self) -> Dict[str, Any]:
        """Get Layer 2 configuration"""
        return self.config.get("layer2", {})
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return self.config.get("api", {})


# Global configuration instance
_config = None


def get_config(config_path: str = None) -> Config:
    """
    Get global configuration instance
    
    Args:
        config_path: Path to config file (only used on first call)
        
    Returns:
        Config: Global configuration instance
    """
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


__all__ = ["Config", "get_config"]
