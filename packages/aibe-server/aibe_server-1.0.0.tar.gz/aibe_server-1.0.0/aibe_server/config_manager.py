"""
Configuration management for the Browser-AI Interface Server
Handles loading configuration from ~/.AIBE/config.json and provides web interface for configuration management
"""

import os
import json
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from functools import lru_cache


class DatabaseConfig(BaseModel):
    """Database configuration settings"""
    connection_string: str = Field(
        default="mongodb://localhost:27017/AIBE",
        description="MongoDB connection string"
    )
    database_name: str = Field(
        default="AIBE",
        description="Database name for storing stories"
    )
    collection_name: str = Field(
        default="Stories",
        description="Collection name for storing stories"
    )
    connection_timeout: int = Field(
        default=30,
        description="Connection timeout in seconds"
    )
    max_pool_size: int = Field(
        default=100,
        description="Maximum connection pool size"
    )


class ServerConfig(BaseModel):
    """Server configuration settings"""
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=3001, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")


class TestStreamingConfig(BaseModel):
    """Test streaming configuration settings"""
    enabled: bool = Field(default=False, description="Enable test streaming to MongoDB")
    database: str = Field(default="test_streams", description="Database for test streams")
    collection_prefix: str = Field(default="test_", description="Prefix for test collection names")
    cleanup_after_days: int = Field(default=7, description="Days to keep test data")


class ServerStreamingConfig(BaseModel):
    """Server streaming configuration settings for live operation debugging"""
    enabled: bool = Field(default=False, description="Enable server streaming to MongoDB")
    database: str = Field(default="server_streams", description="Database for server streams")
    collection_prefix: str = Field(default="server_", description="Prefix for server collection names")
    cleanup_after_days: int = Field(default=7, description="Days to keep server stream data")
    stream_observer: bool = Field(default=True, description="Stream Observer events (browser to server)")
    stream_actor: bool = Field(default=True, description="Stream Actor events (server to browser)")
    stream_story: bool = Field(default=True, description="Stream Story assembly events")
    stream_log: bool = Field(default=True, description="Stream Log events")


class AuthConfig(BaseModel):
    """Authentication configuration settings"""
    config_password: str = Field(default="admin123", description="Password for configuration page")


class Config(BaseModel):
    """Main application configuration"""
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    test_streaming: TestStreamingConfig = Field(default_factory=TestStreamingConfig)
    server_streaming: ServerStreamingConfig = Field(default_factory=ServerStreamingConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)


class ConfigManager:
    """Manages configuration loading, saving, and validation"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".AIBE"
        self.config_file = self.config_dir / "config.json"
        self._config: Optional[Config] = None
        self._ensure_config_exists()
    
    def _ensure_config_exists(self):
        """Ensure config directory and file exist"""
        try:
            # Create directory if it doesn't exist
            self.config_dir.mkdir(mode=0o700, exist_ok=True)
            
            # Create default config file if it doesn't exist
            if not self.config_file.exists():
                self._create_default_config()
                
        except Exception as e:
            print(f"Warning: Could not create config directory/file: {e}")
            
    def _create_default_config(self):
        """Create default configuration file"""
        default_config = Config()
        self._save_config_to_file(default_config)
        
    def _save_config_to_file(self, config: Config):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config.model_dump(), f, indent=2)
            
            # Set file permissions (user read/write only)
            os.chmod(self.config_file, 0o600)
            
        except Exception as e:
            print(f"Error saving config file: {e}")
            raise
    
    def load_config(self) -> Config:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validate and create config object
                return Config(**data)
            else:
                # Return default config if file doesn't exist
                return Config()
                
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Error loading config file, using defaults: {e}")
            return Config()
        except Exception as e:
            print(f"Unexpected error loading config: {e}")
            return Config()
    
    def save_config(self, config: Config):
        """Save configuration to file and clear cache"""
        self._save_config_to_file(config)
        self._config = None  # Clear cache to force reload
        
    def get_config(self) -> Config:
        """Get cached configuration, loading if necessary"""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def update_config(self, updates: Dict[str, Any]) -> Config:
        """Update configuration with new values"""
        current_config = self.get_config()
        
        # Convert to dict for easy updating
        config_dict = current_config.model_dump()
        
        # Apply updates
        for section, values in updates.items():
            if section in config_dict and isinstance(values, dict):
                config_dict[section].update(values)
        
        # Create new config object and save
        new_config = Config(**config_dict)
        self.save_config(new_config)
        
        return new_config
    
    def validate_config(self, config_data: Dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate configuration data"""
        errors = []
        
        try:
            Config(**config_data)
            return True, []
        except ValidationError as e:
            for error in e.errors():
                field = '.'.join(str(x) for x in error['loc'])
                errors.append(f"{field}: {error['msg']}")
            return False, errors
    
    def backup_config(self) -> bool:
        """Create backup of current config file"""
        try:
            if self.config_file.exists():
                backup_file = self.config_file.with_suffix('.json.backup')
                shutil.copy2(self.config_file, backup_file)
                return True
            return False
        except Exception as e:
            print(f"Error creating config backup: {e}")
            return False
    
    def get_config_file_path(self) -> str:
        """Get the path to the configuration file"""
        return str(self.config_file)


# Global config manager instance
_config_manager = ConfigManager()


def get_config() -> Config:
    """Get configuration instance"""
    return _config_manager.get_config()


def get_config_manager() -> ConfigManager:
    """Get the config manager instance"""
    return _config_manager


def get_database_config() -> DatabaseConfig:
    """Get database configuration"""
    return get_config().database


def get_server_config() -> ServerConfig:
    """Get server configuration"""
    return get_config().server


def get_test_streaming_config() -> TestStreamingConfig:
    """Get test streaming configuration"""
    return get_config().test_streaming


def get_server_streaming_config() -> ServerStreamingConfig:
    """Get server streaming configuration"""
    return get_config().server_streaming


def get_auth_config() -> AuthConfig:
    """Get authentication configuration"""
    return get_config().auth


# Utility functions for backward compatibility
def get_mongodb_connection_string() -> str:
    """Get MongoDB connection string"""
    return get_database_config().connection_string


def get_mongodb_database_name() -> str:
    """Get MongoDB database name"""
    return get_database_config().database_name


def get_mongodb_collection_name() -> str:
    """Get MongoDB collection name"""
    return get_database_config().collection_name


def is_development() -> bool:
    """Check if running in development mode"""
    return get_server_config().debug


def is_production() -> bool:
    """Check if running in production mode"""
    return not get_server_config().debug


def validate_mongodb_connection_string(connection_string: str) -> bool:
    """Validate MongoDB connection string format"""
    if not connection_string:
        return False
    
    # Basic validation - should start with mongodb:// or mongodb+srv://
    return (
        connection_string.startswith("mongodb://") or 
        connection_string.startswith("mongodb+srv://")
    )