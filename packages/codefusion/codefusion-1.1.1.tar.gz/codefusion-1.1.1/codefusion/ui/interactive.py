# codefusion/ui/interactive.py
import typing as t
from pathlib import Path
import pyperclip
import logging
import sys

from ..core.app import CodeFusionApp
from .preview import display_file_preview

logger = logging.getLogger(__name__)

try:
    from rich.console import Console
    from rich.prompt import Confirm, Prompt, IntPrompt
    from rich.panel import Panel
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def interactive_compilation_flow(app: CodeFusionApp) -> bool:
    if not RICH_AVAILABLE:
        # Fallback for non-rich environments (if any, though it's a dependency)
        print("Rich library not found. Interactive mode degraded.")
        return simple_interactive_flow(app)

    console = Console()
    
    while True:
        # 1. Scan
        files_to_process, final_extensions = app.scan()

        if not files_to_process:
            console.print("[red]❌ No files found to process![/red]")
            # We allow user to go to options even if no files found, to maybe fix filters
            if not Confirm.ask("Go to options to adjust filters?", default=True):
                 return False
            if not interactive_options_menu(app, console):
                return False
            continue

        # 2. Preview
        display_file_preview(files_to_process, app.root_dir, final_extensions)

        # 3. Estimate Tokens (Rough approximation: 4 chars per token)
        total_size = sum(f.stat().st_size for f in files_to_process if f.exists())
        est_tokens = total_size / 4
        console.print(f"[dim]Estimated Tokens: ~{int(est_tokens):,}[/dim]")

        # 4. Prompt
        console.print("\n[bold]Actions:[/bold]")
        console.print("  [green]y[/green] : Proceed with compilation")
        console.print("  [yellow]o[/yellow] : Options (Filters, Output, Clipboard)")
        console.print("  [red]n[/red] : Cancel and Exit")

        choice = Prompt.ask("Choose an action", choices=["y", "n", "o"], default="y")

        if choice == "n":
            console.print("[yellow]⏸️  Compilation cancelled by user.[/yellow]")
            return False
        elif choice == "o":
            interactive_options_menu(app, console)
            # Loop back to scan/preview
            continue
        elif choice == "y":
            # Proceed
            success = app.writer.write(files_to_process, final_extensions)

            if success and app.copy_to_clipboard:
                if app.output_file and app.output_file.exists():
                    try:
                        content = app.output_file.read_text(encoding='utf-8')
                        pyperclip.copy(content)
                        console.print(Panel("[bold green]✅ Content copied to clipboard![/bold green]", title="Clipboard"))
                    except Exception as e:
                        console.print(f"[red]Failed to copy to clipboard: {e}[/red]")
                else:
                    console.print("[yellow]Output not file-based, cannot copy to clipboard automatically.[/yellow]")

            return success

