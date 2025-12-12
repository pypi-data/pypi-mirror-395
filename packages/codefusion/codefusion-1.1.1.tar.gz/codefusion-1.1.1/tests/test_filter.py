import pytest
from pathlib import Path
from codefusion.core.filter import FileFilter

def test_filter_extensions(tmp_path):
    """Test extension filtering."""
    f = FileFilter(root_dir=tmp_path, user_extensions={".py"})
    assert f.should_include_file(Path("test.py")) is False # should_include checks size/empty, not extension directly in this method?
    # Wait, filter_by_extensions does the extension check. should_include_file checks size/empty.
    # Let's test filter_by_extensions
    files = [Path("test.py"), Path("test.txt")]
    # Mock stat for should_include_file
    (tmp_path / "test.py").write_text("content")
    (tmp_path / "test.txt").write_text("content")
    
    filtered = f.filter_by_extensions([tmp_path / "test.py", tmp_path / "test.txt"], {".py"})
    assert len(filtered) == 1
    assert filtered[0].name == "test.py"

def test_filter_empty_files(tmp_path):
    """Test empty file filtering."""
    f = FileFilter(root_dir=tmp_path, include_empty=False)
    empty = tmp_path / "empty.py"
    empty.touch()
    assert f.should_include_file(empty) is False
    
    f_include = FileFilter(root_dir=tmp_path, include_empty=True)
    assert f_include.should_include_file(empty) is True

def test_filter_min_size(tmp_path):
    """Test minimum size filtering."""
    f = FileFilter(root_dir=tmp_path, min_size=10)
    small = tmp_path / "small.py"
    small.write_text("12345") # 5 bytes
    assert f.should_include_file(small) is False
    
    large = tmp_path / "large.py"
    large.write_text("12345678901") # 11 bytes
    assert f.should_include_file(large) is True

def test_filter_max_size(tmp_path):
    """Test maximum size filtering."""
    f = FileFilter(root_dir=tmp_path, max_size=10)
    small = tmp_path / "small.py"
    small.write_text("12345") # 5 bytes
    assert f.should_include_file(small) is True
    
    large = tmp_path / "large.py"
    large.write_text("12345678901") # 11 bytes
    assert f.should_include_file(large) is False

def test_expand_extensions(tmp_path):
    """Test extension expansion."""
    f = FileFilter(root_dir=tmp_path)
    expanded = f.expand_extensions({".js", ".yml"})
    assert ".js" in expanded
    assert ".jsx" in expanded
    assert ".mjs" in expanded
    assert ".yml" in expanded
    assert ".yaml" in expanded
