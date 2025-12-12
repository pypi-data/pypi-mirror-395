import pytest
from pathlib import Path
from codefusion.core.scanner import FileScanner
from codefusion.ignore.manager import IgnoreManager
from codefusion.core.filter import FileFilter

@pytest.fixture
def scanner_setup(tmp_path):
    """Setup scanner with basic files."""
    (tmp_path / "file1.py").write_text("content")
    (tmp_path / "file2.txt").write_text("content")
    (tmp_path / "ignored.py").write_text("content")
    (tmp_path / ".gitignore").write_text("ignored.py")
    
    ignore_manager = IgnoreManager(root_dir=tmp_path, use_gitignore=True)
    file_filter = FileFilter(root_dir=tmp_path)
    scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter)
    return scanner, tmp_path

def test_scan_basic(scanner_setup):
    """Test basic scanning."""
    scanner, _ = scanner_setup
    files, extensions = scanner.scan()
    filenames = [f.name for f in files]
    assert "file1.py" in filenames
    assert "file2.txt" in filenames
    assert "ignored.py" not in filenames

def test_scan_extensions(scanner_setup):
    """Test scanning with extension filter."""
    scanner, tmp_path = scanner_setup
    scanner.file_filter.user_extensions = {".py"}
    files, _ = scanner.scan()
    filenames = [f.name for f in files]
    assert "file1.py" in filenames
    assert "file2.txt" not in filenames

def test_scan_nested_gitignore(tmp_path):
    """Test nested .gitignore support."""
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "nested.py").write_text("content")
    (tmp_path / "subdir" / "nested_ignored.py").write_text("content")
    (tmp_path / "subdir" / ".gitignore").write_text("nested_ignored.py")
    
    ignore_manager = IgnoreManager(root_dir=tmp_path, use_gitignore=True)
    file_filter = FileFilter(root_dir=tmp_path)
    scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter)
    
    files, _ = scanner.scan()
    filenames = [f.name for f in files]
    assert "nested.py" in filenames
    assert "nested_ignored.py" not in filenames

def test_scan_include_dirs(tmp_path):
    """Test explicit directory inclusion."""
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "src" / "main.py").write_text("content")
    (tmp_path / "tests" / "test_main.py").write_text("content")
    
    ignore_manager = IgnoreManager(root_dir=tmp_path)
    file_filter = FileFilter(root_dir=tmp_path)
    # Only include src
    scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter, include_dirs=["src"])
    
    files, _ = scanner.scan()
    filenames = [f.name for f in files]
    assert "main.py" in filenames
    assert "test_main.py" not in filenames

def test_scan_empty_directory(tmp_path):
    """Test scanning empty directory."""
    ignore_manager = IgnoreManager(root_dir=tmp_path)
    file_filter = FileFilter(root_dir=tmp_path)
    scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter)
    files, _ = scanner.scan()
    assert len(files) == 0

def test_scan_with_custom_ignore(tmp_path):
    """Test scanning with custom ignore file."""
    (tmp_path / "file.py").write_text("content")
    (tmp_path / "custom_ignored.py").write_text("content")
    (tmp_path / ".myignore").write_text("custom_ignored.py")
    
    ignore_manager = IgnoreManager(root_dir=tmp_path, ignore_file_name=".myignore")
    file_filter = FileFilter(root_dir=tmp_path)
    scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter)
    
    files, _ = scanner.scan()
    filenames = [f.name for f in files]
    assert "file.py" in filenames
    assert "custom_ignored.py" not in filenames

def test_scan_binary_files(tmp_path):
    """Test that binary files are excluded by default."""
    (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (tmp_path / "code.py").write_text("print('hello')")
    
    ignore_manager = IgnoreManager(root_dir=tmp_path)
    file_filter = FileFilter(root_dir=tmp_path)
    scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter)
    
    files, _ = scanner.scan()
    filenames = [f.name for f in files]
    assert "code.py" in filenames
    assert "image.png" not in filenames

def test_scan_large_files(tmp_path):
    """Test max size limit."""
    (tmp_path / "small.py").write_text("small")
    (tmp_path / "large.py").write_text("x" * 1024 * 1024) # 1MB
    
    ignore_manager = IgnoreManager(root_dir=tmp_path)
    file_filter = FileFilter(root_dir=tmp_path, max_size=500) # 500 bytes limit
    scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter)
    
    files, _ = scanner.scan()
    filenames = [f.name for f in files]
    assert "small.py" in filenames
    assert "large.py" not in filenames

def test_scan_hidden_files(tmp_path):
    """Test hidden file exclusion."""
    (tmp_path / ".hidden.py").write_text("content")
    (tmp_path / "visible.py").write_text("content")
    
    ignore_manager = IgnoreManager(root_dir=tmp_path)
    file_filter = FileFilter(root_dir=tmp_path)
    scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter)
    
    files, _ = scanner.scan()
    filenames = [f.name for f in files]
    assert "visible.py" in filenames
    # Hidden files are usually not excluded unless in gitignore or default excludes, 
    # but let's check default behavior. Default excludes usually include .*
    # codefusion/utils/constants.py has DEFAULT_EXCLUDE_PATTERNS which includes ".*"
    # Update: DEFAULT_EXCLUDE_PATTERNS does NOT include ".*", so hidden files ARE included.
    assert ".hidden.py" in filenames

def test_scan_symlinks(tmp_path):
    """Test symlink handling (should follow or ignore based on implementation)."""
    # Windows requires admin for symlinks, so we might skip this or use try-except
    try:
        target = tmp_path / "target.py"
        target.write_text("content")
        link = tmp_path / "link.py"
        link.symlink_to(target)
        
        ignore_manager = IgnoreManager(root_dir=tmp_path)
        file_filter = FileFilter(root_dir=tmp_path)
        scanner = FileScanner(root_dir=tmp_path, ignore_manager=ignore_manager, file_filter=file_filter)
        
        files, _ = scanner.scan()
        filenames = [f.name for f in files]
        assert "target.py" in filenames
        assert "link.py" in filenames # os.walk follows symlinks by default or we handle it
    except OSError:
        pytest.skip("Symlinks not supported on this platform/permission")
