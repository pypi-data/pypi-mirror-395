"""File and directory scanning functionality."""

import fnmatch
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .config import Config


# Project markers - files/directories that indicate a project root
PROJECT_MARKERS = {
    # Version control
    ".git",
    ".svn",
    ".hg",
    # Python
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements.txt",
    "Pipfile",
    "poetry.lock",
    # Node.js
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    # Rust
    "Cargo.toml",
    # Go
    "go.mod",
    # Java/Kotlin
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    # .NET
    "*.sln",
    "*.csproj",
    "*.fsproj",
    # Ruby
    "Gemfile",
    "Rakefile",
    # PHP
    "composer.json",
    # Build systems
    "Makefile",
    "CMakeLists.txt",
    "BUILD",
    "WORKSPACE",
    # iOS/macOS
    "*.xcodeproj",
    "*.xcworkspace",
    "Podfile",
    # Android
    "settings.gradle",
    # Misc
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}


@dataclass
class FileInfo:
    """Information about a file."""

    name: str
    path: Path
    size: int
    modified: datetime
    extension: str | None
    relative_path: str  # Path relative to target directory
    from_project: bool = False  # Whether this file is inside a detected project

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "path": str(self.path),
            "size": self.size,
            "modified": self.modified.isoformat(),
            "extension": self.extension,
            "relative_path": self.relative_path,
            "from_project": self.from_project,
        }


@dataclass
class DirectoryInfo:
    """Information about a directory."""

    name: str
    path: Path
    modified: datetime
    item_count: int | None
    sample_contents: list[str]
    relative_path: str  # Path relative to target directory
    is_project: bool = False  # Whether this directory is a detected project root

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "path": str(self.path),
            "modified": self.modified.isoformat(),
            "item_count": self.item_count,
            "sample_contents": self.sample_contents,
            "relative_path": self.relative_path,
            "is_project": self.is_project,
        }


class Scanner:
    """Scans a directory for files and subdirectories."""

    def __init__(self, config: Config) -> None:
        """Initialize the scanner with configuration."""
        self.config = config

    def _matches_ignore_pattern(self, path: Path) -> bool:
        """Check if a path matches any ignore pattern."""
        relative = str(path.relative_to(self.config.target_dir))

        for pattern in self.config.filters.ignore_patterns:
            if fnmatch.fnmatch(relative, pattern):
                return True
            if fnmatch.fnmatch(path.name, pattern):
                return True
        return False

    def _should_skip(self, item: Path) -> bool:
        """Check if an item should be skipped."""
        # Skip configured items
        if item.name in self.config.skip_items:
            return True

        # Skip hidden files if configured
        if self.config.skip_hidden and item.name.startswith("."):
            return True

        # Skip the output directory
        if self.config.output_dir and item == self.config.output_dir:
            return True

        # Skip the config directory
        if item == self.config.config_dir:
            return True

        # Skip if matches ignore pattern
        if self._matches_ignore_pattern(item):
            return True

        return False

    def is_project_directory(self, directory: Path) -> bool:
        """
        Check if a directory is a project root by looking for project markers.

        Returns True if the directory contains any project marker files/directories.
        """
        try:
            contents = {item.name for item in directory.iterdir()}
        except PermissionError:
            return False

        for marker in PROJECT_MARKERS:
            if "*" in marker:
                # Glob pattern
                for item in contents:
                    if fnmatch.fnmatch(item, marker):
                        return True
            else:
                if marker in contents:
                    return True

        return False

    def _scan_directory(
        self,
        directory: Path,
        current_depth: int,
        files: list[FileInfo],
        directories: list[DirectoryInfo],
        in_project: bool = False,
    ) -> None:
        """Recursively scan a directory."""
        try:
            items = list(directory.iterdir())
        except PermissionError:
            return

        for item in items:
            if self._should_skip(item):
                continue

            try:
                stat = item.stat()
                modified = datetime.fromtimestamp(stat.st_mtime)
                relative_path = str(item.relative_to(self.config.target_dir))

                if item.is_file():
                    # Apply filters
                    if not self.config.filters.matches_size(stat.st_size):
                        continue
                    ext = item.suffix.lower() if item.suffix else None
                    if not self.config.filters.matches_extension(ext):
                        continue
                    if not self.config.filters.matches_date(modified):
                        continue

                    files.append(
                        FileInfo(
                            name=item.name,
                            path=item,
                            size=stat.st_size,
                            modified=modified,
                            extension=ext,
                            relative_path=relative_path,
                            from_project=in_project,
                        )
                    )

                elif item.is_dir():
                    # Check if this is a project directory
                    is_project = self.is_project_directory(item)

                    # Get sample contents for better classification
                    sample_contents: list[str] = []
                    item_count: int | None = None

                    try:
                        contents = list(item.iterdir())
                        item_count = len(contents)
                        sample_contents = [c.name for c in contents[:5]]
                    except PermissionError:
                        pass

                    # Decision logic for whether to add directory vs recurse
                    should_add_directory = False
                    should_recurse = False

                    if self.config.flatten_mode:
                        # Flatten mode: projects stay as directories, non-projects get flattened
                        if is_project:
                            # Keep project as a unit - add to directories list
                            should_add_directory = current_depth == 0 and self.config.organize_directories
                            # Don't recurse into projects - we want to move them as a whole
                            should_recurse = False
                        else:
                            # Non-project directory - flatten by recursing without adding
                            should_add_directory = False
                            should_recurse = True
                    else:
                        # Normal mode: top-level dirs added, recurse based on depth
                        should_add_directory = current_depth == 0 and self.config.organize_directories
                        should_recurse = self.config.scan_depth == -1 or current_depth < self.config.scan_depth

                    if should_add_directory:
                        directories.append(
                            DirectoryInfo(
                                name=item.name,
                                path=item,
                                modified=modified,
                                item_count=item_count,
                                sample_contents=sample_contents,
                                relative_path=relative_path,
                                is_project=is_project,
                            )
                        )

                    if should_recurse:
                        # In flatten mode, non-projects at depth 0 get flattened
                        # but we still respect the scan_depth limit
                        if self.config.flatten_mode or self.config.scan_depth == -1 or current_depth < self.config.scan_depth:
                            self._scan_directory(
                                item,
                                current_depth + 1,
                                files,
                                directories,
                                in_project=in_project or is_project,
                            )

            except (PermissionError, OSError):
                continue

    def scan(self) -> tuple[list[FileInfo], list[DirectoryInfo]]:
        """Scan the target directory and return files and directories."""
        if not self.config.target_dir.exists():
            raise FileNotFoundError(
                f"Target directory does not exist: {self.config.target_dir}"
            )

        files: list[FileInfo] = []
        directories: list[DirectoryInfo] = []

        self._scan_directory(self.config.target_dir, 0, files, directories)

        return files, directories

    def get_stats(self) -> dict:
        """Get statistics about what will be scanned."""
        files, directories = self.scan()

        total_size = sum(f.size for f in files)
        extensions: dict[str, int] = {}
        for f in files:
            ext = f.extension or "(no extension)"
            extensions[ext] = extensions.get(ext, 0) + 1

        # Count projects
        project_count = sum(1 for d in directories if d.is_project)

        return {
            "total_files": len(files),
            "total_directories": len(directories),
            "project_directories": project_count,
            "total_size": total_size,
            "total_size_human": self._human_size(total_size),
            "extensions": dict(sorted(extensions.items(), key=lambda x: -x[1])),
            "flatten_mode": self.config.flatten_mode,
        }

    @staticmethod
    def _human_size(size: int) -> str:
        """Convert bytes to human readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"
