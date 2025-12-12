# codefusion/ui/preview.py
import typing as t
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree

def display_file_preview(files: t.List[Path], root_dir: Path, extensions: t.Set[str]) -> None:
    try:
        from rich.console import Console
        RICH_AVAILABLE = True
    except ImportError:
        RICH_AVAILABLE = False

    if not RICH_AVAILABLE:
        print(f"\nFiles to be processed ({len(files)}):")
        for f in files[:20]:
            print(f"  - {f.relative_to(root_dir)}")
        if len(files) > 20:
            print(f"  ... and {len(files) - 20} more files")
        return

    console = Console()
    
    tree = Tree(f"📁 [bold blue]{root_dir.name}[/bold blue] ({len(files)} files)")
    
    dir_groups = {}
    for file_path in files:
        rel_path = file_path.relative_to(root_dir)
        dir_name = str(rel_path.parent) if rel_path.parent != Path('.') else "."
        if dir_name not in dir_groups:
            dir_groups[dir_name] = []
        dir_groups[dir_name].append(rel_path.name)
    
    dirs_shown = 0
    for dir_name, files_in_dir in sorted(dir_groups.items()):
        if dirs_shown >= 10:
            tree.add(f"... and {len(dir_groups) - 10} more directories")
            break
        
        if dir_name == ".":
            dir_node = tree.add("📄 Root files")
        else:
            dir_node = tree.add(f"📁 {dir_name}")
        
        for file_name in files_in_dir[:5]:
            file_ext = Path(file_name).suffix
            emoji = "🐍" if file_ext == ".py" else "📄"
            dir_node.add(f"{emoji} {file_name}")
        
        if len(files_in_dir) > 5:
            dir_node.add(f"... and {len(files_in_dir) - 5} more files")
        dirs_shown += 1
    
    console.print("\n")
    console.print(Panel(tree, title="Files to Process", title_align="left", border_style="green"))
    
    table = Table(title="Compilation Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Files", str(len(files)))
    table.add_row("Extensions", ", ".join(sorted(extensions)) if extensions else "Auto-detected")
    table.add_row("Root Directory", str(root_dir))
    
    total_size = sum(f.stat().st_size for f in files if f.exists())
    size_mb = total_size / (1024 * 1024)
    table.add_row("Total Size", f"{size_mb:.2f} MB")
    
    console.print(table)
