"""Configuration management for ngen-gitops."""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


CONFIG_DIR = Path.home() / ".ngen-gitops"
CONFIG_FILE = CONFIG_DIR / "config.json"


DEFAULT_CONFIG = {
    "bitbucket": {
        "username": "",
        "app_password": "",
        "organization": "loyaltoid"
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8080
    }
}


def ensure_config_dir():
    """Ensure config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """Load configuration from ~/.ngen-gitops/config.json.
    
    Falls back to environment variables if config file doesn't exist.
    Creates default config file if it doesn't exist.
    
    Returns:
        dict: Configuration dictionary
    """
    ensure_config_dir()
    
    # Create default config if it doesn't exist
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        print(f"ℹ️  Created default config at {CONFIG_FILE}")
        print(f"   Please update with your Bitbucket credentials")
    
    # Load config from file
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables if present
    env_user = os.getenv('BITBUCKET_USER')
    env_password = os.getenv('BITBUCKET_APP_PASSWORD')
    env_org = os.getenv('BITBUCKET_ORG')
    
    if env_user:
        config['bitbucket']['username'] = env_user
    if env_password:
        config['bitbucket']['app_password'] = env_password
    if env_org:
        config['bitbucket']['organization'] = env_org
    
    return config


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to ~/.ngen-gitops/config.json.
    
    Args:
        config: Configuration dictionary to save
    """
    ensure_config_dir()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    # Set restrictive permissions
    CONFIG_FILE.chmod(0o600)


def get_config_file_path() -> str:
    """Get the config file path.
    
    Returns:
        str: Absolute path to config file
    """
    return str(CONFIG_FILE)


def config_exists() -> bool:
    """Check if config file exists.
    
    Returns:
        bool: True if config exists
    """
    return CONFIG_FILE.exists()


def get_bitbucket_credentials() -> Dict[str, str]:
    """Get Bitbucket credentials from config.
    
    Returns:
        dict: Dictionary with username, app_password, and organization
    
    Raises:
        ValueError: If credentials are not configured
    """
    config = load_config()
    bitbucket = config.get('bitbucket', {})
    
    username = bitbucket.get('username', '')
    app_password = bitbucket.get('app_password', '')
    organization = bitbucket.get('organization', 'loyaltoid')
    
    if not username or not app_password:
        raise ValueError(
            "Bitbucket credentials not configured. "
            f"Please update {CONFIG_FILE} or set BITBUCKET_USER and BITBUCKET_APP_PASSWORD environment variables."
        )
    
    return {
        'username': username,
        'app_password': app_password,
        'organization': organization
    }


def get_server_config() -> Dict[str, Any]:
    """Get server configuration.
    
    Returns:
        dict: Dictionary with host and port
    """
    config = load_config()
    return config.get('server', DEFAULT_CONFIG['server'])
