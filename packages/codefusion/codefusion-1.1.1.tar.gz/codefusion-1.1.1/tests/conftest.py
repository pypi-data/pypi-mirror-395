import pytest
import os
from pathlib import Path
import shutil

@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure for testing."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create some source files
    (project_dir / "main.py").write_text("print('Hello')")
    (project_dir / "utils.py").write_text("def helper(): pass")
    (project_dir / "ignored.py").write_text("secret = 'key'")
    
    # Create a subdirectory
    sub_dir = project_dir / "subdir"
    sub_dir.mkdir()
    (sub_dir / "sub.py").write_text("class Sub: pass")
    
    # Create .gitignore
    (project_dir / ".gitignore").write_text("ignored.py\n__pycache__/")
    
    return project_dir
