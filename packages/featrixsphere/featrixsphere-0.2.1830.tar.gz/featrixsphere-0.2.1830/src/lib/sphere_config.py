#!/usr/bin/env python3
"""
Sphere Configuration Management

Loads configuration from /sphere/app/config.json if it exists, otherwise uses defaults.
Makes it easy to experiment with different model configurations without code changes.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Default configuration path
DEFAULT_CONFIG_PATH = "/sphere/app/config.json"

# Default values if config file is missing
DEFAULT_CONFIG = {
    "d_model": 128,  # Embedding dimension size
    "row_limit": 1_000_000,  # Maximum rows for training and upload (1M default)
    "enable_multiprocessing_dataloader": True,  # Enable multiprocessing for DataLoaders (default: enabled)
    "num_workers": None,  # Override number of DataLoader workers (None = auto-detect based on platform/CUDA)
    # Future parameters can be added here:
    # "learning_rate": 0.001,
    # "batch_size": 256,
    # "dropout": 0.1,
}


class SphereConfig:
    """
    Singleton configuration manager for Sphere.
    
    Usage:
        config = SphereConfig.get_instance()
        d_model = config.get_d_model()
    """
    
    _instance: Optional['SphereConfig'] = None
    _config: Dict[str, Any] = None
    _config_path: str = DEFAULT_CONFIG_PATH
    
    def __init__(self):
        """Private constructor. Use get_instance() instead."""
        if SphereConfig._instance is not None:
            raise RuntimeError("Use SphereConfig.get_instance() instead of direct instantiation")
        self._load_config()
    
    @classmethod
    def get_instance(cls, config_path: str = None) -> 'SphereConfig':
        """
        Get the singleton instance of SphereConfig.
        
        Args:
            config_path: Optional custom path to config file (for testing)
        
        Returns:
            SphereConfig instance
        """
        if cls._instance is None:
            if config_path:
                cls._config_path = config_path
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the singleton (useful for testing)."""
        cls._instance = None
        cls._config = None
        cls._config_path = DEFAULT_CONFIG_PATH
    
    def _load_config(self):
        """Load configuration from file or use defaults."""
        config_file = Path(self._config_path)
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    self._config = json.load(f)
                logger.info(f"📋 Loaded Sphere configuration from {config_file}")
                logger.info(f"   Configuration: {json.dumps(self._config, indent=2)}")
                
                # Merge with defaults (in case config file doesn't have all keys)
                for key, default_value in DEFAULT_CONFIG.items():
                    if key not in self._config:
                        logger.info(f"   Using default for missing key '{key}': {default_value}")
                        self._config[key] = default_value
                        
            except json.JSONDecodeError as e:
                logger.error(f"❌ Failed to parse config file {config_file}: {e}")
                logger.info(f"   Using default configuration")
                self._config = DEFAULT_CONFIG.copy()
            except Exception as e:
                logger.error(f"❌ Error reading config file {config_file}: {e}")
                logger.info(f"   Using default configuration")
                self._config = DEFAULT_CONFIG.copy()
        else:
            logger.info(f"ℹ️  No config file found at {config_file}")
            logger.info(f"   Using default configuration: {json.dumps(DEFAULT_CONFIG, indent=2)}")
            self._config = DEFAULT_CONFIG.copy()
        
        # Generate README file if missing
        self._generate_readme_if_missing(config_file)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def get_d_model(self) -> int:
        """Get the d_model (embedding dimension) parameter."""
        return self._config.get("d_model", DEFAULT_CONFIG["d_model"])
    
    def get_row_limit(self) -> int:
        """Get the row_limit (maximum rows for training/upload) parameter."""
        return self._config.get("row_limit", DEFAULT_CONFIG["row_limit"])
    
    def get_enable_multiprocessing_dataloader(self) -> bool:
        """Get the enable_multiprocessing_dataloader flag."""
        return self._config.get("enable_multiprocessing_dataloader", DEFAULT_CONFIG["enable_multiprocessing_dataloader"])
    
    def get_num_workers(self) -> Optional[int]:
        """
        Get the num_workers override from config.
        
        Returns:
            int if set in config, None if not set (should use auto-detection)
        """
        num_workers = self._config.get("num_workers", DEFAULT_CONFIG["num_workers"])
        if num_workers is None:
            return None
        try:
            return int(num_workers)
        except (ValueError, TypeError):
            logger.warning(f"⚠️  Invalid num_workers value in config: {num_workers}, using auto-detection")
            return None
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return self._config.copy()
    
    def log_config(self, prefix: str = ""):
        """
        Log all configuration parameters.
        
        Args:
            prefix: Optional prefix for log messages
        """
        logger.info(f"{prefix}🔧 Sphere Configuration:")
        for key, value in self._config.items():
            logger.info(f"{prefix}   {key}: {value}")
    
    def _generate_readme_if_missing(self, config_file: Path):
        """Generate config.json.README.txt if it doesn't exist."""
        readme_file = config_file.parent / f"{config_file.name}.README.txt"
        
        if readme_file.exists():
            return  # Don't overwrite existing README
        
        try:
            readme_content = self._generate_readme_content()
            readme_file.write_text(readme_content, encoding='utf-8')
            logger.info(f"📝 Generated configuration documentation at {readme_file}")
        except Exception as e:
            logger.warning(f"⚠️  Failed to generate config README: {e}")
    
    def _generate_readme_content(self) -> str:
        """Generate the content for config.json.README.txt."""
        return """Sphere Configuration Documentation
==========================================

This file documents all available parameters for /sphere/app/config.json.
This file is auto-generated on startup if missing.

Location: /sphere/app/config.json

USAGE
-----
1. Edit /sphere/app/config.json (create it if it doesn't exist)
2. Add any parameters you want to customize
3. Restart Sphere services to apply changes
4. Check logs to confirm configuration was loaded

All parameters are optional. Missing parameters use defaults.


CORE PARAMETERS
---------------

d_model (integer, default: 128)
  Embedding dimension size - the fundamental dimensionality of learned representations.
  
  Lower values (64, 128):
    - Faster training
    - Less memory usage
    - Simpler representations
    - May underfit complex datasets
  
  Higher values (256, 512, 1024):
    - Slower training
    - More memory usage
    - Richer representations
    - Better for complex, high-dimensional data
    - May overfit small datasets
  
  Recommendations:
    - Start with default (128) for most datasets
    - Increase to 256+ for large datasets (>100k rows) or high-dimensional data (>50 columns)
    - Decrease to 64 for small datasets (<1k rows) or memory-constrained environments
  
  Example: {"d_model": 256}


row_limit (integer, default: 1000000)
  Maximum number of rows to use for training and upload.
  
  - Default: 1,000,000 (1M rows)
  - Datasets larger than this limit will be randomly sampled
  - Use 10000 for quick testing/samples
  - Set to null or omit for no limit (not recommended for very large datasets)
  
  Example: {"row_limit": 500000}


MULTIPROCESSING PARAMETERS
---------------------------

enable_multiprocessing_dataloader (boolean, default: true)
  Enable multiprocessing for PyTorch DataLoaders.
  
  - true: Enable multiprocessing (uses auto-detection or num_workers if set)
  - false: Force single-process (num_workers=0)
  
  When enabled, workers are auto-detected based on:
    - Platform (macOS: 0 workers, Linux: varies)
    - CUDA availability and GPU memory
    - CPU count
  
  Example: {"enable_multiprocessing_dataloader": false}


num_workers (integer or null, default: null)
  Override number of DataLoader worker processes.
  
  - null: Auto-detect based on platform/CUDA (recommended)
  - 0: Single-process (no multiprocessing)
  - 1-16: Specific number of workers
  
  Only used when enable_multiprocessing_dataloader is true.
  
  Note: Each worker uses ~600MB VRAM for CUDA context on GPU systems.
  
  Example: {"num_workers": 4}


ADDITIONAL PARAMETERS
---------------------

The following parameters may also be available depending on your Sphere version:

spread_lr_multiplier (float or null, default: 1.0)
  Learning rate multiplier for spread loss gradients.
  - 1.0: Same learning rate as other losses (default)
  - < 1.0 (e.g., 0.3): Make spread loss learn more slowly
  - null: Disable (use same LR for all losses)
  
  Example: {"spread_lr_multiplier": 0.5}


use_semantic_set_initialization (boolean, default: false)
  Initialize set embeddings using BERT vectors from string cache.
  - true: Categorical values start with semantic relationships preserved
  - false: Standard initialization (default)
  
  Requires string cache to be enabled.
  
  Example: {"use_semantic_set_initialization": true}


EXAMPLE CONFIGURATION
---------------------

{
  "d_model": 128,
  "row_limit": 1000000,
  "enable_multiprocessing_dataloader": true,
  "num_workers": null,
  "spread_lr_multiplier": 1.0,
  "use_semantic_set_initialization": false
}


PRIORITY ORDER
--------------

Configuration values are determined in this order (highest to lowest priority):

1. Explicit override parameters (in code)
2. PYTORCH_NUM_WORKERS environment variable (for num_workers only)
3. config.json file values
4. Default values (built into Sphere)


TROUBLESHOOTING
---------------

Config file not being read:
  - Check logs for: "📋 Loaded Sphere configuration from /sphere/app/config.json"
  - Ensure file exists and is readable
  - Validate JSON syntax: python3 -m json.tool /sphere/app/config.json

Changes not taking effect:
  - Configuration is loaded at startup - restart services after editing config.json
  - Check logs to confirm new values were loaded

Invalid values:
  - Invalid values fall back to defaults
  - Check logs for warnings about invalid configuration


ENVIRONMENT VARIABLES
---------------------

PYTORCH_NUM_WORKERS (integer)
  Override num_workers (takes precedence over config.json)
  Example: export PYTORCH_NUM_WORKERS=4


For more information, see:
  - SPHERE_CONFIG_README.md (full documentation)
  - config.json.example (example configuration file)

This file is auto-generated. Do not edit manually - it will be regenerated if deleted.
"""


