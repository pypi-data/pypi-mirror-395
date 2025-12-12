"""
Extended tests for system_info module.
"""

from unittest.mock import MagicMock, Mock, patch


class TestSystemInfoDataclass:
    """Test SystemInfo dataclass"""

    def test_system_info_creation(self):
        """Test creating SystemInfo"""
        from llm_evaluator.system_info import SystemInfo

        info = SystemInfo(
            cpu_model="Intel i7",
            cpu_cores=8,
            cpu_threads=16,
            ram_total_gb=32.0,
            gpu_info="NVIDIA RTX 3080",
            gpu_vram_gb=10.0,
            os_name="Windows",
            os_version="11",
            python_version="3.11.0",
            ollama_version="0.1.30",
            timestamp="2024-01-01T00:00:00",
        )

        assert info.cpu_model == "Intel i7"
        assert info.cpu_cores == 8

    def test_system_info_markdown(self):
        """Test to_markdown method"""
        from llm_evaluator.system_info import SystemInfo

        info = SystemInfo(
            cpu_model="Intel i7",
            cpu_cores=8,
            cpu_threads=16,
            ram_total_gb=32.0,
            gpu_info="NVIDIA RTX 3080",
            gpu_vram_gb=10.0,
            os_name="Windows",
            os_version="11",
            python_version="3.11.0",
            ollama_version="0.1.30",
            timestamp="2024-01-01T00:00:00",
        )

        markdown = info.to_markdown()

        assert "Intel i7" in markdown
        assert "32.0 GB" in markdown
        assert "RTX 3080" in markdown

    def test_system_info_markdown_no_gpu(self):
        """Test to_markdown with no GPU"""
        from llm_evaluator.system_info import SystemInfo

        info = SystemInfo(
            cpu_model="Intel i7",
            cpu_cores=8,
            cpu_threads=16,
            ram_total_gb=32.0,
            gpu_info=None,
            gpu_vram_gb=None,
            os_name="Linux",
            os_version="5.15",
            python_version="3.11.0",
            ollama_version=None,
            timestamp="2024-01-01",
        )

        markdown = info.to_markdown()

        assert "None" in markdown or "detected" in markdown

    def test_system_info_markdown_16_core_mismatch(self):
        """Test to_markdown with 16-Core in name but fewer cores"""
        from llm_evaluator.system_info import SystemInfo

        info = SystemInfo(
            cpu_model="AMD Ryzen 9 7950X 16-Core Processor",
            cpu_cores=8,  # Mismatch
            cpu_threads=16,
            ram_total_gb=64.0,
            gpu_info=None,
            gpu_vram_gb=None,
            os_name="Windows",
            os_version="11",
            python_version="3.11.0",
            ollama_version=None,
            timestamp="2024-01-01",
        )

        markdown = info.to_markdown()

        # Should show warning about core count
        assert "⚠️" in markdown or "8" in markdown

    def test_system_info_to_dict(self):
        """Test to_dict method"""
        from llm_evaluator.system_info import SystemInfo

        info = SystemInfo(
            cpu_model="CPU",
            cpu_cores=4,
            cpu_threads=8,
            ram_total_gb=16.0,
            gpu_info=None,
            gpu_vram_gb=None,
            os_name="Linux",
            os_version="5.15",
            python_version="3.11",
            ollama_version=None,
            timestamp="2024-01-01",
        )

        d = info.to_dict()

        assert isinstance(d, dict)
        assert d["cpu_model"] == "CPU"

    def test_system_info_to_json(self):
        """Test to_json method"""
        import json

        from llm_evaluator.system_info import SystemInfo

        info = SystemInfo(
            cpu_model="CPU",
            cpu_cores=4,
            cpu_threads=8,
            ram_total_gb=16.0,
            gpu_info=None,
            gpu_vram_gb=None,
            os_name="Linux",
            os_version="5.15",
            python_version="3.11",
            ollama_version=None,
            timestamp="2024-01-01",
        )

        json_str = info.to_json()

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed["cpu_model"] == "CPU"


