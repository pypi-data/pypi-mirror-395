"""
Claude Desktop Configuration Manager

This module provides automated configuration management for Claude Desktop,
specifically for updating OAuth tokens in the claude_desktop_config.json file.

Author: Gerson Amorim
Date: 28 de Novembro de 2025
Project: SimpliQ - Intelligent ERP Data Platform
"""

import json
import os
import shutil
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ClaudeConfigManager:
    """
    Manages Claude Desktop configuration file (claude_desktop_config.json).

    This class provides methods to:
    - Detect the configuration file location based on OS
    - Read and validate existing configuration
    - Create backups before modifications
    - Update OAuth tokens while preserving other settings
    - Save configuration atomically
    """

    # Default MCP server configuration
    # Try to update existing servers in this order of preference
    KNOWN_SERVER_NAMES = ["Tryton local", "SimpliQ MCP Server"]
    DEFAULT_SERVER_NAME = "Tryton local"  # Default name if creating new
    DEFAULT_MCP_CONFIG = {
        "mcpServers": {
            "Tryton local": {
                "command": "npx",
                "args": [
                    "mcp-remote",
                    "http://localhost:8000",
                    "--allow-http",
                    "--header",
                    "Authorization: Bearer {token}"
                ]
            }
        },
        "isUsingBuiltInNodeForMcp": False
    }

    @staticmethod
    def get_config_path() -> Path:
        """
        Detect the path to Claude Desktop configuration file based on OS.

        Returns:
            Path object pointing to claude_desktop_config.json

        Platform-specific paths:
            - Windows: %APPDATA%\\Claude\\claude_desktop_config.json
            - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
            - Linux: ~/.config/Claude/claude_desktop_config.json
        """
        system = platform.system()

        if system == "Windows":
            base_path = Path(os.getenv("APPDATA", ""))
        elif system == "Darwin":  # macOS
            base_path = Path.home() / "Library" / "Application Support"
        else:  # Linux and others
            base_path = Path.home() / ".config"

        config_path = base_path / "Claude" / "claude_desktop_config.json"
        logger.info(f"Detected config path for {system}: {config_path}")

        return config_path

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the configuration manager.

        Args:
            config_path: Optional custom path to config file.
                        If None, auto-detects based on OS.
        """
        self.config_path = config_path or self.get_config_path()
        logger.info(f"ClaudeConfigManager initialized with path: {self.config_path}")

    def read_config(self) -> Dict[str, Any]:
        """
        Read and validate the Claude Desktop configuration file.

        Returns:
            Dictionary containing the configuration

        Returns empty config structure if file doesn't exist.
        Raises exception if file exists but contains invalid JSON.
        """
        if not self.config_path.exists():
            logger.info("Config file does not exist, will create new one")
            return {"mcpServers": {}, "isUsingBuiltInNodeForMcp": False}

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            logger.info(f"Successfully read config with {len(config.get('mcpServers', {}))} servers")
            return config

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise ValueError(f"Configuration file contains invalid JSON: {e}")
        except Exception as e:
            logger.error(f"Error reading config file: {e}")
            raise

    def backup_config(self) -> Optional[Path]:
        """
        Create a timestamped backup of the existing configuration file.

        Returns:
            Path to the backup file, or None if no backup was needed

        Backup format: claude_desktop_config.json.backup.YYYY-MM-DD_HH-MM-SS-microseconds
        """
        if not self.config_path.exists():
            logger.info("No existing config to backup")
            return None

        # Include microseconds to ensure unique filenames even with rapid calls
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        backup_path = self.config_path.with_suffix(f".json.backup.{timestamp}")

        try:
            # Use copy() instead of copy2() to set new mtime on backup
            # This ensures backups are properly sorted by creation time
            shutil.copy(self.config_path, backup_path)
            logger.info(f"Created backup at: {backup_path}")

            # Cleanup old backups (keep last 5)
            self._cleanup_old_backups()

            return backup_path

        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise

    def _cleanup_old_backups(self, keep_count: int = 5):
        """
        Remove old backup files, keeping only the most recent ones.

        Args:
            keep_count: Number of most recent backups to keep
        """
        try:
            backup_pattern = f"{self.config_path.stem}.json.backup.*"
            backup_dir = self.config_path.parent

            # Find all backup files
            backups = sorted(
                backup_dir.glob(backup_pattern),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            # Remove old backups
            for old_backup in backups[keep_count:]:
                old_backup.unlink()
                logger.info(f"Removed old backup: {old_backup.name}")

        except Exception as e:
            logger.warning(f"Failed to cleanup old backups: {e}")

    def update_server_config(self, config: Dict[str, Any], token: str, server_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Update or add the SimpliQ MCP Server configuration with new token.

        Args:
            config: Existing configuration dictionary
            token: New OAuth Bearer token
            server_name: Optional name of the MCP server to update. If not provided:
                        - Updates "Tryton local" if it exists
                        - Else updates "SimpliQ MCP Server" if it exists
                        - Else creates new "Tryton local" server

        Returns:
            Updated configuration dictionary

        Strategy:
        1. If server_name is provided and exists, update it
        2. If server_name is provided but doesn't exist, create it
        3. If server_name is None, use automatic detection (legacy behavior)

        Preserves other MCP servers and settings.
        """
        # Ensure mcpServers key exists
        if "mcpServers" not in config:
            config["mcpServers"] = {}

        # Determine which server to update
        server_to_update = None
        actual_server_name = None  # Track the actual name in the config (with original casing)

        if server_name:
            # User explicitly specified which server to configure
            # Search case-insensitively to avoid duplicates
            server_name_lower = server_name.lower()

            for existing_name in config["mcpServers"].keys():
                if existing_name.lower() == server_name_lower:
                    # Found matching server (case-insensitive)
                    actual_server_name = existing_name  # Use existing name's casing
                    server_to_update = existing_name
                    logger.info(f"User specified server '{server_name}' matches existing '{existing_name}' (case-insensitive), will update it")
                    break

            if actual_server_name is None:
                # Server doesn't exist, will create with user's casing
                server_to_update = server_name
                logger.info(f"User specified server '{server_name}' does not exist, will create it")
        else:
            # Legacy behavior: auto-detect which server to update
            for known_name in self.KNOWN_SERVER_NAMES:
                # Also use case-insensitive comparison for known names
                known_name_lower = known_name.lower()

                for existing_name in config["mcpServers"].keys():
                    if existing_name.lower() == known_name_lower:
                        server_to_update = existing_name
                        logger.info(f"Found existing server '{existing_name}' matching known name '{known_name}' (case-insensitive), will update it")
                        break

                if server_to_update:
                    break

            # If no known server exists, use default name
            if server_to_update is None:
                server_to_update = self.DEFAULT_SERVER_NAME
                logger.info(f"No existing SimpliQ server found, will create '{server_to_update}'")

        # Build server config with new token
        server_config = {
            "command": "npx",
            "args": [
                "mcp-remote",
                "http://localhost:8000",
                "--allow-http",
                "--header",
                f"Authorization: Bearer {token}"
            ]
        }

        # Update or create the server
        config["mcpServers"][server_to_update] = server_config

        # Ensure isUsingBuiltInNodeForMcp is set
        if "isUsingBuiltInNodeForMcp" not in config:
            config["isUsingBuiltInNodeForMcp"] = False

        logger.info(f"Updated server config for '{server_to_update}'")

        # Store the server name that was updated for reporting
        self._last_updated_server = server_to_update

        return config

    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        Save configuration to file atomically.

        Args:
            config: Configuration dictionary to save

        Returns:
            True if successful

        Writes to a temporary file first, then renames to ensure atomicity.
        """
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temporary file
            temp_path = self.config_path.with_suffix('.json.tmp')

            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_path.replace(self.config_path)

            logger.info(f"Successfully saved config to: {self.config_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            # Cleanup temp file if it exists
            if temp_path.exists():
                temp_path.unlink()
            raise

    def auto_configure(self, token: str, server_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Main method to automatically configure Claude Desktop with OAuth token.

        This method orchestrates the entire configuration process:
        1. Read existing configuration (or create new)
        2. Create backup if config exists
        3. Update with new token
        4. Save atomically
        5. Return result with status and paths

        Args:
            token: OAuth Bearer token to configure
            server_name: Optional name of the MCP server to update. If not provided,
                        uses automatic detection to find existing SimpliQ servers.

        Returns:
            Dictionary with operation result:
            {
                "success": bool,
                "message": str,
                "config_path": str,
                "backup_path": str (optional),
                "server_name": str,  # Name of the server that was configured
                "errors": list (optional)
            }
        """
        result = {
            "success": False,
            "message": "",
            "config_path": str(self.config_path),
            "errors": []
        }

        try:
            # Validate token
            if not token or not token.strip():
                result["message"] = "Token cannot be empty"
                result["errors"].append("Empty token provided")
                return result

            token = token.strip()

            # Read existing config
            logger.info("Reading existing configuration...")
            config = self.read_config()

            # Create backup if file exists
            backup_path = self.backup_config()
            if backup_path:
                result["backup_path"] = str(backup_path)

            # Update configuration
            logger.info("Updating configuration with new token...")
            config = self.update_server_config(config, token, server_name)

            # Save configuration
            logger.info("Saving configuration...")
            self.save_config(config)

            # Get the server name that was updated
            updated_server = getattr(self, '_last_updated_server', server_name or self.DEFAULT_SERVER_NAME)

            # Success!
            result["success"] = True
            result["server_name"] = updated_server
            result["message"] = (
                f"Claude Desktop configured successfully! "
                f"Server '{updated_server}' updated with new token. "
                f"Please restart Claude Desktop for changes to take effect."
            )

            logger.info("Auto-configuration completed successfully")
            return result

        except PermissionError as e:
            result["message"] = (
                f"Permission denied: Cannot write to {self.config_path}. "
                f"Please check file permissions or run with appropriate privileges."
            )
            result["errors"].append(str(e))
            logger.error(f"Permission error: {e}")

        except ValueError as e:
            result["message"] = f"Invalid configuration file: {e}"
            result["errors"].append(str(e))
            logger.error(f"Validation error: {e}")

        except Exception as e:
            result["message"] = f"Unexpected error during configuration: {e}"
            result["errors"].append(str(e))
            logger.error(f"Unexpected error: {e}", exc_info=True)

        return result


