import pytest
from pathlib import Path
from codefusion.core.grouper import FileGrouper

def test_grouper_default_groups(tmp_path):
    """Test default file grouping."""
    config = {
        "Python": {"extensions": [".py"]},
        "JavaScript": {"extensions": [".js"]},
        "Markdown": {"extensions": [".md"]}
    }
    grouper = FileGrouper(groups_config=config)
    assert grouper.classify_file(Path("test.py"), tmp_path) == "Python"
    assert grouper.classify_file(Path("test.js"), tmp_path) == "JavaScript"
    assert grouper.classify_file(Path("test.md"), tmp_path) == "Markdown"

def test_grouper_unknown_extension(tmp_path):
    """Test unknown extension grouping."""
    grouper = FileGrouper()
    assert grouper.classify_file(Path("test.unknown"), tmp_path) == "other"

def test_grouper_custom_config(tmp_path):
    """Test custom group configuration."""
    config = {
        "Custom": {'extensions': [".xyz", ".abc"]}
    }
    grouper = FileGrouper(groups_config=config)
    assert grouper.classify_file(Path("test.xyz"), tmp_path) == "Custom"
    # Defaults are not merged if config provided? 
    # Grouper implementation: self.groups_config = groups_config or DEFAULT_GROUPS
    # So if I provide config, defaults are gone except 'other'.
    # assert grouper.classify_file(Path("test.py"), tmp_path) == "Python" # This would fail if defaults are replaced.
    
def test_grouper_case_insensitivity(tmp_path):
    """Test case insensitivity."""
    config = {"Python": {"extensions": [".py"]}}
    grouper = FileGrouper(groups_config=config)
    assert grouper.classify_file(Path("TEST.PY"), tmp_path) == "Python"
