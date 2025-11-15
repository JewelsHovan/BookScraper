from pathlib import Path
import yaml
from typing import Any, Dict, Optional

from src.utils.logger import setup_logger

# Initialize logger for this module
logger = setup_logger(__name__)

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
        """Load configuration from file or create default.
        
        Returns:
            Dictionary containing configuration values. Returns DEFAULT_CONFIG
            if file doesn't exist or on any error.
        """
        try:
            if not self.config_file.exists():
                logger.info(f"Config file not found at {self.config_file}, creating default configuration")
                try:
                    self.config_dir.mkdir(parents=True, exist_ok=True)
                except PermissionError as e:
                    logger.error(f"Permission denied when creating config directory {self.config_dir}: {e}")
                    logger.warning("Using default configuration in memory (changes will not be persisted)")
                    return DEFAULT_CONFIG.copy()
                except OSError as e:
                    logger.error(f"OS error when creating config directory {self.config_dir}: {e}")
                    logger.warning("Using default configuration in memory (changes will not be persisted)")
                    return DEFAULT_CONFIG.copy()
                
                # Try to save default config
                try:
                    self._save_config(DEFAULT_CONFIG)
                except (PermissionError, OSError) as e:
                    logger.error(f"Failed to save default configuration: {e}")
                    logger.warning("Using default configuration in memory (changes will not be persisted)")
                
                return DEFAULT_CONFIG.copy()
            
            # Load existing configuration file
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = yaml.safe_load(f)
                    
                    # Handle case where YAML file is empty or contains only whitespace/comments
                    if loaded_config is None:
                        logger.warning(f"Config file {self.config_file} is empty, using default configuration")
                        return DEFAULT_CONFIG.copy()
                    
                    # Validate that loaded config is a dictionary
                    if not isinstance(loaded_config, dict):
                        logger.error(f"Config file {self.config_file} does not contain a valid configuration dictionary")
                        logger.warning("Using default configuration")
                        return DEFAULT_CONFIG.copy()
                    
                    logger.info(f"Successfully loaded configuration from {self.config_file}")
                    return loaded_config
                    
            except PermissionError as e:
                logger.error(f"Permission denied when reading config file {self.config_file}: {e}")
                logger.warning("Using default configuration")
                return DEFAULT_CONFIG.copy()
                
            except OSError as e:
                logger.error(f"OS error when reading config file {self.config_file}: {e}")
                logger.warning("Using default configuration")
                return DEFAULT_CONFIG.copy()
                
            except yaml.YAMLError as e:
                logger.error(f"Invalid YAML in config file {self.config_file}: {e}")
                logger.warning("Using default configuration")
                return DEFAULT_CONFIG.copy()
                
        except Exception as e:
            # Catch-all for any unexpected errors
            logger.error(f"Unexpected error loading configuration: {e}")
            logger.warning("Using default configuration")
            return DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
            
        Raises:
            ValueError: If config is not a dictionary
            PermissionError: If unable to write to config file due to permissions
            OSError: If unable to write to config file due to OS error
            yaml.YAMLError: If unable to serialize config to YAML
        """
        # Validate input parameter
        if not isinstance(config, dict):
            raise ValueError(f"Config must be a dictionary, got {type(config).__name__}")
        
        if not config:
            logger.warning("Attempting to save empty configuration")
        
        try:
            # Ensure config directory exists
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # Write configuration to file
            with open(self.config_file, 'w') as f:
                yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)
            
            logger.debug(f"Configuration saved to {self.config_file}")
            
        except PermissionError as e:
            logger.error(f"Permission denied when saving config to {self.config_file}: {e}")
            raise
            
        except OSError as e:
            logger.error(f"OS error when saving config to {self.config_file}: {e}")
            raise
            
        except yaml.YAMLError as e:
            logger.error(f"Error serializing configuration to YAML: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key to retrieve
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value and persist to file.
        
        Args:
            key: Configuration key to set
            value: Value to set
            
        Raises:
            PermissionError: If unable to save configuration
            OSError: If unable to save configuration
        """
        self.config[key] = value
        try:
            self._save_config(self.config)
        except (PermissionError, OSError, yaml.YAMLError) as e:
            # Restore previous value on save failure
            if key in DEFAULT_CONFIG:
                self.config[key] = DEFAULT_CONFIG[key]
            else:
                self.config.pop(key, None)
            logger.error(f"Failed to persist configuration change for key '{key}': {e}")
            raise
    
    def get_output_dir(self) -> Path:
        """Get output directory as Path object, creating it if necessary.
        
        Returns:
            Path object pointing to the output directory
            
        Raises:
            PermissionError: If unable to create output directory due to permissions
            OSError: If unable to create output directory due to OS error
        """
        output_dir_str = self.get('output_dir', '~/novels')
        
        # Validate output_dir is a string
        if not isinstance(output_dir_str, str):
            logger.warning(f"Invalid output_dir type ({type(output_dir_str).__name__}), using default")
            output_dir_str = '~/novels'
        
        # Expand user path and convert to absolute path
        output_dir = Path(output_dir_str).expanduser().resolve()
        
        # Create directory if it doesn't exist
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Output directory ready: {output_dir}")
        except PermissionError as e:
            logger.error(f"Permission denied when creating output directory {output_dir}: {e}")
            raise PermissionError(f"Cannot create output directory {output_dir}: {e}") from e
        except OSError as e:
            logger.error(f"OS error when creating output directory {output_dir}: {e}")
            raise OSError(f"Cannot create output directory {output_dir}: {e}") from e
        
        return output_dir
