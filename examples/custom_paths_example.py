#!/usr/bin/env python3
"""
Example demonstrating custom paths functionality in Manim MCP Server

This example shows how to:
1. Specify custom script directory
2. Specify custom output directory  
3. Use custom script names
"""

import asyncio
import json
from pathlib import Path

# Example MCP tool call with custom paths
example_tool_call = {
    "name": "execute_manim",
    "arguments": {
        "code": '''
from manim import *

class CustomPathDemo(Scene):
    def construct(self):
        # Create title
        title = Text("Custom Paths Demo", font_size=48)
        title.set_color(BLUE)
        
        # Create subtitle
        subtitle = Text("Script and output in custom locations!", font_size=24)
        subtitle.next_to(title, DOWN, buff=0.5)
        subtitle.set_color(GREEN)
        
        # Animate
        self.play(Write(title))
        self.wait(0.5)
        self.play(Write(subtitle))
        self.wait(2)
        
        # Transform to final message
        final_text = Text("Success! Check your custom directories.", font_size=32)
        final_text.set_color(YELLOW)
        
        self.play(
            Transform(title, final_text),
            FadeOut(subtitle)
        )
        self.wait(2)
''',
        "script_dir": "~/Documents/manim_scripts",
        "output_dir": "~/Documents/manim_videos", 
        "script_name": "custom_demo"
    }
}

def print_example():
    """Print the example tool call"""
    print("🎬 Manim MCP Server - Custom Paths Example")
    print("=" * 50)
    print()
    print("To use custom paths, call the execute_manim tool with these parameters:")
    print()
    print(json.dumps(example_tool_call, indent=2))
    print()
    print("📁 This will:")
    print("  • Save script to: ~/Documents/manim_scripts/custom_demo.py")
    print("  • Output videos to: ~/Documents/manim_videos/")
    print("  • Use 'custom_demo' as the script name")
    print()
    print("🔧 Available parameters:")
    print("  • code (required): The Manim Python code")
    print("  • script_dir (optional): Custom directory for script file")
    print("  • output_dir (optional): Custom directory for video output")
    print("  • script_name (optional): Custom script filename (without .py)")
    print()
    print("💡 Tips:")
    print("  • Use ~ for home directory (will be expanded)")
    print("  • Directories will be created if they don't exist")
    print("  • If not specified, uses default temporary directories")
    print("  • Use absolute or relative paths")

if __name__ == "__main__":
    print_example() 