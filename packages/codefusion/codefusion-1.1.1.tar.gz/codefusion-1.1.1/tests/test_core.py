import pytest
from codefusion.core.app import CodeFusionApp
from codefusion.core.scanner import FileScanner
from codefusion.core.writer import CodeWriter

def test_scanner_respects_gitignore(temp_project):
    app = CodeFusionApp(directory=temp_project)
    files, _ = app.scan()
    
    file_names = [f.name for f in files]
    assert "main.py" in file_names
    assert "utils.py" in file_names
    assert "sub.py" in file_names
    assert "ignored.py" not in file_names

def test_scanner_extensions_filter(temp_project):
    app = CodeFusionApp(directory=temp_project, extensions={"py"})
    files, _ = app.scan()
    assert len(files) > 0
    assert all(f.suffix == ".py" for f in files)

def test_writer_output(temp_project, tmp_path):
    output_file = tmp_path / "output.txt"
    from codefusion.core.grouper import FileGrouper
    app = CodeFusionApp(directory=temp_project, output_file=output_file)
    # CodeFusionApp handles CodeWriter init internally, so this test should be fine unless CodeFusionApp init changed?
    # Wait, CodeFusionApp init calls CodeWriter?
    # Let's check CodeFusionApp.__init__ or compile method.
    app.compile()
    
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "main.py" in content
    assert "print('Hello')" in content
    assert "utils.py" in content
    assert "sub.py" in content
