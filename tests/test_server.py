"""Tests for the Manim MCP server."""

import pytest
from unittest.mock import AsyncMock, patch
from pathlib import Path

from src.server import validate_manim_code, ManimExecutionError


class TestCodeValidation:
    """Test code validation functionality."""
    
    def test_valid_code_passes(self):
        """Test that valid Manim code passes validation."""
        valid_code = """
from manim import *

class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
"""
        assert validate_manim_code(valid_code) is True
    
    def test_dangerous_patterns_rejected(self):
        """Test that dangerous code patterns are rejected."""
        dangerous_codes = [
            "import os",
            "import subprocess",
            "exec('malicious code')",
            "eval('dangerous')",
            "open('/etc/passwd')",
        ]
        
        for code in dangerous_codes:
            with pytest.raises(ValueError):
                validate_manim_code(code)
    
    def test_case_insensitive_detection(self):
        """Test that dangerous patterns are detected case-insensitively."""
        with pytest.raises(ValueError):
            validate_manim_code("IMPORT OS")


class TestManimExecution:
    """Test Manim execution functionality."""
    
    @pytest.mark.asyncio
    async def test_execution_error_handling(self):
        """Test that execution errors are properly handled."""
        # This would require mocking subprocess execution
        # Implementation depends on testing strategy
        pass


if __name__ == "__main__":
    pytest.main([__file__]) 