"""
Manim MCP Server

A Model Context Protocol server that executes Manim animation code and returns
the generated video files. This server provides tools for creating mathematical
animations using the Manim library.
"""

import asyncio
import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions


# Configuration
MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")
BASE_DIR = Path(__file__).parent / "media"
BASE_DIR.mkdir(exist_ok=True)

# Global server instance
server = Server("manim-mcp-server")


class ManimExecutionError(Exception):
    """Custom exception for Manim execution errors."""
    pass


def validate_manim_code(code: str) -> bool:
    """
    Basic validation of Manim code to prevent obvious security issues.
    
    Args:
        code: The Manim code to validate
        
    Returns:
        True if code passes basic validation
        
    Raises:
        ValueError: If code contains potentially dangerous patterns
    """
    dangerous_patterns = [
        "import os",
        "import subprocess", 
        "import sys",
        "__import__",
        "exec(",
        "eval(",
        "open(",
        "file(",
        "input(",
        "raw_input(",
    ]
    
    code_lower = code.lower()
    for pattern in dangerous_patterns:
        if pattern in code_lower:
            raise ValueError(f"Potentially dangerous code pattern detected: {pattern}")
    
    return True


async def execute_manim_safely(
    code: str, 
    work_dir: Path, 
    script_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    script_name: str = "scene"
) -> Dict[str, Any]:
    """
    Execute Manim code in a controlled environment.
    
    Args:
        code: The Manim code to execute
        work_dir: Working directory for execution
        script_dir: Optional custom directory for script file
        output_dir: Optional custom directory for output videos
        script_name: Name of the script file (without extension)
        
    Returns:
        Dictionary containing execution results
        
    Raises:
        ManimExecutionError: If execution fails
    """
    # Use custom script directory or default to work_dir
    actual_script_dir = script_dir if script_dir else work_dir
    actual_script_dir.mkdir(parents=True, exist_ok=True)
    
    script_path = actual_script_dir / f"{script_name}.py"
    
    try:
        # Write the script
        script_path.write_text(code, encoding="utf-8")
        
        # Build Manim command
        manim_cmd = [MANIM_EXECUTABLE, "-p"]
        
        # Add output directory if specified
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            manim_cmd.extend(["--media_dir", str(output_dir)])
        
        manim_cmd.append(str(script_path))
        
        # Execute Manim
        process = await asyncio.create_subprocess_exec(
            *manim_cmd,
            cwd=str(work_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            # Find generated videos
            search_dir = output_dir if output_dir else (work_dir / "media")
            video_files = []
            if search_dir.exists():
                for video_file in search_dir.rglob("*.mp4"):
                    video_files.append(str(video_file))
            
            return {
                "success": True,
                "stdout": stdout.decode("utf-8"),
                "stderr": stderr.decode("utf-8"),
                "video_files": video_files,
                "work_dir": str(work_dir),
                "script_path": str(script_path),
                "output_dir": str(output_dir) if output_dir else str(work_dir / "media"),
            }
        else:
            raise ManimExecutionError(
                f"Manim execution failed with return code {process.returncode}: "
                f"{stderr.decode('utf-8')}"
            )
            
    except Exception as e:
        if isinstance(e, ManimExecutionError):
            raise
        raise ManimExecutionError(f"Execution error: {str(e)}")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools.
    
    Returns:
        List of available tools for Manim operations
    """
    return [
        types.Tool(
            name="execute_manim",
            description="Execute Manim code and generate animation videos",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Manim Python code to execute. Should contain a Scene class with animation logic.",
                    },
                    "script_dir": {
                        "type": "string",
                        "description": "Optional custom directory to save the script file. If not provided, uses default temporary directory.",
                    },
                    "output_dir": {
                        "type": "string", 
                        "description": "Optional custom directory for video output. If not provided, uses default media directory.",
                    },
                    "script_name": {
                        "type": "string",
                        "description": "Optional custom name for the script file (without extension). Defaults to 'scene'.",
                    }
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="cleanup_workspace",
            description="Clean up temporary files and directories created during Manim execution",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_dir": {
                        "type": "string",
                        "description": "The working directory path to clean up",
                    }
                },
                "required": ["work_dir"],
            },
        ),
        types.Tool(
            name="list_generated_videos",
            description="List all generated video files in the media directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_dir": {
                        "type": "string",
                        "description": "Optional directory to search for videos. If not provided, searches default media directory.",
                    }
                },
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any]
) -> Sequence[types.TextContent | types.ImageContent]:
    """
    Handle tool execution requests.
    
    Args:
        name: Name of the tool to execute
        arguments: Tool arguments
        
    Returns:
        List of content representing the tool execution result
    """
    try:
        if name == "execute_manim":
            return await _handle_execute_manim(arguments)
        elif name == "cleanup_workspace":
            return await _handle_cleanup_workspace(arguments)
        elif name == "list_generated_videos":
            return await _handle_list_videos(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error executing tool '{name}': {str(e)}"
            )
        ]


async def _handle_execute_manim(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle Manim code execution."""
    code = arguments.get("code")
    if not code:
        raise ValueError("Missing required argument: code")
    
    # Get optional custom paths
    script_dir_str = arguments.get("script_dir")
    output_dir_str = arguments.get("output_dir")
    script_name = arguments.get("script_name", "scene")
    
    # Validate the code
    validate_manim_code(code)
    
    # Create unique working directory (fallback if no custom paths provided)
    work_dir_name = f"manim_work_{uuid.uuid4().hex[:8]}"
    work_dir = BASE_DIR / work_dir_name
    work_dir.mkdir(exist_ok=True)
    
    # Convert string paths to Path objects
    script_dir = Path(script_dir_str).expanduser().resolve() if script_dir_str else None
    output_dir = Path(output_dir_str).expanduser().resolve() if output_dir_str else None
    
    try:
        result = await execute_manim_safely(code, work_dir, script_dir, output_dir, script_name)
        
        if result["success"]:
            video_info = ""
            if result["video_files"]:
                video_info = f"\n\nGenerated videos:\n" + "\n".join(
                    f"- {video}" for video in result["video_files"]
                )
            
            return [
                types.TextContent(
                    type="text",
                    text=(
                        f"✅ Manim execution successful!\n\n"
                        f"Script saved to: {result['script_path']}\n"
                        f"Output directory: {result['output_dir']}\n"
                        f"Working directory: {result['work_dir']}\n"
                        f"Output: {result['stdout'][:500]}{'...' if len(result['stdout']) > 500 else ''}"
                        f"{video_info}\n\n"
                        f"Use the cleanup_workspace tool to remove temporary files when done."
                    )
                )
            ]
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"❌ Manim execution failed:\n{result.get('stderr', 'Unknown error')}"
                )
            ]
            
    except Exception as e:
        # Cleanup on error
        if work_dir.exists():
            shutil.rmtree(work_dir, ignore_errors=True)
        raise