# Convenience function for quick usage
def configure_claude_desktop(token: str, server_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to configure Claude Desktop with a token.

    Args:
        token: OAuth Bearer token
        server_name: Optional name of the MCP server to update

    Returns:
        Result dictionary from auto_configure()

    Example:
        >>> result = configure_claude_desktop("eyJhbGc...")
        >>> if result["success"]:
        ...     print(f"Configured: {result['config_path']}")
        ...     print(f"Server: {result['server_name']}")
    """
    manager = ClaudeConfigManager()
    return manager.auto_configure(token, server_name)


if __name__ == "__main__":
    # Simple CLI for testing
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) < 2:
        print("Usage: python claude_config_manager.py <oauth_token>")
        sys.exit(1)

    token = sys.argv[1]
    result = configure_claude_desktop(token)

    print("\n" + "="*70)
    if result["success"]:
        print("✅ SUCCESS")
        print(f"\n{result['message']}")
        print(f"\nConfig file: {result['config_path']}")
        if "backup_path" in result:
            print(f"Backup file: {result['backup_path']}")
    else:
        print("❌ FAILED")
        print(f"\n{result['message']}")
        if result.get("errors"):
            print("\nErrors:")
            for error in result["errors"]:
                print(f"  - {error}")
    print("="*70 + "\n")

    sys.exit(0 if result["success"] else 1)
