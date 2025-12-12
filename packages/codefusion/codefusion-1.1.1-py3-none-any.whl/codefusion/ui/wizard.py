import typing as t
from pathlib import Path
import logging

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

logger = logging.getLogger(__name__)

def run_wizard():
    """
    Runs the interactive configuration wizard.
    """
    if not RICH_AVAILABLE:
        print("Rich library not found. Wizard requires rich.")
        return

    console = Console()
    console.print(Panel("[bold blue]CodeFusion Configuration Wizard[/bold blue]", subtitle="Create your config"))

    config = {}

    # 1. Output File
    config['output'] = Prompt.ask("Default output file name", default="code_compilation.txt")

    # 2. Extensions
    exts = Prompt.ask("Default extensions to include (space separated)", default="py js html css")
    config['extensions'] = exts.split()

    # 3. Ignore File
    config['ignore_file'] = Prompt.ask("Ignore file name", default=".codeignore")

    # 4. Use Gitignore
    config['use_gitignore'] = Confirm.ask("Use .gitignore rules?", default=True)

    # 5. Include Empty
    config['include_empty'] = Confirm.ask("Include empty files?", default=False)

    # 6. Template
    config['template'] = Prompt.ask("Default template", choices=["default", "markdown", "html", "json"], default="default")

    # 7. Cache
    config['cache_size'] = IntPrompt.ask("Max cache size (MB)", default=50)
    config['cache_max_age'] = IntPrompt.ask("Max cache age (days)", default=7)

    # Generate TOML
    toml_content = f"""# CodeFusion Configuration

# Default output file
output = "{config['output']}"

# Extensions to include
extensions = {config['extensions']}

# Ignore file settings
ignore_file = "{config['ignore_file']}"
use_gitignore = {str(config['use_gitignore']).lower()}

# File filtering
include_empty = {str(config['include_empty']).lower()}

# Output format
template = "{config['template']}"

# Cache settings
cache_size = {config['cache_size']}
cache_max_age = {config['cache_max_age']}

# Parallel processing
workers = 4
"""

    output_path = Path("codefusion.toml")
    if output_path.exists():
        if not Confirm.ask(f"{output_path} already exists. Overwrite?", default=False):
            console.print("[yellow]Aborted.[/yellow]")
            return

    output_path.write_text(toml_content, encoding='utf-8')
    console.print(f"[green]✅ Configuration saved to {output_path.resolve()}[/green]")
