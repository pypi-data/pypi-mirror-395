"""SQL file loading and template processing for Duckalog.

This module provides functionality to load SQL content from external files
and process templates with variable substitution.
"""

import re
from pathlib import Path
from typing import Any, Optional

from .errors import (
    SQLFileError,
    SQLFileNotFoundError,
    SQLFilePermissionError,
    SQLFileEncodingError,
    SQLTemplateError,
)
from .logging_utils import log_debug, log_info


class SQLFileLoader:
    """Loads SQL content from external files and processes templates."""

    def __init__(self):
        """Initialize the SQL file loader."""
        self.template_pattern = re.compile(r"\{\{(\w+)\}\}")

    def load_sql_file(
        self,
        file_path: str,
        config_file_path: str,
        variables: Optional[dict[str, Any]] = None,
        as_template: bool = False,
        filesystem: Optional[Any] = None,
    ) -> str:
        """Load SQL content from a file and optionally process as a template.

        Args:
            file_path: Path to the SQL file (can be relative or absolute)
            config_file_path: Path to the config file for resolving relative paths
            variables: Dictionary of variables for template substitution
            as_template: Whether to process the file content as a template
            filesystem: Optional filesystem object for file I/O operations

        Returns:
            The loaded SQL content (processed if template, raw otherwise)

        Raises:
            SQLFileError: If the file cannot be loaded or processed
        """
        variables = variables or {}

        # Resolve the file path relative to config directory
        resolved_path = self._resolve_file_path(file_path, config_file_path)

        log_info(
            "Loading SQL file", file_path=file_path, resolved_path=str(resolved_path)
        )

        # Load the file content
        try:
            if filesystem is not None:
                # Use provided filesystem for I/O
                if not hasattr(filesystem, "open") or not hasattr(filesystem, "exists"):
                    raise SQLFileError(
                        "filesystem object must provide 'open' and 'exists' methods "
                        "for fsspec-compatible interface"
                    )
                if not filesystem.exists(str(resolved_path)):
                    raise SQLFileNotFoundError(
                        f"SQL file not found: {file_path} (resolved to {resolved_path})"
                    )
                with filesystem.open(str(resolved_path), "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                # Use default path-based file I/O
                if not resolved_path.exists():
                    raise SQLFileNotFoundError(
                        f"SQL file not found: {file_path} (resolved to {resolved_path})"
                    )

                try:
                    content = resolved_path.read_text(encoding="utf-8")
                except PermissionError as exc:
                    raise SQLFilePermissionError(
                        f"Permission denied reading SQL file: {resolved_path}"
                    ) from exc
                except UnicodeDecodeError as exc:
                    raise SQLFileEncodingError(
                        f"SQL file has invalid encoding: {resolved_path}"
                    ) from exc

        except OSError as exc:
            raise SQLFileError(f"Failed to read SQL file '{file_path}': {exc}") from exc

        log_debug("SQL file loaded", file_path=file_path, content_length=len(content))

        # Process as template if requested
        if as_template:
            content = self._process_template(content, variables, file_path)

        return content.strip()

    def _resolve_file_path(self, file_path: str, config_file_path: str) -> Path:
        """Resolve a SQL file path relative to the config file directory.

        Args:
            file_path: The SQL file path (can be relative or absolute)
            config_file_path: Path to the config file

        Returns:
            Resolved absolute path to the SQL file

        Raises:
            SQLFileError: If the path is invalid or outside allowed roots
        """
        from .config.validators import (
            is_relative_path,
            resolve_relative_path,
            validate_path_security,
        )

        config_path = Path(config_file_path)

        if is_relative_path(file_path):
            # Resolve relative to config file directory (parent of the config file)
            resolved_str = resolve_relative_path(file_path, config_path.parent)
            resolved = Path(resolved_str)
        else:
            # Absolute path
            resolved = Path(file_path).resolve()

        # Validate path security
        try:
            validate_path_security(str(resolved), config_path.parent)
        except Exception as exc:
            raise SQLFileError(
                f"SQL file path '{file_path}' is not within allowed directory structure"
            ) from exc

        return resolved

    def _process_template(
        self, template_content: str, variables: dict[str, Any], template_path: str
    ) -> str:
        """Process a SQL template with variable substitution.

        Args:
            template_content: The template content with {{variable}} placeholders
            variables: Dictionary of variable values for substitution
            template_path: Path to the template file for error messages

        Returns:
            The processed content with variables substituted

        Raises:
            SQLTemplateError: If required variables are missing
        """
        # Find all placeholder names in the template
        placeholder_names = set()
        for match in self.template_pattern.finditer(template_content):
            placeholder_names.add(match.group(1))

        # Check that all required variables are provided
        missing_variables = placeholder_names - set(variables.keys())
        if missing_variables:
            missing_list = ", ".join(sorted(missing_variables))
            provided_list = ", ".join(sorted(variables.keys())) if variables else "none"
            raise SQLTemplateError(
                f"SQL template '{template_path}' is missing required variables: {missing_list}. "
                f"Provided variables: {provided_list}"
            )

        # Perform variable substitution
        result = template_content
        for var_name, var_value in variables.items():
            # Convert value to string as per spec
            placeholder = f"{{{{{var_name}}}}}"
            result = result.replace(placeholder, str(var_value))

        log_debug(
            "Template processed",
            template_path=template_path,
            variables=len(variables),
            placeholders=len(placeholder_names),
        )

        return result


__all__ = ["SQLFileLoader", "SQLFileError"]
