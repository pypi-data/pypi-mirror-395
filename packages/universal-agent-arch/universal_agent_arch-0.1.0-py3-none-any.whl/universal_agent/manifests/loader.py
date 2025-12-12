"""
universal_agent.manifests.loader

Responsible for loading, parsing, and validating Agent Manifest YAML files.
Handles environment variable expansion and Pydantic validation.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml
from pydantic import ValidationError

from .schema import AgentManifest

logger = logging.getLogger(__name__)

# Regex for matching ${VAR_NAME} or ${VAR_NAME:default_value}
ENV_VAR_PATTERN = re.compile(r"\$\{([A-Za-z0-9_]+)(?::([^}]*))?\}")


class ManifestLoadingError(Exception):
    """Raised when the manifest cannot be loaded or validated."""


class ManifestLoader:
    """
    Loads agent manifests from filesystem, expands environment variables,
    and validates against the Pydantic schema.
    """

    @classmethod
    def load_from_path(cls, path: Union[str, Path]) -> AgentManifest:
        """
        Load a manifest from a file path.

        Args:
            path: Path to the YAML file.

        Returns:
            Validated AgentManifest object.

        Raises:
            ManifestLoadingError: If file not found, invalid YAML, or schema violation.
        """
        file_path = Path(path)
        if not file_path.exists():
            raise ManifestLoadingError(f"Manifest file not found: {file_path}")

        try:
            raw_content = file_path.read_text(encoding="utf-8")
        except Exception as exc:
            raise ManifestLoadingError(f"Failed to read file {file_path}: {exc}")

        expanded_content = cls._expand_env_vars(raw_content)

        try:
            data = yaml.safe_load(expanded_content)
        except yaml.YAMLError as exc:
            raise ManifestLoadingError(f"Invalid YAML syntax in {file_path}: {exc}")

        if not isinstance(data, dict):
            raise ManifestLoadingError(
                f"Manifest root must be a dictionary, got {type(data)}"
            )

        return cls.load_from_dict(data)

    @classmethod
    def load_from_dict(cls, data: Dict[str, Any]) -> AgentManifest:
        """
        Validate a raw dictionary against the AgentManifest schema.
        """
        try:
            return AgentManifest.model_validate(data)
        except ValidationError as exc:
            error_messages = []
            for error in exc.errors():
                loc = " -> ".join(str(x) for x in error["loc"])
                msg = error["msg"]
                error_messages.append(f"Field '{loc}': {msg}")
            error_text = "\n".join(error_messages)
            raise ManifestLoadingError(f"Manifest validation failed:\n{error_text}")

    @staticmethod
    def _expand_env_vars(content: str) -> str:
        """
        Replace ${VAR} and ${VAR:default} with environment variable values.
        Raises ManifestLoadingError if a variable is missing and no default is provided.
        """

        def replace_match(match: re.Match[str]) -> str:
            var_name = match.group(1)
            default_value = match.group(2)
            value: Optional[str] = os.getenv(var_name)
            if value is not None:
                return value
            if default_value is not None:
                return default_value
            raise ManifestLoadingError(
                f"Missing required environment variable: {var_name}"
            )

        try:
            return ENV_VAR_PATTERN.sub(replace_match, content)
        except ManifestLoadingError:
            raise
        except Exception as exc:
            raise ManifestLoadingError(str(exc))

