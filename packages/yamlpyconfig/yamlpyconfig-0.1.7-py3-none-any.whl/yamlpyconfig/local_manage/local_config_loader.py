from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import yaml

logger = logging.getLogger(__name__)
class LocalConfigLoader:
    """Local YAML configuration file loader."""

    def __init__(self, config_dir: Optional[str|Path] = None):
        """
        Initialize local_manage config loader.

        Args:
            config_dir: Directory containing config files. Defaults to current working directory.
        """
        if isinstance(config_dir, str):
            self.config_dir = Path(config_dir) if config_dir else Path.cwd()
        else:
            self.config_dir = config_dir

    @staticmethod
    def _candidate_paths(base: Path, name: str) -> Iterable[Path]:
        """Yield possible file paths for the given base directory and name.

        If the provided name has no YAML extension, try common variants.
        """
        p = base / name
        if p.suffix.lower() in {".yml", ".yaml"}:
            yield p
            return
        # Try with typical YAML suffixes
        yield p.with_suffix(".yaml")
        yield p.with_suffix(".yml")


    def load_local_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a local_manage YAML configuration file.

        Parameters
        - config_dir: The directory containing the configuration file.
        - filename: The configuration file name, with or without .yaml/.yml.

        Returns
        - A dictionary with the parsed YAML content (empty dict if file is empty).

        Raises
        - FileNotFoundError: If no matching file is found.
        - yaml.YAMLError: If the YAML content is invalid.
        """
        if not self.config_dir.exists() or not self.config_dir.is_dir():
            raise FileNotFoundError(f"Config directory does not exist: {self.config_dir}")

        for path in self._candidate_paths(self.config_dir, filename):
            try:
                return self.load_local_yaml_from_path(path)
            except FileNotFoundError:
                pass

        tried = ", ".join(str(p) for p in self._candidate_paths(self.config_dir, filename))
        raise FileNotFoundError(
            f"Config file not found. Tried: {tried}"
        )

    @staticmethod
    def load_local_yaml_from_path(path: Path) -> Dict[str, Any]:
        """Load a local_manage YAML configuration file from a given path.

        Parameters
        - path: The path to the configuration file.

        Returns
        - A dictionary with the parsed YAML content (empty dict if file is empty).

        Raises
        - FileNotFoundError: If the file does not exist.
        - yaml.YAMLError: If the YAML content is invalid.
        """
        if path.exists() and path.is_file():
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                return data or {}
            except Exception as e:
                logger.error(f"Failed to load config file `{path.name}`: {e}")
                raise
        raise FileNotFoundError(
            f"Config file not found. Tried: {path}"
        )