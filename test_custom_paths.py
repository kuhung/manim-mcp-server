#!/usr/bin/env python3
"""
Test script for custom paths functionality in Manim MCP Server
"""

import asyncio
import tempfile
from pathlib import Path
import sys
import os

# Add src to path so we can import the server
sys.path.insert(0, str(Path(__file__).parent / "src"))

from server import execute_manim_safely

async def test_custom_paths():
    """Test the custom paths functionality"""
    
    # Sample Manim code
    test_code = '''
from manim import *

class TestScene(Scene):
    def construct(self):
        text = Text("Hello, Custom Paths!")
        self.play(Write(text))
        self.wait(1)
'''
    
    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Custom script directory
        script_dir = temp_path / "custom_scripts"
        script_dir.mkdir()
        
        # Custom output directory  
        output_dir = temp_path / "custom_output"
        output_dir.mkdir()
        
        # Working directory (fallback)
        work_dir = temp_path / "work"
        work_dir.mkdir()
        
        print(f"Testing with:")
        print(f"  Script dir: {script_dir}")
        print(f"  Output dir: {output_dir}")
        print(f"  Work dir: {work_dir}")
        
        try:
            # Test with custom paths
            result = await execute_manim_safely(
                code=test_code,
                work_dir=work_dir,
                script_dir=script_dir,
                output_dir=output_dir,
                script_name="test_scene"
            )
            
            print(f"\n✅ Execution result:")
            print(f"  Success: {result['success']}")
            print(f"  Script path: {result['script_path']}")
            print(f"  Output dir: {result['output_dir']}")
            print(f"  Video files: {result['video_files']}")
            
            # Check if script was created in the right place
            expected_script = script_dir / "test_scene.py"
            if expected_script.exists():
                print(f"✅ Script created at expected location: {expected_script}")
            else:
                print(f"❌ Script not found at expected location: {expected_script}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_custom_paths()) 