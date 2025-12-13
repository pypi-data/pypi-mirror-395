# Copyright (c) 2025 Microsoft Corporation.
# Licensed under the MIT License

"""
Standalone configuration for nlweb-dataload.

Minimal config focused on database endpoints and embedding providers.
Does not depend on nlweb_core.
"""

import os
import yaml
from typing import Optional, Dict, Any
from pathlib import Path


class DataloadConfig:
    """Configuration for data loading operations."""

    def __init__(self):
        """Initialize with default values."""
        self.config_data = {}
        self.embedding_provider = None
        self.embedding_providers = {}
        self.write_endpoint = None
        self.database_endpoints = {}

    def load(self, config_path: Optional[str] = None):
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to config.yaml file. If not provided, searches:
                - ./config.yaml
                - ./config/config.yaml
                - ~/.nlweb/config.yaml
        """
        # Load .env file first (for environment variables)
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass

        # Find config file
        if not config_path:
            config_path = self._find_config_file()

        if not config_path or not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Config file not found. Provide path or create config.yaml"
            )

        # Load YAML
        with open(config_path, 'r') as f:
            self.config_data = yaml.safe_load(f)

        # Parse embedding configuration
        self._load_embedding_config()

        # Parse database endpoints
        self._load_database_config()

    def _find_config_file(self) -> Optional[str]:
        """Search for config.yaml in common locations."""
        search_paths = [
            'config.yaml',
            'config/config.yaml',
            os.path.expanduser('~/.nlweb/config.yaml')
        ]

        for path in search_paths:
            if os.path.exists(path):
                return path

        return None

    def _load_embedding_config(self):
        """Load embedding provider configuration (unified format)."""
        embedding_config = self.config_data.get('embedding', {})

        # Get preferred provider
        self.embedding_provider = embedding_config.get('provider')

        # Add single embedding config as a provider (unified format)
        if self.embedding_provider and embedding_config:
            self.embedding_providers[self.embedding_provider] = embedding_config

    def _load_database_config(self):
        """Load database endpoint configuration (unified format)."""
        # In unified format, there's a single 'retrieval' config
        retrieval_config = self.config_data.get('retrieval', {})

        # Get provider name as the endpoint name
        provider = retrieval_config.get('provider')

        if provider and retrieval_config:
            # Use provider name as endpoint name
            self.database_endpoints[provider] = self._parse_endpoint_config(
                provider, retrieval_config
            )
            # Set as default write endpoint
            self.write_endpoint = provider

    def _parse_endpoint_config(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse endpoint configuration and resolve environment variables.

        Args:
            name: Endpoint name
            config: Raw config dict

        Returns:
            Parsed config dict
        """
        parsed = {}

        # Copy basic fields
        for key in ['db_type', 'index_name', 'auth_method', 'enabled']:
            if key in config:
                parsed[key] = config[key]

        # Set db_type from provider if not explicitly set
        if 'db_type' not in parsed and 'provider' in config:
            parsed['db_type'] = config['provider']

        # Resolve environment variables for sensitive fields
        if 'api_endpoint_env' in config:
            parsed['api_endpoint'] = os.getenv(config['api_endpoint_env'])
        elif 'api_endpoint' in config:
            parsed['api_endpoint'] = config['api_endpoint']

        if 'api_key_env' in config:
            parsed['api_key'] = os.getenv(config['api_key_env'])
        elif 'api_key' in config:
            parsed['api_key'] = config['api_key']

        # Parse writer configuration
        if 'writer' in config:
            parsed['writer'] = config['writer']

        return parsed

    def get_embedding_config(self, provider: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for an embedding provider with resolved env vars.

        Args:
            provider: Provider name

        Returns:
            Provider config dict with env vars resolved or None
        """
        config = self.embedding_providers.get(provider)
        if not config:
            return None

        # Create a copy with resolved env vars
        resolved = dict(config)

        # Resolve endpoint_env
        if 'endpoint_env' in config:
            resolved['endpoint'] = os.getenv(config['endpoint_env'])

        # Resolve api_key_env
        if 'api_key_env' in config:
            resolved['api_key'] = os.getenv(config['api_key_env'])

        return resolved

    def get_database_endpoint(self, endpoint_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get database endpoint configuration.

        Args:
            endpoint_name: Endpoint name, or None to use write_endpoint

        Returns:
            Endpoint config dict

        Raises:
            ValueError: If endpoint not found
        """
        endpoint_name = endpoint_name or self.write_endpoint

        if not endpoint_name:
            raise ValueError("No endpoint specified and no write_endpoint configured")

        if endpoint_name not in self.database_endpoints:
            available = list(self.database_endpoints.keys())
            raise ValueError(
                f"Unknown endpoint '{endpoint_name}'. Available: {', '.join(available)}"
            )

        return self.database_endpoints[endpoint_name]


# Global config instance
CONFIG = DataloadConfig()


def init(config_path: Optional[str] = None):
    """
    Initialize configuration.

    Args:
        config_path: Optional path to config.yaml

    Example:
        import nlweb_dataload
        nlweb_dataload.init(config_path="config.yaml")
    """
    CONFIG.load(config_path)

    # Also initialize nlweb_core config if available (for Azure providers that depend on it)
    try:
        from nlweb_core.config import CONFIG as CORE_CONFIG
        CORE_CONFIG._load_unified_config(config_path)
    except (ImportError, AttributeError):
        # nlweb_core not available or method doesn't exist, skip
        pass
