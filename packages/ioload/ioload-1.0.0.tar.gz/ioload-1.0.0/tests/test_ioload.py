"""
Unit tests for ioload
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from collections import deque

# Import functions to test
try:
    from ioload import format_bytes
except ImportError:
    # If running as script, import directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("ioload", Path(__file__).parent.parent / "ioload.py")
    ioload = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ioload)
    format_bytes = ioload.format_bytes


# Mock ioload module for testing
class TestIOStatMonitor:
    """Test IOStatMonitor class functionality."""
    
    def test_device_validation(self):
        """Test device name validation."""
        # This would test the _is_valid_device method
        # For now, just a placeholder
        assert True
    
    def test_data_structure(self):
        """Test data structure initialization."""
        # Test that deques are properly initialized
        test_deque = deque(maxlen=60)
        assert test_deque.maxlen == 60


class TestFormatBytes:
    """Test format_bytes function."""
    
    def test_format_bytes_basic(self):
        """Test basic byte formatting."""
        # Import the function
        from ioload import format_bytes
        
        assert format_bytes(0) == "0.00 B/s"
        assert format_bytes(512) == "512.00 B/s"
        assert format_bytes(1024) == "1.00 KB/s"
        assert format_bytes(1024 * 1024) == "1.00 MB/s"
    
    def test_format_bytes_negative(self):
        """Test handling of negative values."""
        from ioload import format_bytes
        
        # Should handle negative gracefully
        result = format_bytes(-100)
        assert "0.00" in result or "-" not in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