def interactive_options_menu(app: CodeFusionApp, console) -> bool:
    """
    Displays and handles the options menu.
    """
    while True:
        console.clear()
        
        # Status Table
        from rich.table import Table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Option", style="cyan")
        table.add_column("Value", style="white")
        
        # Group 1: Output
        table.add_row("[bold]Output Settings[/bold]", "")
        table.add_row("[1] Output File", str(app.output_file or 'STDOUT'))
        table.add_row("[2] Clipboard", f"[{'green' if app.copy_to_clipboard else 'red'}]{'ON' if app.copy_to_clipboard else 'OFF'}[/]")
        table.add_row("[3] Template", app.writer.template)
        
        # Group 2: Filters
        table.add_row("", "")
        table.add_row("[bold]Filters[/bold]", "")
        ext_str = ", ".join(sorted(app.file_filter.user_extensions)) if app.file_filter.user_extensions else "Auto-detect"
        table.add_row("[4] Extensions", ext_str)
        table.add_row("[5] Include Empty", f"[{'green' if app.file_filter.include_empty else 'red'}]{'YES' if app.file_filter.include_empty else 'NO'}[/]")
        table.add_row("[6] Ignore File", app.ignore_manager.ignore_file_name)
        
        # Group 3: Features
        table.add_row("", "")
        table.add_row("[bold]Advanced Features[/bold]", "")
        table.add_row("[7] Resume Mode", f"[{'green' if app.writer.resume else 'red'}]{'ON' if app.writer.resume else 'OFF'}[/]")
        table.add_row("[8] Secret Detection", f"[{'green' if app.writer.detect_secrets else 'red'}]{'ON' if app.writer.detect_secrets else 'OFF'}[/]")

        console.print(Panel(table, title="[bold blue]⚙️  Configuration Options[/bold blue]", expand=False))

        console.print("\n[0] ↩️  Done / Back to Preview")
        console.print("[x] ❌ Exit Application")

        choice = Prompt.ask("Select an option", choices=["0", "x", "1", "2", "3", "4", "5", "6", "7", "8"], default="0")

        if choice == "0":
            break

        elif choice == "x":
            console.print("[yellow]Exiting application...[/yellow]")
            sys.exit(0)

        elif choice == "1":
            console.print("[dim](Leave empty to keep current)[/dim]")
            new_path = Prompt.ask("Enter new output path (or 'stdout')")
            if not new_path.strip():
                continue

            if new_path.lower() == 'stdout':
                app.output_file = None
                app.writer.output_file = None
                app.writer.to_stdout = True
            else:
                app.output_file = Path(new_path)
                app.writer.output_file = Path(new_path)
                app.writer.to_stdout = False
                app.ignore_manager.output_file = app.output_file

        elif choice == "2":
            app.copy_to_clipboard = not app.copy_to_clipboard

        elif choice == "3":
            new_template = Prompt.ask("Select template", choices=["default", "markdown", "html", "json"], default=app.writer.template)
            app.writer.template = new_template
            app.writer.renderer.template = new_template # Update renderer too if needed, though writer creates new one? No, writer has one.

        elif choice == "4":
            console.print("[dim](Leave empty to keep current, enter 'auto' for auto-detect)[/dim]")
            current = " ".join(sorted(app.file_filter.user_extensions)) if app.file_filter.user_extensions else ""
            new_exts = Prompt.ask("Enter extensions (space separated, e.g., 'py js')", default=current)

            if new_exts.strip().lower() == 'auto':
                app.file_filter.user_extensions = None
                app.scanner.file_filter.user_extensions = None
            elif new_exts.strip():
                ext_set = {f".{ext.lstrip('.')}" for ext in new_exts.split()}
                app.file_filter.user_extensions = ext_set
                app.scanner.file_filter.user_extensions = ext_set

        elif choice == "5":
            app.file_filter.include_empty = not app.file_filter.include_empty
            app.scanner.file_filter.include_empty = app.file_filter.include_empty

        elif choice == "6":
            console.print("[dim](Leave empty to keep current)[/dim]")
            new_ignore = Prompt.ask("Enter ignore file name", default=app.ignore_manager.ignore_file_name)
            if new_ignore.strip():
                app.ignore_manager.ignore_file_name = new_ignore.strip()
                app.ignore_manager._load_patterns()
        
        elif choice == "7":
            app.writer.resume = not app.writer.resume
            
        elif choice == "8":
            app.writer.detect_secrets = not app.writer.detect_secrets
            if app.writer.detect_secrets and not app.writer.secret_detector:
                from ..core.security import SecretDetector
                app.writer.secret_detector = SecretDetector()

    return True

def simple_interactive_flow(app: CodeFusionApp) -> bool:
    """Fallback for non-rich environments."""
    files_to_process, final_extensions = app.scan()
    if not files_to_process:
        print("❌ No files found to process!")
        return False

    display_file_preview(files_to_process, app.root_dir, final_extensions)
    
    response = input("\n🚀 Proceed with compilation? (Y/n): ").strip().lower()
    if response in ('', 'y', 'yes'):
        return app.writer.write(files_to_process, final_extensions)
    return False
