"""Configuration management for LLM File Organizer."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal

LLMProvider = Literal["openai", "anthropic", "ollama"]


@dataclass
class ScanFilters:
    """Filters for what to include in the scan."""

    # File extensions to include (empty = all)
    extensions: set[str] = field(default_factory=set)

    # File extensions to exclude
    exclude_extensions: set[str] = field(default_factory=set)

    # Minimum file size in bytes (0 = no minimum)
    min_size: int = 0

    # Maximum file size in bytes (0 = no maximum)
    max_size: int = 0

    # Only files modified after this date
    modified_after: datetime | None = None

    # Only files modified before this date
    modified_before: datetime | None = None

    # Ignore patterns (glob-style, like .gitignore)
    ignore_patterns: list[str] = field(default_factory=list)

    def matches_size(self, size: int) -> bool:
        """Check if a file size matches the filter."""
        if self.min_size > 0 and size < self.min_size:
            return False
        if self.max_size > 0 and size > self.max_size:
            return False
        return True

    def matches_extension(self, ext: str | None) -> bool:
        """Check if a file extension matches the filter."""
        if ext is None:
            ext = ""
        ext = ext.lower().lstrip(".")

        if self.exclude_extensions and ext in self.exclude_extensions:
            return False
        if self.extensions and ext not in self.extensions:
            return False
        return True

    def matches_date(self, modified: datetime) -> bool:
        """Check if a modification date matches the filter."""
        if self.modified_after and modified < self.modified_after:
            return False
        if self.modified_before and modified > self.modified_before:
            return False
        return True


@dataclass
class Config:
    """Configuration settings for LLM File Organizer."""

    # Target directory to organize
    target_dir: Path = field(default_factory=Path.cwd)

    # Output directory for organized files (None = create _Organized in target)
    output_dir: Path | None = None

    # How many levels deep to scan (0 = only top level, -1 = unlimited)
    scan_depth: int = 0

    # Whether to organize directories as well as files
    organize_directories: bool = True

    # Flatten mode: extract files from non-project subdirectories
    # Projects (detected by markers like package.json, .git, etc.) stay intact
    flatten_mode: bool = False

    # LLM settings
    llm_provider: LLMProvider = "openai"
    llm_model: str | None = None

    # Processing settings
    batch_size: int = 50

    # Scan filters
    filters: ScanFilters = field(default_factory=ScanFilters)

    # Items to always skip
    skip_items: set[str] = field(
        default_factory=lambda: {
            ".DS_Store",
            ".localized",
            ".git",
            ".svn",
            ".hg",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            ".env",
        }
    )

    # Skip hidden files/directories
    skip_hidden: bool = True

    # Override app directory (for testing) - None means use default ~/.llm-file-organizer
    _app_dir: Path | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Set defaults after initialization."""
        if self.output_dir is None:
            self.output_dir = self.target_dir / "_Organized"

        if self.llm_model is None:
            self.llm_model = self.default_model_for_provider(self.llm_provider)

    @staticmethod
    def default_model_for_provider(provider: LLMProvider) -> str:
        """Get the default model for a provider."""
        defaults = {
            "openai": "gpt-5-mini",
            "anthropic": "claude-sonnet-4-20250514",
            "ollama": "llama3.2",
        }
        return defaults.get(provider, "gpt-5-mini")

    @staticmethod
    def get_app_dir() -> Path:
        """Get the application data directory (~/.llm-file-organizer)."""
        return Path.home() / ".llm-file-organizer"

    def _get_target_slug(self) -> str:
        """Create a safe directory name from the target path."""
        # Convert path to a safe slug: /Users/john/Downloads -> Users_john_Downloads
        parts = self.target_dir.resolve().parts
        # Skip the root "/" on Unix
        if parts and parts[0] == "/":
            parts = parts[1:]
        return "_".join(parts)

    @property
    def config_dir(self) -> Path:
        """Directory for config and log files for this target."""
        base = self._app_dir if self._app_dir else self.get_app_dir()
        return base / "plans" / self._get_target_slug()

    def get_timestamped_plan_file(self, timestamp: str | None = None) -> Path:
        """Get a timestamped plan file path."""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.config_dir / f"plan_{timestamp}.json"

    def get_latest_plan_file(self) -> Path | None:
        """Find the most recent plan file for this target."""
        if not self.config_dir.exists():
            return None
        plans = sorted(self.config_dir.glob("plan_*.json"), reverse=True)
        return plans[0] if plans else None

    def list_plans(self) -> list[Path]:
        """List all plan files for this target, newest first."""
        if not self.config_dir.exists():
            return []
        return sorted(self.config_dir.glob("plan_*.json"), reverse=True)

    @property
    def plan_file(self) -> Path:
        """Path to the latest plan file (for compatibility)."""
        latest = self.get_latest_plan_file()
        if latest:
            return latest
        # Return a new timestamped path if no plans exist
        return self.get_timestamped_plan_file()

    @property
    def undo_file(self) -> Path:
        """Path to the undo log file."""
        return self.config_dir / "undo_log.json"


def parse_size(size_str: str) -> int:
    """Parse a human-readable size string to bytes."""
    size_str = size_str.strip().upper()
    multipliers = {
        "B": 1,
        "KB": 1024,
        "MB": 1024 * 1024,
        "GB": 1024 * 1024 * 1024,
        "TB": 1024 * 1024 * 1024 * 1024,
    }

    for suffix, mult in multipliers.items():
        if size_str.endswith(suffix):
            try:
                return int(float(size_str[: -len(suffix)].strip()) * mult)
            except ValueError:
                pass

    try:
        return int(size_str)
    except ValueError:
        return 0


def get_filter_presets() -> dict[str, ScanFilters]:
    """Get preset filter configurations (created fresh to avoid stale dates)."""
    return {
        "images": ScanFilters(
            extensions={"jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "ico", "heic"}
        ),
        "documents": ScanFilters(
            extensions={"pdf", "doc", "docx", "txt", "md", "rtf", "odt", "xls", "xlsx", "ppt", "pptx"}
        ),
        "code": ScanFilters(
            extensions={"py", "js", "ts", "jsx", "tsx", "java", "c", "cpp", "h", "go", "rs", "rb"}
        ),
        "media": ScanFilters(
            extensions={"mp3", "mp4", "avi", "mov", "mkv", "wav", "flac", "m4a", "webm"}
        ),
        "archives": ScanFilters(
            extensions={"zip", "tar", "gz", "rar", "7z", "bz2", "xz"}
        ),
        "large_files": ScanFilters(
            min_size=100 * 1024 * 1024  # 100MB+
        ),
        "old_files": ScanFilters(
            modified_before=datetime.now() - timedelta(days=365)  # Older than 1 year
        ),
        "recent_files": ScanFilters(
            modified_after=datetime.now() - timedelta(days=30)  # Last 30 days
        ),
    }
