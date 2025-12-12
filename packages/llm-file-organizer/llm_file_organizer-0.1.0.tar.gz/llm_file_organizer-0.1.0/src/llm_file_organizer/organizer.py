"""File organization and move/undo logic."""

import json
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import Config
from .plan_manager import PlanManager
from .scanner import DirectoryInfo, FileInfo

console = Console()


@dataclass
class MoveOperation:
    """Represents a single move operation."""

    item_type: str  # "file" or "directory"
    name: str
    source: Path
    destination: Path
    category: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.item_type,
            "name": self.name,
            "source": str(self.source),
            "destination": str(self.destination),
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MoveOperation":
        """Create from dictionary."""
        return cls(
            item_type=data["type"],
            name=data["name"],
            source=Path(data["source"]),
            destination=Path(data["destination"]),
            category=data["category"],
        )


class Organizer:
    """Handles file organization, moves, and undo operations."""

    def __init__(self, config: Config, verbose: bool = False) -> None:
        """Initialize the organizer."""
        self.config = config
        self.verbose = verbose
        self.plan_manager = PlanManager(config.config_dir, config.target_dir)
        self._current_plan_file: Path | None = None

    def create_move_plan(
        self,
        files: list[FileInfo],
        directories: list[DirectoryInfo],
        file_classifications: dict[str, list[str]],
        dir_classifications: dict[str, list[str]],
    ) -> list[MoveOperation]:
        """Create a plan of all moves to be made."""
        moves: list[MoveOperation] = []

        # Create lookups
        file_lookup = {f.name: f for f in files}
        dir_lookup = {d.name: d for d in directories}

        output_dir = self.config.output_dir
        if output_dir is None:
            output_dir = self.config.target_dir / "_Organized"

        # Plan file moves
        for category, names in file_classifications.items():
            for name in names:
                if name in file_lookup:
                    item = file_lookup[name]
                    dest_folder = output_dir / "Files" / category
                    moves.append(
                        MoveOperation(
                            item_type="file",
                            name=name,
                            source=item.path,
                            destination=dest_folder / name,
                            category=category,
                        )
                    )

        # Plan directory moves
        for category, names in dir_classifications.items():
            for name in names:
                if name in dir_lookup:
                    item = dir_lookup[name]
                    dest_folder = output_dir / "Folders" / category
                    moves.append(
                        MoveOperation(
                            item_type="directory",
                            name=name,
                            source=item.path,
                            destination=dest_folder / name,
                            category=category,
                        )
                    )

        return moves

    def preview_moves(self, moves: list[MoveOperation]) -> None:
        """Display a preview of planned moves."""
        # Count totals
        file_count = sum(1 for m in moves if m.item_type == "file")
        dir_count = sum(1 for m in moves if m.item_type == "directory")

        # Group by type and category
        file_categories: dict[str, list[str]] = defaultdict(list)
        dir_categories: dict[str, list[str]] = defaultdict(list)

        for move in moves:
            if move.item_type == "directory":
                dir_categories[move.category].append(move.name)
            else:
                file_categories[move.category].append(move.name)

        # Shorten destination path for display
        dest = str(self.config.output_dir)
        home = str(Path.home())
        if dest.startswith(home):
            dest = "~" + dest[len(home):]

        # Summary panel
        summary = Text()
        summary.append(f"{len(moves):,}", style="bold green")
        summary.append(" items to organize  ")
        summary.append(f"{file_count:,}", style="cyan")
        summary.append(" files  ")
        summary.append(f"{dir_count:,}", style="yellow")
        summary.append(" folders\n\n")
        summary.append("Destination: ", style="dim")
        summary.append(dest, style="white")

        console.print()
        console.print(Panel(summary, title="Organization Plan", border_style="blue"))

        # Create summary table
        table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
        table.add_column("Category", style="cyan")
        table.add_column("Files", justify="right", style="white")
        table.add_column("Folders", justify="right", style="white")
        table.add_column("Sample Items", style="dim")

        # Combine categories
        all_categories = set(file_categories.keys()) | set(dir_categories.keys())

        for category in sorted(all_categories):
            files = file_categories.get(category, [])
            dirs = dir_categories.get(category, [])

            file_str = str(len(files)) if files else "-"
            dir_str = str(len(dirs)) if dirs else "-"

            # Sample items (up to 3)
            samples = (files + dirs)[:3]
            sample_str = ", ".join(samples)
            if len(sample_str) > 50:
                sample_str = sample_str[:47] + "..."

            table.add_row(category, file_str, dir_str, sample_str)

        console.print()
        console.print(table)
        console.print()

    def save_plan(self, moves: list[MoveOperation], description: str = "") -> Path:
        """Save the move plan to a new timestamped JSON file. Returns the file path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_file = self.config.get_timestamped_plan_file(timestamp)

        # Count files and directories
        file_count = sum(1 for m in moves if m.item_type == "file")
        dir_count = sum(1 for m in moves if m.item_type == "directory")

        plan_data = {
            "created": datetime.now().isoformat(),
            "version": "1.0",
            "target_dir": str(self.config.target_dir),
            "output_dir": str(self.config.output_dir),
            "total_moves": len(moves),
            "file_count": file_count,
            "directory_count": dir_count,
            "moves": [m.to_dict() for m in moves],
        }

        plan_file.parent.mkdir(parents=True, exist_ok=True)
        with open(plan_file, "w", encoding="utf-8") as f:
            json.dump(plan_data, f, indent=2)

        # Register in plan index
        self.plan_manager.register_plan(plan_file, len(moves), description)

        # Store the current plan file path for reference
        self._current_plan_file = plan_file

        if self.verbose:
            print(f"\nPlan saved: {plan_file}")

        return plan_file

    def load_plan(self, plan_file: Path | None = None) -> list[MoveOperation]:
        """Load a move plan. Uses latest plan if no specific file given."""
        if plan_file is None:
            plan_file = self.config.get_latest_plan_file()

        if plan_file is None or not plan_file.exists():
            raise FileNotFoundError(
                f"No plan file found for {self.config.target_dir}\n"
                "Run llm-file-organizer first to generate a plan."
            )

        with open(plan_file, encoding="utf-8") as f:
            plan_data = json.load(f)

        # Store for reference
        self._current_plan_file = plan_file

        if self.verbose:
            created = plan_data.get('created', plan_data.get('timestamp', 'unknown'))
            if created and created != 'unknown':
                try:
                    dt = datetime.fromisoformat(created)
                    created = dt.strftime("%b %d, %Y at %I:%M%p").replace(" 0", " ").lower()
                except ValueError:
                    pass
            console.print(f"[dim]Plan:[/dim] {plan_file.name} [dim]({created})[/dim]")

        return [MoveOperation.from_dict(m) for m in plan_data["moves"]]

    def get_current_plan_file(self) -> Path | None:
        """Get the path to the current plan file being used."""
        return self._current_plan_file or self.config.get_latest_plan_file()

    def execute_moves(
        self, moves: list[MoveOperation], dry_run: bool = True
    ) -> tuple[int, int]:
        """Execute the planned moves. Returns (success_count, error_count)."""
        if dry_run:
            console.print("\n[dim]DRY RUN - No files will be moved[/dim]")
            self.preview_moves(moves)
            console.print("[dim]To execute, run with --execute or --from-plan[/dim]\n")
            return 0, 0

        self.preview_moves(moves)

        # Confirm with user
        console.print(
            Panel(
                "[bold yellow]This will move files and folders![/bold yellow]\n\n"
                "Type [bold]yes[/bold] to proceed, anything else to cancel.",
                title="Confirm",
                border_style="yellow",
            )
        )
        response = input("> ")

        if response.lower() != "yes":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return 0, 0

        # Mark plan as executing
        plan_file = self.get_current_plan_file()
        if plan_file:
            self.plan_manager.mark_executing(plan_file)

        # Save undo log BEFORE making any changes
        self._save_undo_log(moves)

        # Execute moves
        success_count = 0
        error_count = 0

        for move in moves:
            try:
                # Create destination directory if needed
                move.destination.parent.mkdir(parents=True, exist_ok=True)

                # Check if destination already exists
                if move.destination.exists():
                    if self.verbose:
                        print(f"  SKIP (exists): {move.name}")
                    continue

                # Check if source still exists
                if not move.source.exists():
                    if self.verbose:
                        print(f"  SKIP (source missing): {move.name}")
                    continue

                # Move the item
                shutil.move(str(move.source), str(move.destination))
                if self.verbose:
                    print(f"  MOVED: {move.name} -> {move.category}")
                success_count += 1

            except Exception as e:
                print(f"  ERROR: {move.name} - {e}")
                error_count += 1

        # Mark plan as executed
        if plan_file:
            self.plan_manager.mark_executed(plan_file, success_count, error_count)

        # Show completion message
        console.print()
        if error_count == 0:
            console.print(
                Panel(
                    f"[bold green]Successfully moved {success_count:,} items![/bold green]\n\n"
                    f"Run [cyan]llm-file-organizer --undo[/cyan] to revert if needed.",
                    title="Complete",
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    f"[green]Moved {success_count:,} items[/green], "
                    f"[red]{error_count:,} errors[/red]\n\n"
                    f"Run [cyan]llm-file-organizer --undo[/cyan] to revert if needed.",
                    title="Complete",
                    border_style="yellow",
                )
            )

        return success_count, error_count

    def _save_undo_log(self, moves: list[MoveOperation]) -> None:
        """Save the undo log before executing moves."""
        undo_data = {
            "timestamp": datetime.now().isoformat(),
            "moves": [m.to_dict() for m in moves],
        }

        self.config.undo_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config.undo_file, "w", encoding="utf-8") as f:
            json.dump(undo_data, f, indent=2)

        if self.verbose:
            print(f"\nUndo log saved to: {self.config.undo_file}")

    def undo(self) -> tuple[int, int]:
        """Undo the last organization. Returns (success_count, error_count)."""
        if not self.config.undo_file.exists():
            print("No undo log found. Nothing to undo.")
            return 0, 0

        with open(self.config.undo_file, encoding="utf-8") as f:
            undo_data = json.load(f)

        moves = [MoveOperation.from_dict(m) for m in undo_data["moves"]]

        print(f"Undo log from: {undo_data['timestamp']}")
        print(f"Will restore {len(moves)} items to original locations.")

        response = input("\nType 'yes' to undo, anything else to cancel: ")
        if response.lower() != "yes":
            print("Undo cancelled.")
            return 0, 0

        success_count = 0
        error_count = 0

        for move in moves:
            try:
                source = move.destination  # Current location
                dest = move.source  # Original location

                if not source.exists():
                    if self.verbose:
                        print(f"  SKIP (not found): {move.name}")
                    continue

                if dest.exists():
                    if self.verbose:
                        print(f"  SKIP (original exists): {move.name}")
                    continue

                shutil.move(str(source), str(dest))
                if self.verbose:
                    print(f"  RESTORED: {move.name}")
                success_count += 1

            except Exception as e:
                print(f"  ERROR: {move.name} - {e}")
                error_count += 1

        print(f"\nRestored {success_count} items, {error_count} errors")

        # Mark plan as undone
        if success_count > 0:
            self.plan_manager.mark_undone()

        # Offer to clean up empty directories
        response = input("\nRemove empty organization folders? (yes/no): ")
        if response.lower() == "yes":
            self._cleanup_empty_dirs(self.config.output_dir)

        return success_count, error_count

    def _cleanup_empty_dirs(self, path: Path | None) -> None:
        """Remove empty directories recursively."""
        if path is None or not path.exists():
            return

        for item in path.iterdir():
            if item.is_dir():
                self._cleanup_empty_dirs(item)

        try:
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                if self.verbose:
                    print(f"  Removed empty: {path}")
        except Exception as e:
            if self.verbose:
                print(f"  Could not remove {path}: {e}")
