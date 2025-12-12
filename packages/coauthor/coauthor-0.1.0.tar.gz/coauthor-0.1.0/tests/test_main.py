import sys
import os
import tempfile
from unittest.mock import patch
import pytest
from coauthor.main import main
from coauthor import __version__


def test_main(monkeypatch):
    test_args = ["main"]
    with patch.object(sys, "argv", test_args):
        main()
    assert True


def test_version(monkeypatch, capsys):
    test_args = ["main", "--version"]
    with pytest.raises(SystemExit) as exc_info:
        with patch.object(sys, "argv", test_args):
            main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert captured.out.startswith(f"coauthor {__version__}")


def test_main_with_config_path_that_does_not_exist(monkeypatch):
    test_args = ["main", "--config_path", "test_config.yaml", "--profile", "test_profile"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(FileNotFoundError):
            main()


def test_main_with_config_path(monkeypatch):
    file_path_expected = os.path.join(os.getcwd(), ".coauthor.yml")
    test_args = ["main", "--config_path", file_path_expected]
    with patch.object(sys, "argv", test_args):
        monkeypatch.setattr("builtins.print", lambda x: x)
        main()


def test_main_with_no_arguments(monkeypatch):
    test_args = ["main"]
    with patch.object(sys, "argv", test_args):
        monkeypatch.setattr("builtins.print", lambda x: x)
        main()


def test_main_log_file(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        test_args = ["main", "--log_file", f"{os.getcwd()}/debug.log"]
        with patch.object(sys, "argv", test_args):
            main()


# def test_script_execution():
#     script_path = os.path.join(os.getcwd(), "src", "coauthor", "main.py")
#     python_interpreter = os.path.expanduser("~/.virtualenv/c2d_ai/bin/python")
#     src_dir = os.path.join(os.getcwd(), "src")
#     env = os.environ.copy()
#     env["PYTHONPATH"] = src_dir
#     result = subprocess.run([python_interpreter, script_path], capture_output=True, text=True, env=env)
#     assert result.returncode == 0
