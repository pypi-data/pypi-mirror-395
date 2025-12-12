"""Configuration saver for ML experiments"""

import json
import os
import inspect
from datetime import datetime
from typing import Optional, List, Dict, Any


def save_config_to_json(
    output_dir: str,
    config_name: str = "config.json",
    exclude: Optional[List[str]] = None
) -> str:
    """
    Save all UPPERCASE variables from the calling module to a JSON file.
    
    Args:
        output_dir: Directory where to save the config
        config_name: Name of the JSON file (default: "config.json")
        exclude: List of variable names to exclude (default: None)
    
    Returns:
        Path to the saved config file
    
    Example:
        >>> RUN_NAME = "my_experiment"
        >>> BATCH_SIZE = 32
        >>> save_config_to_json("./outputs")
        Config saved to: ./outputs/config.json
    """
    # Get the caller's frame
    frame = inspect.currentframe().f_back
    
    # Extract all global variables
    config = {}
    exclude = exclude or []
    
    for name, value in frame.f_globals.items():
        # Keep only UPPERCASE and non-private variables
        if name.isupper() and not name.startswith('_'):
            # Skip excluded variables
            if name in exclude:
                continue
            
            # Convert to JSON serializable format
            try:
                json.dumps(value)  # Test if JSON serializable
                config[name] = value
            except (TypeError, ValueError):
                config[name] = str(value)
    
    # Add metadata
    config['_saved_at'] = datetime.now().isoformat()
    config['_config_version'] = "0.1.0"
    
    # Create directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to JSON
    config_path = os.path.join(output_dir, config_name)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4, sort_keys=True)
    
    print(f"✓ Config saved to: {config_path}")
    return config_path


def load_config_from_json(config_path: str) -> Dict[str, Any]:
    """
    Load a configuration from a JSON file.
    
    Args:
        config_path: Path to the config JSON file
    
    Returns:
        Dictionary with the configuration
    
    Example:
        >>> config = load_config_from_json("./outputs/config.json")
        >>> print(config['RUN_NAME'])
        my_experiment
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print(f"✓ Config loaded from: {config_path}")
    return config


class ConfigSaver:
    """
    Class-based interface for config saving with more control.
    
    Example:
        >>> saver = ConfigSaver(exclude=['DEVICE', 'DEBUG'])
        >>> saver.save("./outputs")
    """
    
    def __init__(self, exclude: Optional[List[str]] = None):
        """
        Initialize the ConfigSaver.
        
        Args:
            exclude: List of variable names to exclude from saving
        """
        self.exclude = exclude or []
    
    def save(self, output_dir: str, config_name: str = "config.json") -> str:
        """
        Save configuration to JSON file.
        
        Args:
            output_dir: Directory where to save the config
            config_name: Name of the JSON file
        
        Returns:
            Path to the saved config file
        """
        return save_config_to_json(output_dir, config_name, self.exclude)
    
    def add_exclude(self, *vars_to_exclude: str) -> None:
        """Add variables to the exclusion list."""
        self.exclude.extend(vars_to_exclude)
    
    def remove_exclude(self, *vars_to_include: str) -> None:
        """Remove variables from the exclusion list."""
        for var in vars_to_include:
            if var in self.exclude:
                self.exclude.remove(var)