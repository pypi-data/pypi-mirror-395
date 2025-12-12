#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Configuration manager for Stata MCP server using TOML format."""

import os
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Third-party fallback
    except ImportError:
        tomllib = None

try:
    import tomli_w
    TOML_WRITE_AVAILABLE = True
except ImportError:
    tomli_w = None
    TOML_WRITE_AVAILABLE = False

from pydantic import BaseModel, Field


class StataServerConfig(BaseModel):
    """Configuration for Stata MCP server."""
    
    name: str = "aigroup-stata-mcp"
    instructions: str = "Stata-MCP lets you and LLMs run Stata do-files and fetch results"
    website_url: str = "https://github.com/jackdark425"
    working_directory: Optional[str] = None
    stata_cli: Optional[str] = None


class ConfigManager:
    """Manager for handling TOML configuration files."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file. If None, uses default location.
        """
        if config_path is None:
            # Default config file location in project directory
            project_root = Path(__file__).parent.parent.parent
            self.config_path = project_root / "config.toml"
        else:
            self.config_path = Path(config_path)
    
    def load_config(self) -> StataServerConfig:
        """
        Load configuration from TOML file.
        
        Returns:
            StataServerConfig: The loaded configuration.
            
        Raises:
            FileNotFoundError: If the config file doesn't exist and no default config.
            ValueError: If TOML parsing fails.
        """
        if not self.config_path.exists():
            # Return default configuration if no config file exists
            return StataServerConfig()
        
        if tomllib is None:
            raise RuntimeError("TOML parsing library not available. "
                             "Please install tomli for Python < 3.11")
        
        try:
            with open(self.config_path, "rb") as f:
                config_data = tomllib.load(f)
            return StataServerConfig(**config_data)
        except Exception as e:
            raise ValueError(f"Failed to load configuration from {self.config_path}: {str(e)}") from e
    
    def save_config(self, config: StataServerConfig) -> None:
        """
        Save configuration to TOML file.
        
        Args:
            config: The configuration to save.
            
        Raises:
            RuntimeError: If TOML writing library is not available.
            IOError: If writing to file fails.
        """
        if not TOML_WRITE_AVAILABLE:
            raise RuntimeError("TOML writing library not available. "
                             "Please install tomli-w to save configuration")
        
        try:
            # Create directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert config to dict and save as TOML
            config_dict = config.model_dump()
            with open(self.config_path, "wb") as f:
                tomli_w.dump(config_dict, f)
        except Exception as e:
            raise IOError(f"Failed to save configuration to {self.config_path}: {str(e)}") from e
    
    def create_default_config(self) -> StataServerConfig:
        """
        Create and save a default configuration file.
        
        Returns:
            StataServerConfig: The default configuration.
        """
        config = StataServerConfig()
        self.save_config(config)
        return config
    
    def config_exists(self) -> bool:
        """
        Check if configuration file exists.
        
        Returns:
            bool: True if config file exists, False otherwise.
        """
        return self.config_path.exists()