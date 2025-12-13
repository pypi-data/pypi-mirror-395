"""
SimpliQ OAuth Callback Server - Configuration Manager

This module handles loading and managing configuration from YAML files
for the OAuth Callback Server.

Author: Gerson Amorim
Date: 28 de Novembro de 2025
Project: SimpliQ - Intelligent ERP Data Platform
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional


class OAuthCallbackConfig:
    """
    Configuration manager for OAuth Callback Server.

    Loads configuration from YAML file and provides typed access to settings.
    Similar to user_manager/config.py but adapted for callback server needs.
    """

    def __init__(self, config_file: str = "oauth_callback_config.yml"):
        """
        Initialize configuration manager.

        Args:
            config_file: Path to YAML configuration file
        """
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Returns:
            Dictionary with configuration data

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML
        """
        config_path = Path(self.config_file)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_file}\n"
                f"Expected location: {config_path.absolute()}"
            )

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            if not config:
                raise ValueError("Configuration file is empty")

            return config

        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")

    def get_server_config(self) -> Dict[str, Any]:
        """
        Get server configuration section.

        Returns:
            Dictionary with server settings:
            - name: str
            - version: str
            - host: str
            - port: int
            - debug: bool
            - ssl_enabled: bool
            - ssl_cert: Optional[str]
            - ssl_key: Optional[str]
        """
        server = self.config_data.get("server", {})

        return {
            "name": server.get("name", "SimpliQ OAuth Callback Server"),
            "version": server.get("version", "1.0.0"),
            "host": server.get("host", "localhost"),
            "port": int(server.get("port", 3000)),
            "debug": bool(server.get("debug", False)),
            "ssl_enabled": bool(server.get("ssl_enabled", False)),
            "ssl_cert": server.get("ssl_cert"),
            "ssl_key": server.get("ssl_key")
        }

    def get_callback_config(self) -> Dict[str, Any]:
        """
        Get callback configuration section.

        Returns:
            Dictionary with callback settings:
            - callback_file: str
            - callback_path: str
        """
        callback = self.config_data.get("callback", {})

        return {
            "callback_file": callback.get("callback_file", "oauth_callback.html"),
            "callback_path": callback.get("callback_path", "/callback")
        }

    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration section.

        Returns:
            Dictionary with logging settings:
            - level: str
            - format: str
            - log_to_file: bool
            - log_file: str
        """
        logging_cfg = self.config_data.get("logging", {})

        return {
            "level": logging_cfg.get("level", "INFO"),
            "format": logging_cfg.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            "log_to_file": bool(logging_cfg.get("log_to_file", True)),
            "log_file": logging_cfg.get("log_file", "oauth_callback_server.log")
        }

    def get_cors_config(self) -> Dict[str, Any]:
        """
        Get CORS configuration section.

        Returns:
            Dictionary with CORS settings:
            - allow_origins: list
            - allow_credentials: bool
        """
        cors = self.config_data.get("cors", {})

        return {
            "allow_origins": cors.get("allow_origins", ["*"]),
            "allow_credentials": bool(cors.get("allow_credentials", True))
        }

    def get_all_config(self) -> Dict[str, Any]:
        """
        Get entire configuration.

        Returns:
            Complete configuration dictionary
        """
        return {
            "server": self.get_server_config(),
            "callback": self.get_callback_config(),
            "logging": self.get_logging_config(),
            "cors": self.get_cors_config()
        }

    def validate_ssl_config(self) -> tuple[bool, Optional[str]]:
        """
        Validate SSL configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        server = self.get_server_config()

        if not server["ssl_enabled"]:
            return True, None

        # Check if cert and key are specified
        if not server["ssl_cert"] or not server["ssl_key"]:
            return False, "SSL is enabled but ssl_cert or ssl_key is not specified"

        # Check if files exist
        cert_path = Path(server["ssl_cert"])
        key_path = Path(server["ssl_key"])

        if not cert_path.exists():
            return False, f"SSL certificate file not found: {server['ssl_cert']}"

        if not key_path.exists():
            return False, f"SSL key file not found: {server['ssl_key']}"

        return True, None


# Convenience function for quick loading
def load_config(config_file: str = "oauth_callback_config.yml") -> OAuthCallbackConfig:
    """
    Load configuration from YAML file.

    Args:
        config_file: Path to configuration file

    Returns:
        OAuthCallbackConfig instance

    Example:
        >>> config = load_config()
        >>> server_cfg = config.get_server_config()
        >>> print(f"Server will run on {server_cfg['host']}:{server_cfg['port']}")
    """
    return OAuthCallbackConfig(config_file)


if __name__ == "__main__":
    # Test configuration loading
    import sys
    import io

    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    print("=" * 70)
    print("OAuth Callback Server - Configuration Test")
    print("=" * 70)

    try:
        config = load_config()

        print("\n✅ Configuration loaded successfully!")
        print("\nServer Configuration:")
        server = config.get_server_config()
        for key, value in server.items():
            print(f"  {key}: {value}")

        print("\nCallback Configuration:")
        callback = config.get_callback_config()
        for key, value in callback.items():
            print(f"  {key}: {value}")

        print("\nLogging Configuration:")
        logging_cfg = config.get_logging_config()
        for key, value in logging_cfg.items():
            print(f"  {key}: {value}")

        print("\nCORS Configuration:")
        cors = config.get_cors_config()
        for key, value in cors.items():
            print(f"  {key}: {value}")

        # Validate SSL if enabled
        is_valid, error = config.validate_ssl_config()
        if not is_valid:
            print(f"\n❌ SSL Configuration Error: {error}")
            sys.exit(1)
        elif server["ssl_enabled"]:
            print("\n✅ SSL Configuration validated")

        print("\n" + "=" * 70)
        print("Configuration is valid and ready to use!")
        print("=" * 70)

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        sys.exit(1)
