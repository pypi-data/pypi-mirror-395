import json
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for CLI"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".oroio-cli"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()
        self._load_env()
    
    def _ensure_config_dir(self):
        """Ensure config directory exists"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_env(self):
        """Load environment variables from .env file"""
        # Try to load .env from multiple locations (in priority order)
        env_locations = [
            Path.cwd() / ".env",                    # Current directory
            Path(__file__).parent / ".env",         # CLI directory
            Path.home() / ".oroio-cli" / ".env",    # Config directory
        ]
        
        for env_file in env_locations:
            if env_file.exists():
                load_dotenv(env_file, override=False)
                break
    
    def load(self) -> dict:
        """Load configuration from file and environment variables"""
        # Start with default config
        config = {
            "api_endpoint": "http://localhost:8000",
            "access_token": None,
            "refresh_token": None
        }
        
        # Load from config file if exists
        if self.config_file.exists():
            try:
                file_config = json.loads(self.config_file.read_text())
                config.update(file_config)
            except:
                pass
        
        # Override with environment variables if set
        # Environment variables take precedence over config file
        if os.getenv("OROIO_API_ENDPOINT"):
            config["api_endpoint"] = os.getenv("OROIO_API_ENDPOINT")
        
        return config
    
    def save(self, config: dict):
        """Save configuration to file"""
        self.config_file.write_text(json.dumps(config, indent=2))
    
    def get_api_endpoint(self) -> str:
        """Get API endpoint"""
        config = self.load()
        return config.get("api_endpoint", "http://localhost:8000")
    
    def set_api_endpoint(self, endpoint: str):
        """Set API endpoint"""
        config = self.load()
        config["api_endpoint"] = endpoint
        self.save(config)
    
    def get_access_token(self) -> Optional[str]:
        """Get access token"""
        config = self.load()
        return config.get("access_token")
    
    def set_tokens(self, access_token: str, refresh_token: str):
        """Set access and refresh tokens"""
        config = self.load()
        config["access_token"] = access_token
        config["refresh_token"] = refresh_token
        self.save(config)
    
    def clear_tokens(self):
        """Clear authentication tokens"""
        config = self.load()
        config["access_token"] = None
        config["refresh_token"] = None
        self.save(config)
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.get_access_token() is not None


# Global config instance
config = Config()
