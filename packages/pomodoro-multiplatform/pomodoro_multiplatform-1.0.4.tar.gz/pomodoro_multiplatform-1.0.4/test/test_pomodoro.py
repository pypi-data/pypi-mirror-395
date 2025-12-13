"""
Tests for pomodoro.py
"""

import subprocess
import sys
from unittest.mock import patch

try:
    import pytest
except ImportError:
    pytest = None  # type: ignore

# Import functions from pomodoro
sys.path.insert(0, ".")
from pomodoro import format_minutes, parse_args


def test_format_minutes():
    """Test time formatting function."""
    assert format_minutes(0) == "00:00"
    assert format_minutes(60) == "01:00"
    assert format_minutes(125) == "02:05"
    assert format_minutes(3599) == "59:59"
    assert format_minutes(3661) == "61:01"


def test_parse_args_defaults():
    """Test argument parsing with defaults."""
    with patch("sys.argv", ["pomodoro.py"]):
        args = parse_args()
        assert args.work == 25
        assert args.short == 5
        assert args.long == 15
        assert args.every == 2


def test_parse_args_custom():
    """Test argument parsing with custom values."""
    with patch(
        "sys.argv",
        [
            "pomodoro.py",
            "--work",
            "50",
            "--short",
            "10",
            "--long",
            "20",
            "--every",
            "4",
        ],
    ):
        args = parse_args()
        assert args.work == 50
        assert args.short == 10
        assert args.long == 20
        assert args.every == 4


def test_script_help():
    """Test that script shows help message."""
    result = subprocess.run(
        [sys.executable, "pomodoro.py", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Pomodoro" in result.stdout or "pomodoro" in result.stdout.lower()


def test_notify_without_plyer():
    """Test notification function works without plyer."""
    from pomodoro import notify

    # Should not raise any exceptions
    notify("Test Title", "Test Message")


def test_wait_for_user_confirmation():
    """Test user confirmation function."""
    from pomodoro import wait_for_user_confirmation
    import platform

    if platform.system() != "Darwin":
        # Test console input version
        with patch("builtins.input", return_value="y"):
            assert wait_for_user_confirmation("Test?") is True

        with patch("builtins.input", return_value="n"):
            assert wait_for_user_confirmation("Test?") is False


if __name__ == "__main__":
    if pytest:
        pytest.main([__file__, "-v"])
