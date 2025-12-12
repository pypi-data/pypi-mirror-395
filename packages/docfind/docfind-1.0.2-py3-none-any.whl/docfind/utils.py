"""
Utility functions for docfind.

Provides file type detection, hash calculation, configuration management,
and other helper functions.
"""

import os
import hashlib
import mimetypes
import platform
import subprocess
import shutil
import json
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)


def get_config_dir() -> Path:
    """Get platform-specific config directory."""
    system = platform.system()

    if system == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:  # Linux and others
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))

    config_dir = base / "docfind"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_data_dir() -> Path:
    """Get platform-specific data directory."""
    system = platform.system()

    if system == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:  # Linux and others
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    data_dir = base / "docfind"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_default_db_path() -> Path:
    """Get default database file path."""
    return get_data_dir() / "docfind.db"


def get_config_path() -> Path:
    """Get configuration file path."""
    return get_config_dir() / "config.json"


class Config:
    """Application configuration manager."""

    DEFAULT_CONFIG = {
        "max_file_size": 100 * 1024 * 1024,  # 100 MB
        "threads": 4,
        "ignore_globs": [
            "*.pyc",
            "__pycache__",
            ".git",
            ".svn",
            "node_modules",
            ".venv",
            "venv",
            "*.log",
        ],
        "trust_external_tools": False,
        "ripgrep_path": "rg",
        "theme": "dark",
        "accent_color": "#3a7bd5",
        "db_path": str(get_default_db_path()),
    }

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config file (default: platform-specific)
        """
        self.config_path = config_path or get_config_path()
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    user_config = json.load(f)
                config = self.DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    def save(self):
        """Save configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self.data, f, indent=2)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.data[key] = value

    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dict syntax."""
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        """Set configuration value using dict syntax."""
        self.data[key] = value


def calculate_sha256(file_path: Path, chunk_size: int = 8192) -> str:
    """
    Calculate SHA256 hash of a file.

    Args:
        file_path: Path to file
        chunk_size: Size of chunks to read

    Returns:
        Hex digest of SHA256 hash
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()


def detect_file_type(file_path: Path) -> str:
    """
    Detect file type from extension.

    Args:
        file_path: Path to file

    Returns:
        File type/extension (lowercase, without dot)
    """
    suffix = file_path.suffix.lower()
    return suffix[1:] if suffix else "unknown"


def get_mime_type(file_path: Path) -> Optional[str]:
    """
    Get MIME type of a file.

    Args:
        file_path: Path to file

    Returns:
        MIME type string or None
    """
    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type


def is_text_file(file_path: Path, sample_size: int = 8192) -> bool:
    """
    Check if file appears to be a text file.

    Args:
        file_path: Path to file
        sample_size: Number of bytes to sample

    Returns:
        True if file appears to be text
    """
    try:
        with open(file_path, "rb") as f:
            sample = f.read(sample_size)

        # Check for null bytes (binary indicator)
        if b"\x00" in sample:
            return False

        # Try to decode as UTF-8
        try:
            sample.decode("utf-8")
            return True
        except UnicodeDecodeError:
            pass

        # Try other common encodings
        for encoding in ["latin-1", "cp1252", "iso-8859-1"]:
            try:
                sample.decode(encoding)
                return True
            except UnicodeDecodeError:
                continue

        return False

    except Exception:
        return False


def format_size(size: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def find_ripgrep() -> Optional[str]:
    """
    Find ripgrep executable.

    Returns:
        Path to rg executable or None if not found
    """
    rg_path = shutil.which("rg")
    if rg_path:
        logger.info(f"Found ripgrep at: {rg_path}")
    else:
        logger.warning("ripgrep not found in PATH")
    return rg_path


def check_ripgrep_version() -> Optional[str]:
    """
    Check ripgrep version.

    Returns:
        Version string or None if ripgrep not available
    """
    try:
        result = subprocess.run(
            ["rg", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # First line contains version
            version_line = result.stdout.strip().split("\n")[0]
            return version_line
        return None
    except Exception as e:
        logger.debug(f"Failed to check ripgrep version: {e}")
        return None


def should_ignore(file_path: Path, ignore_patterns: List[str]) -> bool:
    """
    Check if file should be ignored based on patterns.

    Args:
        file_path: Path to check
        ignore_patterns: List of glob patterns to ignore

    Returns:
        True if file should be ignored
    """
    from fnmatch import fnmatch

    path_str = str(file_path)
    name = file_path.name

    for pattern in ignore_patterns:
        # Check against full path and just the name
        if fnmatch(path_str, pattern) or fnmatch(name, pattern):
            return True

        # Check against any path component
        for part in file_path.parts:
            if fnmatch(part, pattern):
                return True

    return False


def is_system_path(path: Path) -> bool:
    """
    Check if path is a critical system path that should require confirmation.

    Args:
        path: Path to check

    Returns:
        True if path is a system path
    """
    system = platform.system()
    path_str = str(path.resolve()).lower()

    if system == "Windows":
        system_paths = [
            r"c:\windows",
            r"c:\program files",
            r"c:\program files (x86)",
            r"c:\programdata",
        ]
        return any(path_str.startswith(sp.lower()) for sp in system_paths)

    else:  # Unix-like
        system_paths = [
            "/bin",
            "/sbin",
            "/usr/bin",
            "/usr/sbin",
            "/etc",
            "/sys",
            "/proc",
        ]
        return any(path_str.startswith(sp) for sp in system_paths)


def setup_logging(
    log_file: Optional[Path] = None, level: int = logging.INFO, verbose: bool = False
) -> logging.Logger:
    """
    Setup application logging.

    Args:
        log_file: Optional log file path
        level: Logging level
        verbose: Enable verbose logging

    Returns:
        Root logger
    """
    if verbose:
        level = logging.DEBUG

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    if log_file:
        from logging.handlers import RotatingFileHandler

        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10 MB
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger
