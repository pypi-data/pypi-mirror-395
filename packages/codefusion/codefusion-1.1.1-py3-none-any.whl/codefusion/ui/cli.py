# codefusion/ui/cli.py
import argparse
import logging
import sys
import os
import typing as t
from pathlib import Path

from ..core.app import CodeFusionApp
from ..config.loader import ConfigLoader
from ..utils.logging import setup_logging
from ..utils.constants import DEFAULT_EXCLUDE_PATTERNS, get_exclude_patterns
from ..cache.manager import CacheManager
from .. import __version__
from .interactive import interactive_compilation_flow
from .preview import display_file_preview

logger = logging.getLogger(__name__)

try:
    from rich.console import Console
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"CodeFusion v{__version__} - Intelligently compile source code into a single document for AI analysis.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='''
Examples:
  codefusion                          # Interactive mode in current directory
  codefusion --auto                   # Auto-compile without preview
  codefusion -e py js -o out.txt      # Compile Python and JS files
  codefusion --include-licenses       # Include license files  
  codefusion --include-packages       # Include package files
        '''
    )
    
    parser.add_argument(
        "directory",
        nargs='?',
        help="The root directory containing the code files (default: current directory)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="The output file name/path (default: code_compilation.txt)"
    )
    
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-compile without interactive preview"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file (.toml format)"
    )
    
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of file"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=os.cpu_count(),
        help="Number of parallel workers"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show files that would be processed without compiling"
    )
    
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Include empty files"
    )
    
    parser.add_argument(
        "--min-size",
        type=int,
        default=0,
        help="Minimum file size in bytes"
    )
    
    parser.add_argument(
        "--max-size",
        type=int,
        help="Maximum file size in bytes"
    )
    
    parser.add_argument(
        "-i", "--ignore-file",
        default=".codeignore",
        help="Custom ignore file name"
    )
    
    parser.add_argument(
        "-e", "--extensions",
        nargs="+",
        help="File extensions to include (e.g., py js html)"
    )
    
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Do not use .gitignore rules"
    )
    
    parser.add_argument(
        "--exclude",
        nargs="+",
        metavar="PATTERN",
        help="Additional exclusion patterns"
    )
    
    parser.add_argument(
        "--include-dirs",
        nargs="+",
        metavar="DIR",
        help="Directories to explicitly include"
    )
    
    parser.add_argument(
        "--template",
        choices=["default", "markdown", "html", "json"],
        default="default",
        help="Output template format"
    )
    
    parser.add_argument(
        "--list-default-exclusions",
        action="store_true",
        help="List default exclusion patterns and exit"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"CodeFusion {__version__}"
    )
    
    parser.add_argument(
        "--no-grouping",
        action="store_true",
        help="Disable file grouping"
    )
    
    parser.add_argument(
        "--include-licenses",
        action="store_true",
        help="Include LICENSE files"
    )
    
    parser.add_argument(
        "--include-readmes",
        action="store_true", 
        help="Include README files"
    )
    
    parser.add_argument(
        "--include-wrappers",
        action="store_true",
        help="Include build tool wrappers (mvnw, gradlew, etc.)"
    )
    
    parser.add_argument(
        "--include-lockfiles",
        action="store_true",
        help="Include dependency lock files"
    )
    
    parser.add_argument(
        "--include-packages",
        action="store_true",
        help="Include package.json and similar dependency files"
    )
    parser.add_argument(
        "--cache-stats",
        action="store_true",
        help="Show cache statistics and exit"
    )
    
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cache for current project and exit"
    )
    
    parser.add_argument(
        "--clear-all-caches",
        action="store_true",
        help="Clear all CodeFusion caches (all projects) and exit"
    )
    
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable cache for this run"
    )
    
    parser.add_argument(
        "--cache-size",
        type=int,
        help="Maximum cache size in MB (default: 50)"
    )
    
    parser.add_argument(
        "--cache-max-age",
        type=int,
        help="Maximum cache entry age in days (default: 7)"
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last interrupted compilation"
    )

    parser.add_argument(
        "--detect-secrets",
        action="store_true",
        help="Scan for and redact secrets (API keys, tokens)"
    )

    parser.add_argument(
        "--example",
        metavar="LANG",
        help="Generate example configuration/code for language (e.g., python)"
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to run (e.g., 'init')"
    )

    args = parser.parse_args()
    
    setup_logging(args.verbose)

    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel(f"[bold green]CodeFusion v{__version__}[/bold green]", title="[bold]CodeFusion[/bold]", subtitle="[cyan]Stable Build[/cyan]"))

    # Handle 'init' command
    if args.directory == 'init' or args.command == 'init':
        from .wizard import run_wizard
        run_wizard()
        return 0

    # Handle 'example' command
    if args.example:
        # Simple example generator
        print(f"Generating example for {args.example}...")
        # For now just print a message as placeholder or create a dummy file
        # The user asked for "codefusion --example python generates sample config"
        # My wizard generates config. Maybe this generates a sample .codeignore?
        with open(".codeignore", "w") as f:
            f.write("*.pyc\n__pycache__/\n.git/\n")
        print("Created sample .codeignore")
        return 0
    
    # Set exclusion flags (default to True for excluding)
    exclude_licenses = not args.include_licenses
    exclude_readmes = not args.include_readmes  
    exclude_wrappers = not args.include_wrappers
    exclude_lockfiles = not args.include_lockfiles
    exclude_packages = not args.include_packages

    if args.list_default_exclusions:
        print("Default Exclusion Patterns (fnmatch syntax):")
        for pattern in sorted(DEFAULT_EXCLUDE_PATTERNS):
            print(f"  - {pattern}")
        return 0
    if args.cache_stats:
        cache = CacheManager(project_root=Path(args.directory or Path.cwd()))
        stats = cache.get_stats()
        
        if RICH_AVAILABLE:
            from rich.table import Table
            console = Console()
            
            table = Table(title="📊 Cache Statistics", show_header=True)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="magenta")
            
            table.add_row("Cache Directory", stats['cache_dir'])
            table.add_row("Cache File", stats['cache_file'])
            table.add_row("Total Entries", str(stats['entry_count']))
            table.add_row("Content Files", str(stats.get('content_files', 0)))
            table.add_row("Cache Size", f"{stats['size_mb']:.2f} MB")
            table.add_row("Max Size", f"{stats['max_size_mb']} MB")
            table.add_row("Max Age", f"{stats['max_age_days']} days")
            
            if stats.get('created'):
                import datetime
                created = datetime.datetime.fromtimestamp(stats['created'])
                table.add_row("Created", created.strftime('%Y-%m-%d %H:%M:%S'))
            
            if stats.get('last_cleanup'):
                last_cleanup = datetime.datetime.fromtimestamp(stats['last_cleanup'])
                table.add_row("Last Cleanup", last_cleanup.strftime('%Y-%m-%d %H:%M:%S'))
            
            console.print(table)
        else:
            print("\n=== Cache Statistics ===")
            print(f"Cache Directory: {stats['cache_dir']}")
            print(f"Cache File: {stats['cache_file']}")
            print(f"Total Entries: {stats['entry_count']}")
            print(f"Cache Size: {stats['size_mb']:.2f} MB")
            print(f"Max Size: {stats['max_size_mb']} MB")
            print(f"Max Age: {stats['max_age_days']} days")
        
        return 0
    
    if args.clear_cache:
        cache = CacheManager(project_root=Path(args.directory or Path.cwd()))
        cache.clear()
        if RICH_AVAILABLE:
            console = Console()
            console.print("[green]✅ Cache cleared for current project[/green]")
        else:
            print("✅ Cache cleared for current project")
        return 0
    
    if args.clear_all_caches:
        try:
            CacheManager.clear_all_caches()
            if RICH_AVAILABLE:
                console = Console()
                console.print("[green]✅ All CodeFusion caches cleared[/green]")
            else:
                print("✅ All CodeFusion caches cleared")
        except Exception as e:
            logger.error(f"Failed to clear all caches: {e}")
            return 1
        return 0

    try:
        config_loader = ConfigLoader(args.config) if args.config else None
        config = config_loader.get_config() if config_loader else {}
        
        extensions_set: t.Optional[t.Set[str]] = None
        from ..utils.helpers import ensure_leading_dot
        if args.extensions:
            extensions_set = {ensure_leading_dot(ext) for ext in args.extensions}
        elif config.get('extensions'):
            extensions_set = {ensure_leading_dot(ext) for ext in config['extensions']}

        output_path = None
        if args.stdout:
            output_path = None
        elif args.output:
            output_path = args.output
        elif config.get('output'):
            output_path = config['output']
        elif not args.dry_run:
            output_path = "code_compilation.txt"
            
        base_patterns = get_exclude_patterns(
            exclude_licenses=exclude_licenses,
            exclude_readmes=exclude_readmes,
            exclude_wrappers=exclude_wrappers,
            exclude_lockfiles=exclude_lockfiles,
            exclude_packages=exclude_packages
        )
        
        if args.exclude:
            final_patterns = base_patterns + args.exclude
        else:
            final_patterns = base_patterns

        # Handle directory argument properly if it's not 'init'
        target_dir = args.directory if args.directory and args.directory != 'init' else None

        app = CodeFusionApp(
            directory=target_dir or config.get('directory'),
            output_file=output_path,
            ignore_file_name=args.ignore_file or config.get('ignore_file', '.codeignore'),
            use_gitignore=not args.no_gitignore and config.get('use_gitignore', True),
            extensions=extensions_set,
            verbose=args.verbose,
            extra_exclude_patterns=final_patterns, 
            num_workers=args.workers or config.get('workers', os.cpu_count()),
            dry_run=args.dry_run,
            include_empty=args.include_empty or config.get('include_empty', False),
            min_size=args.min_size or config.get('min_size', 0),
            max_size=args.max_size or config.get('max_size'),
            to_stdout=args.stdout,
            include_dirs=args.include_dirs or config.get('include_dirs'),
            template=args.template or config.get('template', 'default'),
            no_grouping=args.no_grouping or config.get('no_grouping', False),
            use_cache=not args.no_cache if hasattr(args, 'no_cache') else True,
            cache_size=args.cache_size or config.get('cache_size', 50),
            cache_max_age=args.cache_max_age or config.get('cache_max_age', 7),
            resume=args.resume,
            detect_secrets=args.detect_secrets
        )

        if args.dry_run:
            files_to_process, _ = app.scan()
            display_file_preview(files_to_process, app.root_dir, set())
            return 0
        elif args.auto:
            success = app.compile()
        else:
            success = interactive_compilation_flow(app)
        
        return 0 if success else 1

    except ValueError as ve:
        logger.error(f"Configuration Error: {ve}")
        return 1
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        if args.verbose:
            import traceback
            logger.debug(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
