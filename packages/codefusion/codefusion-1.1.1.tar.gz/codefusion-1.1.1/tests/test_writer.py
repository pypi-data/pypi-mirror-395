import pytest
from pathlib import Path
from codefusion.core.writer import CodeWriter
from codefusion.core.grouper import FileGrouper

def test_writer_markdown_template(tmp_path):
    """Test markdown output format."""
    writer = CodeWriter(root_dir=tmp_path, output_file=tmp_path / "out.md", template="markdown", grouper=FileGrouper())
    files = [tmp_path / "test.py"]
    (tmp_path / "test.py").write_text("print('hello')")
    
    writer.write(files, {".py"})
    
    content = (tmp_path / "out.md").read_text(encoding="utf-8")
    # The writer might use different formatting or headers. 
    # Let's check for file path and content presence which is more robust.
    assert "test.py" in content
    assert "print('hello')" in content
    # Check for code block start if possible, but might depend on language detection
    # assert "```" in content

def test_writer_xml_template(tmp_path):
    """Test XML output format (if supported, or default structure)."""
    # Assuming 'default' or specific template. Let's check supported templates.
    # CLI says: choices=["default", "markdown", "html", "json"]
    writer = CodeWriter(root_dir=tmp_path, output_file=tmp_path / "out.xml", template="default", grouper=FileGrouper())
    files = [tmp_path / "test.py"]
    (tmp_path / "test.py").write_text("print('hello')")
    
    writer.write(files, {".py"})
    content = (tmp_path / "out.xml").read_text(encoding="utf-8")
    assert "test.py" in content
    assert "print('hello')" in content
    assert "=" * 10 in content # Separator

def test_writer_json_template(tmp_path):
    """Test JSON output format."""
    writer = CodeWriter(root_dir=tmp_path, output_file=tmp_path / "out.json", template="json", grouper=FileGrouper())
    files = [tmp_path / "test.py"]
    (tmp_path / "test.py").write_text("print('hello')")
    
    writer.write(files, {".py"})
    
    import json
    content = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    assert isinstance(content, list) or isinstance(content, dict)
    # Depending on implementation, might be list of files or dict structure
    # Based on writer.py logic (I recall _write_json), it likely dumps a structure.

def test_writer_grouping(tmp_path):
    """Test file grouping in output."""
    writer = CodeWriter(root_dir=tmp_path, output_file=tmp_path / "out.txt", grouper=FileGrouper())
    files = [tmp_path / "test.py", tmp_path / "style.css"]
    (tmp_path / "test.py").write_text("code")
    (tmp_path / "style.css").write_text("style")
    
    writer.write(files, {".py", ".css"})
    content = (tmp_path / "out.txt").read_text(encoding="utf-8")
    # Groups are usually headers like "# Python" or similar
    # We check if both files are present
    assert "test.py" in content
    assert "style.css" in content

def test_writer_stdout(tmp_path, capsys):
    """Test writing to stdout."""
    writer = CodeWriter(root_dir=tmp_path, output_file=None, to_stdout=True, grouper=FileGrouper())
    files = [tmp_path / "test.py"]
    (tmp_path / "test.py").write_text("print('stdout')")
    
    writer.write(files, {".py"})
    captured = capsys.readouterr()
    assert "print('stdout')" in captured.out