async def _handle_cleanup_workspace(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle workspace cleanup."""
    work_dir_path = arguments.get("work_dir")
    if not work_dir_path:
        raise ValueError("Missing required argument: work_dir")
    
    work_dir = Path(work_dir_path)
    
    # Security check: ensure the directory is within our BASE_DIR
    try:
        work_dir.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        raise ValueError("Invalid work directory: must be within the media directory")
    
    try:
        if work_dir.exists() and work_dir.is_dir():
            shutil.rmtree(work_dir)
            return [
                types.TextContent(
                    type="text",
                    text=f"✅ Successfully cleaned up workspace: {work_dir_path}"
                )
            ]
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"⚠️ Directory not found or not a directory: {work_dir_path}"
                )
            ]
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to cleanup workspace {work_dir_path}: {str(e)}"
            )
        ]


async def _handle_list_videos(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle listing generated videos."""
    try:
        search_dir_str = arguments.get("search_dir")
        video_files = []
        
        if search_dir_str:
            # Search in custom directory
            search_dir = Path(search_dir_str).expanduser().resolve()
            if search_dir.exists():
                for video_file in search_dir.rglob("*.mp4"):
                    video_files.append(str(video_file))
        else:
            # Search in default media directories
            for work_dir in BASE_DIR.iterdir():
                if work_dir.is_dir() and work_dir.name.startswith("manim_work_"):
                    media_dir = work_dir / "media"
                    if media_dir.exists():
                        for video_file in media_dir.rglob("*.mp4"):
                            video_files.append(str(video_file))
        
        if video_files:
            video_list = "\n".join(f"- {video}" for video in video_files)
            return [
                types.TextContent(
                    type="text",
                    text=f"📹 Generated videos:\n{video_list}"
                )
            ]
        else:
            return [
                types.TextContent(
                    type="text",
                    text="📹 No generated videos found."
                )
            ]
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Error listing videos: {str(e)}"
            )
        ]


async def main() -> None:
    """Main entry point for the server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="manim-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main()) 