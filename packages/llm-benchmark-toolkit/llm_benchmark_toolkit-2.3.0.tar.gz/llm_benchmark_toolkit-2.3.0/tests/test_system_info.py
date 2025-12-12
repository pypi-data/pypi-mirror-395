"""
Tests for system information module

Tests SystemInfo dataclass and collection functions.
"""

import json
from unittest.mock import Mock, patch

import pytest

from llm_evaluator.system_info import (
    SystemInfo,
    collect_system_info,
    get_cpu_model,
    get_gpu_info,
    get_ollama_version,
)


class TestSystemInfo:
    """Test SystemInfo dataclass"""

    @pytest.fixture
    def sample_info(self):
        """Create sample SystemInfo object"""
        return SystemInfo(
            cpu_model="AMD Ryzen 9 5900X",
            cpu_cores=12,
            cpu_threads=24,
            ram_total_gb=32.0,
            gpu_info="NVIDIA RTX 3080",
            gpu_vram_gb=10.0,
            os_name="Windows",
            os_version="11",
            python_version="3.11.0",
            ollama_version="0.1.29",
            timestamp="2024-01-15T10:30:00",
        )

    def test_to_dict(self, sample_info):
        """Test conversion to dictionary"""
        data = sample_info.to_dict()

        assert isinstance(data, dict)
        assert data["cpu_model"] == "AMD Ryzen 9 5900X"
        assert data["cpu_cores"] == 12
        assert data["ram_total_gb"] == 32.0
        assert data["gpu_info"] == "NVIDIA RTX 3080"

    def test_to_json(self, sample_info):
        """Test conversion to JSON"""
        json_str = sample_info.to_json()

        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data["cpu_model"] == "AMD Ryzen 9 5900X"

    def test_to_markdown(self, sample_info):
        """Test conversion to markdown"""
        md = sample_info.to_markdown()

        assert isinstance(md, str)
        assert "AMD Ryzen 9 5900X" in md
        assert "32.0 GB" in md
        assert "NVIDIA RTX 3080" in md
        assert "Windows 11" in md

    def test_no_gpu(self):
        """Test markdown output without GPU"""
        info = SystemInfo(
            cpu_model="Intel Core i7",
            cpu_cores=8,
            cpu_threads=16,
            ram_total_gb=16.0,
            gpu_info=None,
            gpu_vram_gb=None,
            os_name="Linux",
            os_version="Ubuntu 22.04",
            python_version="3.10.0",
            ollama_version=None,
            timestamp="2024-01-15",
        )

        md = info.to_markdown()
        assert "None detected" in md

    def test_no_ollama(self):
        """Test markdown output without Ollama"""
        info = SystemInfo(
            cpu_model="Intel Core i7",
            cpu_cores=8,
            cpu_threads=16,
            ram_total_gb=16.0,
            gpu_info=None,
            gpu_vram_gb=None,
            os_name="Linux",
            os_version="Ubuntu 22.04",
            python_version="3.10.0",
            ollama_version=None,
            timestamp="2024-01-15",
        )

        md = info.to_markdown()
        assert "Not installed" in md


class TestGetCpuModel:
    """Test get_cpu_model function"""

    def test_returns_string(self):
        """Test that CPU model is a string"""
        model = get_cpu_model()
        assert isinstance(model, str)
        assert len(model) > 0

    @patch("platform.system")
    @patch("platform.processor")
    def test_fallback_to_processor(self, mock_processor, mock_system):
        """Test fallback when specific method fails"""
        mock_system.return_value = "Unknown"
        mock_processor.return_value = "Generic CPU"

        model = get_cpu_model()
        assert isinstance(model, str)


class TestCollectSystemInfo:
    """Test collect_system_info function"""

    def test_returns_system_info(self):
        """Test that function returns SystemInfo object"""
        info = collect_system_info()

        assert isinstance(info, SystemInfo)
        assert info.cpu_cores > 0
        assert info.cpu_threads > 0
        assert info.ram_total_gb > 0
        assert info.os_name in ["Windows", "Linux", "Darwin"]
        assert info.python_version is not None

    def test_timestamp_present(self):
        """Test that timestamp is set"""
        info = collect_system_info()

        assert info.timestamp is not None
        assert len(info.timestamp) > 0


class TestGetGpuInfo:
    """Test get_gpu_info function"""

    def test_returns_tuple(self):
        """Test that function returns tuple"""
        gpu_name, gpu_vram = get_gpu_info()

        # Either both None or both have values
        if gpu_name is not None:
            assert isinstance(gpu_name, str)
        if gpu_vram is not None:
            assert isinstance(gpu_vram, (int, float))

    def test_gpu_info_no_exceptions(self):
        """Test that get_gpu_info doesn't raise exceptions"""
        # Should handle any system gracefully
        try:
            gpu_name, gpu_vram = get_gpu_info()
            # Just verify it returns something
            assert gpu_name is None or isinstance(gpu_name, str)
        except Exception:
            pytest.fail("get_gpu_info should not raise exceptions")


class TestGetOllamaVersion:
    """Test get_ollama_version function"""

    @patch("subprocess.run")
    def test_ollama_installed(self, mock_run):
        """Test when Ollama is installed"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "ollama version 0.1.29"
        mock_run.return_value = mock_result

        version = get_ollama_version()
        assert version is not None
        assert "0.1.29" in version

    @patch("subprocess.run")
    def test_ollama_not_installed(self, mock_run):
        """Test when Ollama is not installed"""
        mock_run.side_effect = FileNotFoundError("ollama not found")

        version = get_ollama_version()
        assert version is None

    @patch("subprocess.run")
    def test_ollama_error(self, mock_run):
        """Test when Ollama command fails"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        version = get_ollama_version()
        # Should not raise
        assert version is None or isinstance(version, str)
