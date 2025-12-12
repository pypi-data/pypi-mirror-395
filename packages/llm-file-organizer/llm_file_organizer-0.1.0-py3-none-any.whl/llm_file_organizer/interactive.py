"""Interactive CLI for LLM File Organizer."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from prompt_toolkit.completion import PathCompleter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from . import __app_name__, __version__
from .config import Config, LLMProvider, ScanFilters, get_filter_presets, parse_size
from .plan_manager import PlanManager, get_all_targets_with_plans
from .scanner import Scanner

# Load .env at module import time so API keys are available
load_dotenv()

console = Console()


def print_banner() -> None:
    """Print the application banner."""
    console.print()
    logo = Text()
    logo.append("    ╦  ╦  ╔╦╗  ╔═╗┬┬  ┌─┐  ╔═╗┬─┐┌─┐┌─┐┌┐┌┬┌─┐┌─┐┬─┐\n", style="bold cyan")
    logo.append("    ║  ║  ║║║  ╠╣ ││  ├┤   ║ ║├┬┘│ ┬├─┤││││┌─┘├┤ ├┬┘\n", style="bold cyan")
    logo.append("    ╩═╝╩═╝╩ ╩  ╚  ┴┴─┘└─┘  ╚═╝┴└─└─┘┴ ┴┘└┘┴└─┘└─┘┴└─", style="bold cyan")
    console.print(logo)
    console.print()
    subtitle = Text()
    subtitle.append("    AI-Powered Filesystem Organizer  ", style="dim")
    subtitle.append(f"v{__version__}", style="cyan")
    console.print(subtitle)
    console.print()


def get_directory() -> Path:
    """Prompt user for target directory."""
    console.print("\n[bold]Step 1: Choose Directory[/bold]")

    home = Path.home()
    choices = []

    # Add common directories if they exist
    for name, path in [
        ("Desktop", home / "Desktop"),
        ("Downloads", home / "Downloads"),
        ("Documents", home / "Documents"),
        ("Current directory", Path.cwd()),
    ]:
        if path.exists():
            choices.append(Choice(value=path, name=f"{name} ({path})"))

    choices.append(Separator())
    choices.append(Choice(value="custom", name="Enter custom path..."))

    while True:
        result = inquirer.select(
            message="Which directory would you like to organize?",
            choices=choices,
            default=choices[0].value if choices else None,
            pointer="❯",
            qmark="",
        ).execute()

        if result == "custom":
            custom_path = inquirer.text(
                message="Enter full path:",
                qmark="",
                completer=PathCompleter(only_directories=True, expanduser=True),
            ).execute()
            path = Path(custom_path).expanduser().resolve()
            if path.exists() and path.is_dir():
                return path
            console.print(f"[red]Directory not found: {path}[/red]")
        else:
            return result


def get_scan_depth() -> int:
    """Prompt user for scan depth."""
    console.print("\n[bold]Step 2: Scan Depth[/bold]")

    choices = [
        Choice(value=0, name="Top level only (files directly in target)"),
        Choice(value=1, name="One level deep"),
        Choice(value=2, name="Two levels deep"),
        Choice(value=-1, name="Unlimited (scan all subdirectories)"),
    ]

    return inquirer.select(
        message="How deep should we scan?",
        choices=choices,
        default=0,
        pointer="❯",
        qmark="",
    ).execute()


def get_organize_directories() -> bool:
    """Ask if user wants to organize directories too."""
    console.print("\n[bold]Step 3: Organize Directories?[/bold]")

    return inquirer.confirm(
        message="Should we organize directories as well as files?",
        default=True,
        qmark="",
    ).execute()


def get_flatten_mode() -> bool:
    """Ask if user wants to flatten non-project directories."""
    console.print("\n[bold]Flatten Mode[/bold]")

    choices = [
        Choice(
            value=False,
            name="Keep structure - Organize directories as-is"
        ),
        Choice(
            value=True,
            name="Flatten - Extract files from subdirectories (projects stay intact)"
        ),
    ]

    return inquirer.select(
        message="How should we handle subdirectories?",
        choices=choices,
        default=False,
        pointer="❯",
        qmark="",
    ).execute()


def get_file_filters() -> ScanFilters:
    """Prompt user for file filters."""
    console.print("\n[bold]Step 4: File Filters[/bold]")

    presets = get_filter_presets()
    descriptions = {
        "images": "JPG, PNG, GIF, etc.",
        "documents": "PDF, DOC, TXT, etc.",
        "code": "PY, JS, TS, etc.",
        "media": "MP3, MP4, MOV, etc.",
        "archives": "ZIP, TAR, GZ, etc.",
        "large_files": "Files over 100MB",
        "old_files": "Modified over 1 year ago",
        "recent_files": "Modified in last 30 days",
    }

    choices = [Choice(value=None, name="No filter (organize all files)")]
    choices.append(Separator("── Presets ──"))

    for name, preset in presets.items():
        desc = descriptions.get(name, "")
        display = f"{name.replace('_', ' ').title()} ({desc})"
        choices.append(Choice(value=name, name=display))

    choices.append(Separator())
    choices.append(Choice(value="custom", name="Custom filter..."))

    result = inquirer.select(
        message="Filter which files to organize?",
        choices=choices,
        default=None,
        pointer="❯",
        qmark="",
    ).execute()

    if result is None:
        return ScanFilters()
    elif result == "custom":
        return get_custom_filter()
    else:
        return presets[result]


def get_custom_filter() -> ScanFilters:
    """Get custom filter settings from user."""
    console.print("\n[bold]Custom Filter Configuration[/bold]")

    filters = ScanFilters()

    # Extensions
    ext_input = inquirer.text(
        message="File extensions to include (comma-separated, empty for all):",
        default="",
        qmark="",
    ).execute()

    if ext_input.strip():
        filters.extensions = {
            e.strip().lstrip(".").lower()
            for e in ext_input.split(",")
            if e.strip()
        }

    # Min size
    min_size = inquirer.text(
        message="Minimum file size (e.g., 1MB, 500KB, empty for none):",
        default="",
        qmark="",
    ).execute()

    if min_size.strip():
        filters.min_size = parse_size(min_size)

    # Max size
    max_size = inquirer.text(
        message="Maximum file size (e.g., 100MB, 1GB, empty for none):",
        default="",
        qmark="",
    ).execute()

    if max_size.strip():
        filters.max_size = parse_size(max_size)

    return filters


def get_llm_provider() -> tuple[LLMProvider, str | None]:
    """Prompt user for LLM provider."""
    console.print("\n[bold]Step 5: AI Provider[/bold]")

    providers = [
        ("openai", "OpenAI", "OPENAI_API_KEY"),
        ("anthropic", "Anthropic", "ANTHROPIC_API_KEY"),
        ("ollama", "Ollama (local)", None),
    ]

    choices = []
    default_provider = None

    for key, name, env_var in providers:
        if env_var:
            has_key = bool(os.environ.get(env_var))
            status = "✓ API key found" if has_key else "✗ API key not set"
            display = f"{name} ({status})"
            if has_key and default_provider is None:
                default_provider = key
        else:
            display = f"{name} (no API key needed)"

        choices.append(Choice(value=key, name=display))

    if default_provider is None:
        default_provider = "openai"

    provider = inquirer.select(
        message="Which AI provider should we use?",
        choices=choices,
        default=default_provider,
        pointer="❯",
        qmark="",
    ).execute()

    # Ask for model
    default_model = Config.default_model_for_provider(provider)
    model = inquirer.text(
        message="Model to use:",
        default=default_model,
        qmark="",
    ).execute()

    return provider, model


def get_plan_manager(target_dir: Path) -> PlanManager:
    """Get a PlanManager for the given directory."""
    config = Config(target_dir=target_dir)
    return PlanManager(config.config_dir, target_dir)


def show_detailed_plan_list() -> None:
    """Show detailed list of all plans across all directories."""
    app_dir = Config.get_app_dir()
    all_targets = get_all_targets_with_plans(app_dir)

    if not all_targets:
        console.print("\n[yellow]No plans found.[/yellow]")
        return

    for target_dir, manager in all_targets:
        plans = manager.get_all_plans()
        if not plans:
            continue

        # Directory header
        display_path = str(target_dir).replace(str(Path.home()), "~")
        console.print(f"\n[bold cyan]{display_path}[/bold cyan]")

        # Plans table
        table = Table(box=None, show_header=True, padding=(0, 1))
        table.add_column("Status", width=12)
        table.add_column("Created", width=22)
        table.add_column("Moves", justify="right", width=6)
        table.add_column("Result", width=12)

        for plan in plans[:5]:
            result_str = ""
            if plan.success_count is not None:
                result_str = f"{plan.success_count} ok"
                if plan.error_count:
                    result_str += f", {plan.error_count} err"

            table.add_row(
                plan.format_status(),
                plan.format_created(),
                str(plan.total_moves),
                result_str,
            )

        console.print(table)

        if len(plans) > 5:
            console.print(f"  [dim]... and {len(plans) - 5} older plans[/dim]")


def get_classification_mode() -> str:
    """Ask user which classification mode to use."""
    console.print("\n[bold]Classification Mode[/bold]")

    choices = [
        Choice(
            value="smart",
            name="Smart mode (recommended) - Auto-classify known file types, LLM for the rest"
        ),
        Choice(
            value="full",
            name="Full LLM mode - Send everything to AI for smarter categorization"
        ),
    ]

    return inquirer.select(
        message="How should we classify your files?",
        choices=choices,
        default="smart",
        pointer="❯",
        qmark="",
    ).execute()


def get_post_classification_action() -> str:
    """Ask user what to do after classification."""
    console.print()

    choices = [
        Choice(value="execute", name="Execute now - Move files immediately"),
        Choice(value="save", name="Save plan for later - Review and run when ready"),
    ]

    return inquirer.select(
        message="What would you like to do with this plan?",
        choices=choices,
        default="execute",
        pointer="❯",
        qmark="",
    ).execute()


def run_interactive() -> dict | None:
    """
    Run the interactive configuration wizard.

    Returns a dict with:
        - config: Config object
        - action: 'execute', 'save', or 'from_plan'
        - classification_mode: 'smart' or 'full'
    Or None if cancelled.
    """
    try:
        return _run_interactive_inner()
    except KeyboardInterrupt:
        console.print("\n")
        console.print("[yellow]Cancelled by user.[/yellow]")
        return None


def show_status_dashboard() -> None:
    """Show a dashboard of all plans across all directories."""
    app_dir = Config.get_app_dir()
    all_targets = get_all_targets_with_plans(app_dir)

    if not all_targets:
        console.print("[dim]No existing plans found.[/dim]")
        return

    # Count totals
    total_pending = 0
    total_undoable = 0

    table = Table(title="Your Organization Plans", box=None)
    table.add_column("Directory", style="cyan", no_wrap=True)
    table.add_column("Pending", justify="right", width=8)
    table.add_column("Undoable", justify="right", width=8)
    table.add_column("Total", justify="right", width=8)

    for target_dir, manager in all_targets:
        plans = manager.get_all_plans()
        pending = len([p for p in plans if p.status == "pending"])
        undoable = len([p for p in plans if p.can_undo])

        total_pending += pending
        total_undoable += undoable

        # Shorten path for display
        display_path = str(target_dir)
        home = str(Path.home())
        if display_path.startswith(home):
            display_path = "~" + display_path[len(home):]

        pending_str = str(pending) if pending else "-"
        undoable_str = str(undoable) if undoable else "-"

        table.add_row(display_path, pending_str, undoable_str, str(len(plans)))

    console.print()
    console.print(table)

    # Summary line
    summary_parts = []
    if total_pending:
        summary_parts.append(f"[green]{total_pending} pending[/green]")
    if total_undoable:
        summary_parts.append(f"[yellow]{total_undoable} undoable[/yellow]")
    if summary_parts:
        console.print(f"\n  {', '.join(summary_parts)}")
    console.print()


def get_global_action() -> tuple[str, Path | None, str | None]:
    """
    Show main menu with all available actions.
    Returns (action, target_dir or None, plan_file or None).
    """
    app_dir = Config.get_app_dir()
    all_targets = get_all_targets_with_plans(app_dir)

    choices = []

    # Collect pending plans across all directories
    pending_plans: list[tuple[Path, PlanManager, str, int]] = []
    undoable_plans: list[tuple[Path, PlanManager, str, int]] = []

    for target_dir, manager in all_targets:
        for plan in manager.get_pending_plans():
            pending_plans.append((target_dir, manager, plan.file, plan.total_moves))
        undoable = manager.get_undoable_plan()
        if undoable:
            undoable_plans.append((target_dir, manager, undoable.file, undoable.success_count or 0))

    # Add pending plan options
    if pending_plans:
        if len(pending_plans) == 1:
            target, _, plan_file, moves = pending_plans[0]
            display = str(target).replace(str(Path.home()), "~")
            choices.append(Choice(
                value=f"execute:{target}:{plan_file}",
                name=f"Execute pending plan: {display} ({moves} moves)"
            ))
        else:
            choices.append(Choice(
                value="execute_menu",
                name=f"Execute a pending plan ({len(pending_plans)} available)"
            ))

    # Add undo options
    if undoable_plans:
        if len(undoable_plans) == 1:
            target, _, plan_file, count = undoable_plans[0]
            display = str(target).replace(str(Path.home()), "~")
            choices.append(Choice(
                value=f"undo:{target}:{plan_file}",
                name=f"Undo last execution: {display} ({count} items)"
            ))
        else:
            choices.append(Choice(
                value="undo_menu",
                name=f"Undo an execution ({len(undoable_plans)} available)"
            ))

    # View all plans option if any exist
    if all_targets:
        choices.append(Choice(value="manage", name="View/manage all plans"))
        choices.append(Separator())

    # Always show new scan option
    choices.append(Choice(value="new", name="Organize a new directory"))
    choices.append(Choice(value="quit", name="Exit"))

    result = inquirer.select(
        message="What would you like to do?",
        choices=choices,
        pointer="❯",
        qmark="",
    ).execute()

    # Parse result
    if result.startswith("execute:") or result.startswith("undo:"):
        parts = result.split(":", 2)
        action = parts[0]
        target_dir = Path(parts[1])
        plan_file = parts[2]
        return action, target_dir, plan_file

    return result, None, None


def show_pending_menu() -> tuple[str, Path | None, str | None]:
    """Show menu to select from multiple pending plans."""
    app_dir = Config.get_app_dir()
    all_targets = get_all_targets_with_plans(app_dir)

    choices = []
    for target_dir, manager in all_targets:
        for plan in manager.get_pending_plans():
            display = str(target_dir).replace(str(Path.home()), "~")
            choices.append(Choice(
                value=f"{target_dir}:{plan.file}",
                name=f"{display} - {plan.total_moves} moves ({plan.format_created()})"
            ))

    choices.append(Separator())
    choices.append(Choice(value="back", name="Back"))

    result = inquirer.select(
        message="Select a plan to execute:",
        choices=choices,
        pointer="❯",
        qmark="",
    ).execute()

    if result == "back":
        return "back", None, None

    parts = result.split(":", 1)
    return "execute", Path(parts[0]), parts[1]


def show_undo_menu() -> tuple[str, Path | None, str | None]:
    """Show menu to select from multiple undoable plans."""
    app_dir = Config.get_app_dir()
    all_targets = get_all_targets_with_plans(app_dir)

    choices = []
    for target_dir, manager in all_targets:
        plan = manager.get_undoable_plan()
        if plan:
            display = str(target_dir).replace(str(Path.home()), "~")
            choices.append(Choice(
                value=f"{target_dir}:{plan.file}",
                name=f"{display} - {plan.success_count} items ({plan.format_created()})"
            ))

    choices.append(Separator())
    choices.append(Choice(value="back", name="Back"))

    result = inquirer.select(
        message="Select an execution to undo:",
        choices=choices,
        pointer="❯",
        qmark="",
    ).execute()

    if result == "back":
        return "back", None, None

    parts = result.split(":", 1)
    return "undo", Path(parts[0]), parts[1]


def _run_interactive_inner() -> dict | None:
    """Inner function for interactive wizard (allows clean Ctrl+C handling)."""
    print_banner()

    # Show status dashboard first
    show_status_dashboard()

    # Main action loop
    while True:
        action, target_dir, plan_file = get_global_action()

        if action == "quit":
            console.print("[yellow]Goodbye![/yellow]")
            return None

        if action == "execute_menu":
            action, target_dir, plan_file = show_pending_menu()
            if action == "back":
                continue

        if action == "undo_menu":
            action, target_dir, plan_file = show_undo_menu()
            if action == "back":
                continue

        if action == "execute" and target_dir and plan_file:
            config = Config(target_dir=target_dir)
            return {
                "config": config,
                "action": "from_plan",
                "plan_file": plan_file,
                "classification_mode": None,
            }

        if action == "undo" and target_dir:
            config = Config(target_dir=target_dir)
            return {
                "config": config,
                "action": "undo",
                "plan_file": plan_file,
                "classification_mode": None,
            }

        if action == "manage":
            # Show detailed plan list for all directories
            show_detailed_plan_list()
            continue

        if action == "new":
            # Break to continue with fresh scan flow
            break

    # New scan flow
    target_dir = get_directory()
    config = Config(target_dir=target_dir)

    # Step 3: New scan - gather configuration
    scan_depth = get_scan_depth()
    organize_dirs = get_organize_directories()

    # Ask about flatten mode if scanning deeper than top level
    flatten_mode = False
    if scan_depth != 0:
        flatten_mode = get_flatten_mode()

    filters = get_file_filters()

    # Update config with scan settings
    config.scan_depth = scan_depth
    config.organize_directories = organize_dirs
    config.flatten_mode = flatten_mode
    config.filters = filters

    # Step 4: Show scan preview
    console.print("\n[bold]Scanning...[/bold]")
    scanner = Scanner(config)
    stats = scanner.get_stats()

    _show_scan_stats(config, stats)

    if stats["total_files"] == 0 and stats["total_directories"] == 0:
        console.print("\n[yellow]No files or directories found matching your criteria.[/yellow]")
        return None

    # Step 5: Classification mode
    classification_mode = get_classification_mode()

    # Step 6: AI Provider (only ask if we'll use LLM)
    need_full_llm = classification_mode == "full"
    has_unknown_files = _has_unknown_extensions(stats.get("extensions", {}))

    if need_full_llm or has_unknown_files or stats["total_directories"] > 0:
        provider, model = get_llm_provider()
        config.llm_provider = provider
        config.llm_model = model

    # Step 7: What to do after classification
    post_action = get_post_classification_action()

    return {
        "config": config,
        "action": post_action,  # 'execute' or 'save'
        "classification_mode": classification_mode,
    }


def _show_scan_stats(config: Config, stats: dict) -> None:
    """Display scan statistics."""
    table = Table(show_header=False, box=None)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Target Directory", str(config.target_dir))
    table.add_row("Scan Depth", str(config.scan_depth) if config.scan_depth >= 0 else "Unlimited")
    table.add_row("Files Found", str(stats["total_files"]))
    table.add_row("Directories Found", str(stats["total_directories"]))
    table.add_row("Total Size", stats["total_size_human"])

    console.print()
    console.print(table)

    # Show top extensions
    if stats["extensions"]:
        console.print("\n[bold]Top File Types:[/bold]")
        for ext, count in list(stats["extensions"].items())[:8]:
            console.print(f"  {ext}: {count}")


def _has_unknown_extensions(extensions: dict) -> bool:
    """Check if there are files with unknown extensions that need LLM."""
    from .classifier import EXTENSION_TO_CATEGORY
    for ext in extensions.keys():
        if ext.lower() not in EXTENSION_TO_CATEGORY:
            return True
    return False


def show_results(success: int, errors: int, plan_file: Path, executed: bool = False) -> None:
    """Show the results of the organization."""
    if executed:
        if success > 0:
            console.print(
                Panel(
                    f"[green]Successfully moved {success} items![/green]\n\n"
                    f"Run [cyan]llm-file-organizer --undo[/cyan] to revert if needed.",
                    title="Complete",
                    border_style="green",
                )
            )
        else:
            console.print(
                Panel(
                    f"[yellow]No items were moved.[/yellow]\n"
                    f"Errors: {errors}",
                    title="Complete",
                    border_style="yellow",
                )
            )
    elif success > 0:
        console.print(
            Panel(
                f"[green]Plan created with {success} moves![/green]\n\n"
                f"Plan saved to: {plan_file}\n\n"
                f"To execute later, run:\n"
                f"  [cyan]lfo {plan_file.parent.parent} --from-plan[/cyan]\n\n"
                f"Or just run [cyan]lfo[/cyan] and choose 'Resume from saved plan'",
                title="Plan Saved",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                f"[yellow]No moves to plan.[/yellow]",
                title="Complete",
                border_style="yellow",
            )
        )
