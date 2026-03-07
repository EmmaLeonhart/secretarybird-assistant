"""Tests for the OpenClaw bridge module."""
import os
import sys
import pytest

from backend.openclaw.bridge import OpenClawBridge, WSLManager


class TestWSLManager:
    """Test WSL management utilities."""

    def test_init(self):
        """Test WSLManager initialization."""
        manager = WSLManager()
        assert manager is not None

    def test_windows_to_wsl_path(self):
        """Test converting Windows paths to WSL paths."""
        manager = WSLManager()
        wsl_path = manager.windows_to_wsl_path(r"C:\Users\test\file.txt")
        assert wsl_path == "/mnt/c/Users/test/file.txt"

    def test_windows_to_wsl_path_drive_letter(self):
        """Test drive letter conversion."""
        manager = WSLManager()
        wsl_path = manager.windows_to_wsl_path(r"D:\Data\report.xlsx")
        assert wsl_path == "/mnt/d/Data/report.xlsx"

    def test_wsl_to_windows_path(self):
        """Test converting WSL paths to Windows paths."""
        manager = WSLManager()
        win_path = manager.wsl_to_windows_path("/mnt/c/Users/test/file.txt")
        assert win_path == r"C:\Users\test\file.txt"

    def test_wsl_to_windows_path_non_mnt(self):
        """Test that non-/mnt paths are returned as-is."""
        manager = WSLManager()
        path = "/home/user/file.txt"
        result = manager.wsl_to_windows_path(path)
        assert result == path

    def test_path_roundtrip(self):
        """Test that path conversion roundtrips correctly."""
        manager = WSLManager()
        original = r"C:\Users\test\Documents\file.xlsx"
        wsl = manager.windows_to_wsl_path(original)
        back = manager.wsl_to_windows_path(wsl)
        assert back == original


class TestOpenClawBridge:
    """Test OpenClaw bridge functionality."""

    def test_init(self):
        """Test bridge initialization."""
        bridge = OpenClawBridge()
        assert bridge is not None
        assert bridge.process is None

    def test_is_not_running_initially(self):
        """Test that bridge reports not running initially."""
        bridge = OpenClawBridge()
        assert bridge.is_running() is False

    def test_session_id_generation(self):
        """Test that session IDs are unique."""
        bridge = OpenClawBridge()
        id1 = bridge._generate_session_id()
        id2 = bridge._generate_session_id()
        assert id1 != id2

    def test_build_command(self):
        """Test building the OpenClaw command."""
        bridge = OpenClawBridge()
        cmd = bridge._build_command("Hello, help me organize files")
        assert isinstance(cmd, list)
        assert len(cmd) > 0