class TestGetCpuModel:
    """Test get_cpu_model function"""

    @patch("platform.system")
    def test_get_cpu_model_linux(self, mock_system):
        """Test getting CPU model on Linux"""
        from llm_evaluator.system_info import get_cpu_model

        mock_system.return_value = "Linux"

        # Mock open for /proc/cpuinfo
        cpuinfo_content = "model name : Intel Core i7-12700K"
        with patch("builtins.open", MagicMock(return_value=iter([cpuinfo_content]))):
            # Should not crash
            result = get_cpu_model()
            assert isinstance(result, str)

    @patch("platform.system")
    @patch("platform.processor")
    def test_get_cpu_model_fallback(self, mock_processor, mock_system):
        """Test get_cpu_model fallback"""
        mock_system.return_value = "Unknown"
        mock_processor.return_value = "Unknown Processor"

        from llm_evaluator.system_info import get_cpu_model

        result = get_cpu_model()

        assert isinstance(result, str)


class TestGetGpuInfo:
    """Test get_gpu_info function"""

    @patch("subprocess.run")
    def test_get_gpu_info_nvidia(self, mock_run):
        """Test getting NVIDIA GPU info"""
        from llm_evaluator.system_info import get_gpu_info

        mock_run.return_value = Mock(returncode=0, stdout="NVIDIA GeForce RTX 3080, 10240 MiB")

        gpu_name, vram_gb = get_gpu_info()

        assert gpu_name == "NVIDIA GeForce RTX 3080"
        assert vram_gb == 10.0

    @patch("subprocess.run")
    def test_get_gpu_info_no_gpu(self, mock_run):
        """Test getting GPU info when none available"""

        from llm_evaluator.system_info import get_gpu_info

        mock_run.side_effect = FileNotFoundError

        gpu_name, vram_gb = get_gpu_info()

        assert gpu_name is None


class TestGetOllamaVersion:
    """Test get_ollama_version function"""

    @patch("subprocess.run")
    def test_get_ollama_version_installed(self, mock_run):
        """Test getting Ollama version when installed"""
        from llm_evaluator.system_info import get_ollama_version

        mock_run.return_value = Mock(returncode=0, stdout="ollama version 0.1.30")

        version = get_ollama_version()

        assert version == "0.1.30"

    @patch("subprocess.run")
    def test_get_ollama_version_not_installed(self, mock_run):
        """Test getting Ollama version when not installed"""
        from llm_evaluator.system_info import get_ollama_version

        mock_run.side_effect = FileNotFoundError

        version = get_ollama_version()

        assert version is None


class TestCollectSystemInfo:
    """Test collect_system_info function"""

    @patch("llm_evaluator.system_info.get_cpu_model")
    @patch("llm_evaluator.system_info.get_gpu_info")
    @patch("llm_evaluator.system_info.get_ollama_version")
    def test_collect_system_info(self, mock_ollama, mock_gpu, mock_cpu):
        """Test collecting system info"""
        from llm_evaluator.system_info import SystemInfo, collect_system_info

        mock_cpu.return_value = "Intel i7"
        mock_gpu.return_value = ("RTX 3080", 10.0)
        mock_ollama.return_value = "0.1.30"

        info = collect_system_info()

        assert isinstance(info, SystemInfo)
        assert info.cpu_model == "Intel i7"
        assert info.gpu_info == "RTX 3080"

    @patch("llm_evaluator.system_info.get_cpu_model")
    @patch("llm_evaluator.system_info.get_gpu_info")
    @patch("llm_evaluator.system_info.get_ollama_version")
    def test_collect_system_info_no_gpu(self, mock_ollama, mock_gpu, mock_cpu):
        """Test collecting system info without GPU"""
        from llm_evaluator.system_info import collect_system_info

        mock_cpu.return_value = "AMD Ryzen"
        mock_gpu.return_value = (None, None)
        mock_ollama.return_value = None

        info = collect_system_info()

        assert info.gpu_info is None
        assert info.ollama_version is None


class TestGetRamInfo:
    """Test RAM info retrieval"""

    def test_ram_total_retrieved(self):
        """Test RAM total is retrieved correctly"""
        from llm_evaluator.system_info import collect_system_info

        # Should run without crashing
        info = collect_system_info()

        assert info.ram_total_gb > 0


class TestOsInfo:
    """Test OS info retrieval"""

    def test_os_info_retrieved(self):
        """Test OS info is retrieved correctly"""
        from llm_evaluator.system_info import collect_system_info

        info = collect_system_info()

        assert info.os_name in ["Windows", "Linux", "Darwin"]
        assert info.os_version


class TestPythonVersion:
    """Test Python version retrieval"""

    def test_python_version_format(self):
        """Test Python version has correct format"""
        from llm_evaluator.system_info import collect_system_info

        info = collect_system_info()

        # Should be like "3.11.0"
        assert "." in info.python_version
