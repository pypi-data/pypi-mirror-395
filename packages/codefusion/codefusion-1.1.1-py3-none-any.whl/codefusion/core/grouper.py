# codefusion/core/grouper.py
from pathlib import Path
import typing as t
import fnmatch

# Default fallback if no config is provided
DEFAULT_GROUPS = {
    'other': {
        'priority': 99,
        'description': 'Other Files'
    }
}

class FileGrouper:
    def __init__(self, groups_config: t.Optional[t.Dict[str, t.Any]] = None):
        self.groups_config = groups_config or DEFAULT_GROUPS
        # Ensure 'other' group exists
        if 'other' not in self.groups_config:
            self.groups_config['other'] = {'priority': 99, 'description': 'Other Files'}

    def classify_file(self, file_path: Path, root_dir: Path) -> str:
        """Classify a file into a group based on extension, name, and path."""
        try:
            rel_path = file_path.relative_to(root_dir)
        except ValueError:
            rel_path = file_path
        
        ext = file_path.suffix.lower()
        name = file_path.name.lower()
        path_str = rel_path.as_posix().lower()
        
        # Check each group (except 'other')
        for group_name, group_config in self.groups_config.items():
            if group_name == 'other':
                continue
            
            # Check extensions
            if ext and ext in group_config.get('extensions', []):
                return group_name
            
            # Check exact names (for extensionless files)
            if name in group_config.get('names', []):
                return group_name
            
            # Check path patterns
            for pattern in group_config.get('patterns', []):
                # Convert glob pattern to path matching
                pattern_clean = pattern.strip('*/')
                if pattern_clean in path_str:
                    return group_name
        
        return 'other'

    def group_and_sort_files(self, files: t.List[Path], root_dir: Path) -> t.List[t.Tuple[str, t.List[Path]]]:
        """
        Group files logically and sort within groups.
        Returns list of tuples: (group_name, [files_in_group])
        """
        grouped: t.Dict[str, t.List[Path]] = {}
        
        for file_path in files:
            group = self.classify_file(file_path, root_dir)
            if group not in grouped:
                grouped[group] = []
            grouped[group].append(file_path)
        
        # Sort files within each group by relative path
        for group in grouped:
            grouped[group].sort(key=lambda f: f.relative_to(root_dir).as_posix())
        
        # Create ordered list of (group_name, files) tuples by priority
        result = []
        # Sort groups by priority
        sorted_groups = sorted(grouped.keys(), key=lambda x: self.groups_config.get(x, {}).get('priority', 99))
        
        for group_name in sorted_groups:
            result.append((group_name, grouped[group_name]))
        
        return result

    def get_group_description(self, group_name: str) -> str:
        """Get the description for a group."""
        return self.groups_config.get(group_name, {}).get('description', group_name.title())

