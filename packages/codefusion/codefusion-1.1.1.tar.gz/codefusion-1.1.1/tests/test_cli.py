import pytest
from codefusion.ui.cli import main
from unittest.mock import patch
import sys

def test_cli_help(capsys):
    with patch.object(sys, 'argv', ['codefusion', '--help']):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "CodeFusion" in captured.out
        assert "usage:" in captured.out

def test_cli_version(capsys):
    with patch.object(sys, 'argv', ['codefusion', '--version']):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "CodeFusion" in captured.out
