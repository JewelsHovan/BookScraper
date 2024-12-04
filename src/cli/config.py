from pathlib import Path
import yaml
from typing import Any, Dict, Optional

DEFAULT_CONFIG = {
    'output_dir': '~/novels',
    'max_workers': 5,
    'default_format': 'html',
    'cache_ttl': 3600,
    'sites': {
        'novelfull': {
            'enabled': True,
            'rate_limit': 1
        },
        'novelusb': {
            'enabled': True,
            'rate_limit': 2
        }
    },
    'progress_bar': True,
    'color_output': True,
    'verbose': False
}

class Config:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'bookscraper'
        self.config_file = self.config_dir / 'config.yaml'
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if not self.config_file.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self._save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        
        with open(self.config_file) as f:
            return yaml.safe_load(f)
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            yaml.safe_dump(config, f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
        self._save_config(self.config)
    
    def get_output_dir(self) -> Path:
        """Get output directory as Path object."""
        output_dir = self.get('output_dir', '~/novels')
        return Path(output_dir).expanduser()
