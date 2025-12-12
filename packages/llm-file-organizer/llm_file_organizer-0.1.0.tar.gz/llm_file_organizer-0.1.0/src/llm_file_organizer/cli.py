"""Command-line interface for LLM File Organizer."""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from . import __app_name__, __version__
from .classifier import Classifier
from .config import Config, ScanFilters, get_filter_presets, parse_size
from .organizer import Organizer
from .scanner import Scanner


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description="AI-powered filesystem cleanup tool. Organizes files and folders using LLM classification.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  llm-file-organizer                           # Interactive mode (recommended)
  llm-file-organizer ~/Downloads               # Organize specific directory
  llm-file-organizer --depth 2                 # Scan 2 levels deep
  llm-file-organizer --filter images           # Only organize images
  llm-file-organizer --execute                 # Classify and execute immediately
  llm-file-organizer --from-plan               # Execute from saved plan
  llm-file-organizer --undo                    # Undo last organization
  llm-file-organizer --provider anthropic      # Use Claude instead of GPT

Environment Variables:
  OPENAI_API_KEY      Required for OpenAI provider (default)
  ANTHROPIC_API_KEY   Required for Anthropic provider
  OLLAMA_HOST         Ollama server URL (default: http://localhost:11434)
        """,
    )

    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=None,
        help="Directory to organize (default: interactive prompt)",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output directory for organized files (default: TARGET/_Organized)",
    )

    # Action arguments (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode (default if no target specified)",
    )
    action_group.add_argument(
        "--execute",
        action="store_true",
        help="Classify with LLM and execute moves immediately",
    )
    action_group.add_argument(
        "--from-plan",
        action="store_true",
        help="Execute from saved move_plan.json (no LLM call)",
    )
    action_group.add_argument(
        "--undo",
        action="store_true",
        help="Undo the last organization",
    )

    # Scan options
    scan_group = parser.add_argument_group("Scan Options")
    scan_group.add_argument(
        "-d", "--depth",
        type=int,
        default=0,
        help="How many levels deep to scan (0=top only, -1=unlimited, default: 0)",
    )
    scan_group.add_argument(
        "--no-dirs",
        action="store_true",
        help="Don't organize directories, only files",
    )
    scan_group.add_argument(
        "--flatten",
        action="store_true",
        help="Extract files from subdirectories (projects detected and kept intact)",
    )
    scan_group.add_argument(
        "-f", "--filter",
        type=str,
        choices=list(get_filter_presets().keys()),
        default=None,
        help="Use a preset filter (images, documents, code, media, etc.)",
    )
    scan_group.add_argument(
        "--ext",
        type=str,
        default=None,
        help="Only include these extensions (comma-separated, e.g., 'py,js,ts')",
    )
    scan_group.add_argument(
        "--min-size",
        type=str,
        default=None,
        help="Minimum file size (e.g., '1MB', '500KB')",
    )
    scan_group.add_argument(
        "--max-size",
        type=str,
        default=None,
        help="Maximum file size (e.g., '100MB', '1GB')",
    )

    # LLM options
    llm_group = parser.add_argument_group("LLM Options")
    llm_group.add_argument(
        "-p", "--provider",
        type=str,
        choices=["openai", "anthropic", "ollama"],
        default="openai",
        help="LLM provider to use (default: openai)",
    )
    llm_group.add_argument(
        "-m", "--model",
        type=str,
        default=None,
        help="Model to use (default: provider's default model)",
    )
    llm_group.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Number of items per LLM batch (default: 50)",
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed progress",
    )
    output_group.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Minimal output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser


def build_filters(parsed: argparse.Namespace) -> ScanFilters:
    """Build scan filters from parsed arguments."""
    # Start with preset if specified
    if parsed.filter:
        presets = get_filter_presets()
        filters = presets.get(parsed.filter, ScanFilters())
    else:
        filters = ScanFilters()

    # Override with specific options
    if parsed.ext:
        filters.extensions = {
            e.strip().lstrip(".").lower()
            for e in parsed.ext.split(",")
            if e.strip()
        }

    if parsed.min_size:
        filters.min_size = parse_size(parsed.min_size)

    if parsed.max_size:
        filters.max_size = parse_size(parsed.max_size)

    return filters


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    # Load environment variables from .env file
    load_dotenv()

    parser = create_parser()
    parsed = parser.parse_args(args)

    # Interactive mode if no target specified and not a special action
    if parsed.target is None and not parsed.from_plan and not parsed.undo:
        parsed.interactive = True

    if parsed.interactive:
        try:
            from .interactive import run_interactive, show_results, console
        except ImportError:
            print("Error: Interactive mode requires 'rich' and 'InquirerPy' packages.")
            print("Install with: pip install rich InquirerPy")
            return 1

        result = run_interactive()
        if result is None:
            return 0

        config = result["config"]
        action = result["action"]
        classification_mode = result["classification_mode"]
        plan_file_name = result.get("plan_file")  # Optional specific plan file

        # Create organizer
        organizer = Organizer(config, verbose=True)

        # Handle undo action
        if action == "undo":
            console.print("\n[bold]Undoing last organization...[/bold]")
            success, errors = organizer.undo()
            if success > 0:
                console.print(f"\n[green]Restored {success} items![/green]")
            return 0

        # Handle resume from existing plan
        if action == "from_plan":
            try:
                # Load specific plan file if provided, otherwise latest
                plan_path = None
                if plan_file_name:
                    plan_path = config.config_dir / plan_file_name
                moves = organizer.load_plan(plan_path)
                success, errors = organizer.execute_moves(moves, dry_run=False)
                # Results shown by execute_moves
            except FileNotFoundError as e:
                console.print(f"[red]Error: {e}[/red]")
                return 1
            return 0

        # New classification flow
        console.print("\n[bold]Classifying...[/bold]")

        scanner = Scanner(config)
        try:
            files, directories = scanner.scan()
        except FileNotFoundError as e:
            console.print(f"[red]Error: {e}[/red]")
            return 1

        # Classify with selected mode
        classifier = Classifier(config, verbose=True, mode=classification_mode or "smart")
        try:
            file_classifications, dir_classifications = classifier.classify_all(
                files, directories
            )
        except (ImportError, ValueError) as e:
            console.print(f"[red]Error: {e}[/red]")
            return 1

        # Create move plan
        moves = organizer.create_move_plan(
            files, directories, file_classifications, dir_classifications
        )

        if not moves:
            console.print("[yellow]No moves to make![/yellow]")
            return 0

        # Save plan (always save, even if executing)
        plan_file = organizer.save_plan(moves)

        if action == "execute":
            console.print(f"\n[bold]Executing {len(moves)} moves...[/bold]")
            success, errors = organizer.execute_moves(moves, dry_run=False)
            show_results(success, errors, plan_file, executed=True)
        else:
            # Just save plan for later
            show_results(len(moves), 0, plan_file, executed=False)

        return 0

    # Non-interactive CLI mode
    target = parsed.target or Path.cwd()

    if not target.exists():
        print(f"Error: Target directory does not exist: {target}")
        return 1

    if not target.is_dir():
        print(f"Error: Target is not a directory: {target}")
        return 1

    config = Config(
        target_dir=target.resolve(),
        output_dir=parsed.output.resolve() if parsed.output else None,
        scan_depth=parsed.depth,
        organize_directories=not parsed.no_dirs,
        flatten_mode=parsed.flatten,
        filters=build_filters(parsed),
        llm_provider=parsed.provider,
        llm_model=parsed.model,
        batch_size=parsed.batch_size,
    )

    verbose = parsed.verbose and not parsed.quiet

    # Create organizer
    organizer = Organizer(config, verbose=verbose)

    # Handle undo
    if parsed.undo:
        if not parsed.quiet:
            print("LLM File Organizer - Undo")
            print("=" * 40)
        organizer.undo()
        return 0

    # Handle execute from plan
    if parsed.from_plan:
        if not parsed.quiet:
            print("LLM File Organizer - Execute from Plan")
            print("=" * 40)
        try:
            moves = organizer.load_plan()
            if not parsed.quiet:
                print(f"  {len(moves)} moves in plan")
            organizer.execute_moves(moves, dry_run=False)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return 1
        return 0

    # Normal flow: scan, classify, organize
    if not parsed.quiet:
        print("LLM File Organizer")
        print("=" * 40)
        print(f"Target: {config.target_dir}")
        print(f"Depth: {config.scan_depth}")
        print(f"Provider: {config.llm_provider} ({config.llm_model})")
        mode = "EXECUTE" if parsed.execute else "DRY RUN (saves plan)"
        print(f"Mode: {mode}")
        print()

    # Scan
    if verbose:
        print("Scanning directory...")

    scanner = Scanner(config)
    try:
        files, directories = scanner.scan()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    if verbose:
        print(f"  Found {len(files)} files and {len(directories)} directories")

    if not files and not directories:
        print("Nothing to organize!")
        return 0

    # Classify (CLI always uses smart mode by default)
    if verbose:
        print(f"\nClassifying with {config.llm_provider}...")

    classifier = Classifier(config, verbose=verbose, mode="smart")
    try:
        file_classifications, dir_classifications = classifier.classify_all(
            files, directories
        )
    except (ImportError, ValueError) as e:
        print(f"Error: {e}")
        return 1

    # Create move plan
    moves = organizer.create_move_plan(
        files, directories, file_classifications, dir_classifications
    )

    if not moves:
        print("No moves to make!")
        return 0

    # Save plan
    organizer.save_plan(moves)
    if verbose and not parsed.execute:
        print(f"\nPlan saved to: {config.plan_file}")
        print("Review it, then run with --from-plan to execute")

    # Execute or preview
    organizer.execute_moves(moves, dry_run=not parsed.execute)

    return 0


if __name__ == "__main__":
    sys.exit(main())
