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
    "normalize_column_encoders": False,  # Phase 1 fix: only normalize in joint encoder
    "normalize_joint_encoder": True,  # Should almost always be True
    "use_semantic_set_initialization": True,  # Initialize set embeddings from BERT (also enables OOV handling)
    "enable_spectral_norm_clipping": True,  # Enable spectral norm clipping during training
    "spectral_norm_clip_threshold": 12.0,  # Maximum spectral norm before clipping (if enabled)
    "adaptive_scalar_hidden_dim": 16,  # Hidden dimension for AdaptiveScalarEncoder MLPs (default: 16 for speed)
    "use_delimiter_preprocessing": False,  # Preprocess delimited strings ("a,b,c" → "a\nb\nc") before BERT encoding
    "enable_predictor_architecture_selection": False,  # DISABLED: Architecture selection wastes 30+ epochs for <1% improvement
    "string_server_host": "taco.local",  # String server host: "taco", "taco.local", or "localhost" (None = use local model)
    "es_weight_initialization": "random",  # "random" = standard pytorch init, "pca_string" = init from PCA of string embeddings
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
    
    def get_normalize_column_encoders(self) -> bool:
        """
        Get whether to normalize individual column encoder outputs.
        
        When False: Column encoders return unnormalized vectors (Phase 1 fix)
        When True: Column encoders normalize their outputs (legacy behavior)
        
        Default: True (for backward compatibility)
        
        This controls the redundant normalization that limits sphere coverage.
        Setting to False removes column-level normalization, keeping only the
        final joint encoder normalization.
        """
        return self._config.get("normalize_column_encoders", DEFAULT_CONFIG["normalize_column_encoders"])
    
    def get_normalize_joint_encoder(self) -> bool:
        """
        Get whether to normalize joint encoder output.
        
        This should almost always be True to ensure embeddings lie on unit sphere.
        
        Default: True
        
        Only set to False for experimental purposes or specific use cases
        where unnormalized embeddings are desired.
        """
        return self._config.get("normalize_joint_encoder", DEFAULT_CONFIG["normalize_joint_encoder"])
    
    def use_semantic_set_initialization(self) -> bool:
        """
        Get whether to initialize set embeddings using BERT vectors from string cache.
        
        When True:
        - Set embeddings are initialized with semantic vectors (e.g., colors, sizes in order)
        - Out-of-vocabulary values at inference can use BERT projection instead of UNKNOWN
        - Faster convergence and better rare value handling
        
        Default: False (backward compatible)
        
        Requires string cache to be enabled during training.
        """
        return self._config.get("use_semantic_set_initialization", DEFAULT_CONFIG.get("use_semantic_set_initialization", False))
    
    def use_delimiter_preprocessing(self) -> bool:
        """
        Get whether to preprocess delimited strings before BERT encoding.
        
        When True:
        - Detect common delimiters (comma, semicolon, pipe, slash, tab) in string columns
        - Preprocess: "a,b,c" → "a\\nb\\nc" before BERT encoding
        - Results in better embeddings for multi-valued fields
        - Requires 30%+ of values to have delimiter to activate
        
        When False:
        - No delimiter detection or preprocessing
        - Strings are encoded by BERT as-is
        - DELIMITER strategy in adaptive encoder still learns when to trust BERT's raw encoding
        
        Default: False (conservative - no preprocessing)
        
        Note: Enabling this CHANGES string cache keys for columns with detected delimiters.
        Existing trained models with cached strings may need retraining.
        Only detects "safe" delimiters: , ; | / :: // \\t (not - or _ due to false positive risk)
        """
        return self._config.get("use_delimiter_preprocessing", DEFAULT_CONFIG.get("use_delimiter_preprocessing", False))
    
    def get_enable_spectral_norm_clipping(self) -> bool:
        """
        Get whether to enable spectral norm clipping during training.
        
        When True:
        - Spectral norms of layers exceeding the threshold are clipped
        - Helps stabilize training by preventing extreme weight values
        
        When False:
        - No spectral norm clipping is applied
        - Layers can have arbitrarily large spectral norms
        
        Default: True (for stability)
        
        Note: This can be disabled to allow more exploration during training,
        but may lead to instability in some cases.
        """
        return self._config.get("enable_spectral_norm_clipping", DEFAULT_CONFIG.get("enable_spectral_norm_clipping", True))
    
    def get_spectral_norm_clip_threshold(self) -> float:
        """
        Get the spectral norm clipping threshold.
        
        If spectral norm clipping is enabled, layers with spectral norms
        exceeding this threshold will be clipped down to this value.
        
        Default: 12.0
        
        Higher values allow larger weight magnitudes.
        Lower values enforce more conservative weight constraints.
        """
        return self._config.get("spectral_norm_clip_threshold", DEFAULT_CONFIG.get("spectral_norm_clip_threshold", 12.0))
    
    def get_adaptive_scalar_hidden_dim(self) -> int:
        """
        Get the hidden dimension size for AdaptiveScalarEncoder MLPs.
        
        Each strategy (linear, log, robust, rank, periodic) uses an MLP with this hidden size.
        Smaller values = faster training but potentially less expressive.
        
        Default: 16 (good balance of speed and quality)
        
        Common values:
        - 16: Fast, 4× faster than 64 (recommended for most use cases)
        - 32: Medium, 2× faster than 64 (good accuracy/speed tradeoff)
        - 64: Slow, most expressive (use if accuracy is critical)
        """
        return self._config.get("adaptive_scalar_hidden_dim", DEFAULT_CONFIG.get("adaptive_scalar_hidden_dim", 16))
    
    def get_string_server_host(self) -> Optional[str]:
        """
        Get the string server host configuration.
        
        Returns:
            "taco" - Use remote string server (tries taco.local first, then taco, then proxy)
            "taco.local" - Use remote string server directly at taco.local:9000
            "localhost" - Use local string server at localhost:9000
            None - Use local sentence transformer model (legacy behavior)
        
        Default: "taco.local" (uses remote string server)
        """
        return self._config.get("string_server_host", DEFAULT_CONFIG.get("string_server_host", "taco.local"))
    
    def get_enable_predictor_architecture_selection(self) -> bool:
        """
        Get whether to enable automatic predictor architecture selection during EmbeddingSpace training.
        
        When True:
        - The system will train multiple candidate predictor architectures for a few epochs
        - Selects the best architecture based on validation loss
        - Affects both column predictors and joint predictor
        - Only runs on fresh training (not when resuming from checkpoint)
        
        When False:
        - Uses default predictor architecture (no selection)
        - Faster training start (skips architecture selection phase)
        
        Default: False (DISABLED - architecture selection provides <1% improvement for 30+ epochs overhead)
        
        Note: Architecture selection adds ~15 epochs × 2-4 candidates = ~30-60 epochs of overhead
        before main training begins, but typically only shows <1% validation loss improvement.
        """
        return self._config.get("enable_predictor_architecture_selection", DEFAULT_CONFIG.get("enable_predictor_architecture_selection", False))
    
    def get_es_weight_initialization(self) -> str:
        """
        Get the embedding space weight initialization strategy.
        
        Options:
        - "random": Standard PyTorch initialization (default)
        - "pca_string": Initialize weights using PCA of string embeddings from sentence transformer
        
        Default: "random"
        
        The PCA initialization uses statistics from sentence transformer embeddings to set
        initial weight distributions. This can help with convergence but requires access
        to the string server for BERT embeddings.
        """
        return self._config.get("es_weight_initialization", DEFAULT_CONFIG.get("es_weight_initialization", "random"))
    
    def auto_compute_d_model(self, num_columns: int) -> int:
        """
        Auto-compute d_model based on number of columns (if not manually set).
        
        Tiers (multiples of 64):
        - < 10 columns:  64
        - < 30 columns:  128
        - < 60 columns:  192
        - >= 60 columns: 256
        
        Args:
            num_columns: Number of columns in dataset
        
        Returns:
            Recommended d_model
        """
        # Check if manually overridden in config
        if "d_model" in self._config:
            return self._config["d_model"]
        
        # Auto-compute based on tiers
        if num_columns < 10:
            return 64
        elif num_columns < 30:
            return 128
        elif num_columns < 60:
            return 192
        else:
            return 256
    
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


def get_d_model() -> int:
    """
    Convenience function to get d_model from configuration.
    
    Returns:
        d_model value (default: 128)
    
    Example:
        from featrix.neural.sphere_config import get_d_model
        
        d_model = get_d_model()  # Gets from config.json or uses default
    """
    return SphereConfig.get_instance().get_d_model()


def get_config() -> SphereConfig:
    """
    Convenience function to get the configuration instance.
    
    Returns:
        SphereConfig instance
    
    Example:
        from featrix.neural.sphere_config import get_config
        
        config = get_config()
        d_model = config.get_d_model()
        learning_rate = config.get("learning_rate", 0.001)
    """
    return SphereConfig.get_instance()


if __name__ == "__main__":
    # Demo usage
    print("Sphere Configuration Demo")
    print("=" * 60)
    
    config = get_config()
    config.log_config()
    
    print(f"\nGetting specific values:")
    print(f"  d_model: {config.get_d_model()}")
    print(f"  custom_key (default=42): {config.get('custom_key', 42)}")