def get_d_model() -> int:
    """
    Convenience function to get d_model from configuration.
    
    Returns:
        d_model value (default: 128)
    
    Example:
        from lib.sphere_config import get_d_model
        
        d_model = get_d_model()  # Gets from config.json or uses default
    """
    return SphereConfig.get_instance().get_d_model()


def get_row_limit() -> int:
    """
    Convenience function to get row_limit from configuration.
    
    Returns:
        row_limit value (default: 1,000,000)
    
    Example:
        from lib.sphere_config import get_row_limit
        
        row_limit = get_row_limit()  # Gets from config.json or uses default
    """
    return SphereConfig.get_instance().get_row_limit()


def get_config() -> SphereConfig:
    """
    Convenience function to get the configuration instance.
    
    Returns:
        SphereConfig instance
    
    Example:
        from lib.sphere_config import get_config
        
        config = get_config()
        d_model = config.get_d_model()
        learning_rate = config.get("learning_rate", 0.001)
    """
    return SphereConfig.get_instance()


def get_data_dir() -> str:
    """
    Compatibility function to get data directory path.
    
    This function exists for backward compatibility with older code that may
    have imported get_data_dir from lib.sphere_config. The actual data directory
    is now managed by the config module.
    
    Returns:
        Data directory path (default: /sphere/app/featrix_data)
    
    Example:
        from lib.sphere_config import get_data_dir
        
        data_dir = get_data_dir()
    """
    # Import here to avoid circular dependencies
    try:
        from config import config
        return str(config.data_dir)
    except (ImportError, AttributeError):
        # Fallback to default if config module not available
        return "/sphere/app/featrix_data"


if __name__ == "__main__":
    # Demo usage
    print("Sphere Configuration Demo")
    print("=" * 60)
    
    config = get_config()
    config.log_config()
    
    print(f"\nGetting specific values:")
    print(f"  d_model: {config.get_d_model()}")
    print(f"  custom_key (default=42): {config.get('custom_key', 42)}")

