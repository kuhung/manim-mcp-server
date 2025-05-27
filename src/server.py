"""
Manim MCP Server - Refactored with Fine-grained Tools

A Model Context Protocol server that executes Manim animation code and returns
the generated video files. This refactored version provides fine-grained tools
for better control and flexibility.
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
server = Server("manim-mcp-server-refactored")


class ManimError(Exception):
    """Base exception for Manim operations."""
    pass


class ScriptValidationError(ManimError):
    """Exception for script validation errors."""
    pass


class RenderError(ManimError):
    """Exception for rendering errors."""
    pass


def validate_manim_code(code: str) -> bool:
    """
    Validate Manim code for security issues.
    
    Args:
        code: The Manim code to validate
        
    Returns:
        True if code passes validation
        
    Raises:
        ScriptValidationError: If code contains dangerous patterns
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
            raise ScriptValidationError(f"Potentially dangerous code pattern detected: {pattern}")
    
    return True


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools."""
    return [
        # Script Management Tools
        types.Tool(
            name="create_script",
            description="Create and save a Manim script file",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Manim Python code to save",
                    },
                    "script_dir": {
                        "type": "string",
                        "description": "Directory to save the script (optional, uses temp dir if not provided)",
                    },
                    "script_name": {
                        "type": "string",
                        "description": "Name of the script file without extension (default: 'scene')",
                    },
                    "validate": {
                        "type": "boolean",
                        "description": "Whether to validate the script for security (default: true)",
                    }
                },
                "required": ["code"],
            },
        ),
        
        types.Tool(
            name="validate_script",
            description="Validate Manim script for security issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Manim code to validate",
                    }
                },
                "required": ["code"],
            },
        ),
        
        # Rendering Tools
        types.Tool(
            name="render_animation",
            description="Execute Manim rendering for a script file",
            inputSchema={
                "type": "object",
                "properties": {
                    "script_path": {
                        "type": "string",
                        "description": "Path to the Manim script file",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Directory for video output (optional)",
                    },
                    "quality": {
                        "type": "string",
                        "description": "Render quality (low, medium, high, production)",
                        "enum": ["low", "medium", "high", "production"]
                    },
                    "preview": {
                        "type": "boolean",
                        "description": "Whether to open preview after rendering (default: true)",
                    }
                },
                "required": ["script_path"],
            },
        ),
        
        # File Management Tools
        types.Tool(
            name="find_videos",
            description="Find video files in specified directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_dir": {
                        "type": "string",
                        "description": "Directory to search for videos",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "File pattern to match (default: '*.mp4')",
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to search recursively (default: true)",
                    }
                },
                "required": ["search_dir"],
            },
        ),
        
        types.Tool(
            name="get_workspace_info",
            description="Get information about a workspace directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "workspace_path": {
                        "type": "string",
                        "description": "Path to the workspace directory",
                    }
                },
                "required": ["workspace_path"],
            },
        ),
        
        types.Tool(
            name="cleanup_files",
            description="Clean up files and directories",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_path": {
                        "type": "string",
                        "description": "Path to file or directory to clean up",
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to remove directories recursively (default: false)",
                    }
                },
                "required": ["target_path"],
            },
        ),
        
        # Convenience Tool (for backward compatibility)
        types.Tool(
            name="execute_manim_complete",
            description="Complete Manim workflow: create script, render, and return results",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Manim Python code to execute",
                    },
                    "script_dir": {
                        "type": "string",
                        "description": "Custom directory for script file (optional)",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Custom directory for video output (optional)",
                    },
                    "script_name": {
                        "type": "string",
                        "description": "Custom script filename without extension (default: 'scene')",
                    },
                    "quality": {
                        "type": "string",
                        "description": "Render quality (default: 'medium')",
                        "enum": ["low", "medium", "high", "production"]
                    }
                },
                "required": ["code"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any]
) -> Sequence[types.TextContent | types.ImageContent]:
    """Handle tool execution requests."""
    try:
        if name == "create_script":
            return await _handle_create_script(arguments)
        elif name == "validate_script":
            return await _handle_validate_script(arguments)
        elif name == "render_animation":
            return await _handle_render_animation(arguments)
        elif name == "find_videos":
            return await _handle_find_videos(arguments)
        elif name == "get_workspace_info":
            return await _handle_get_workspace_info(arguments)
        elif name == "cleanup_files":
            return await _handle_cleanup_files(arguments)
        elif name == "execute_manim_complete":
            return await _handle_execute_manim_complete(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Error executing tool '{name}': {str(e)}"
            )
        ]


# Tool Implementation Functions

async def _handle_create_script(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle script creation."""
    code = arguments.get("code")
    if not code:
        raise ValueError("Missing required argument: code")
    
    script_dir_str = arguments.get("script_dir")
    script_name = arguments.get("script_name", "scene")
    validate = arguments.get("validate", True)
    
    # Validate code if requested
    if validate:
        try:
            validate_manim_code(code)
        except ScriptValidationError as e:
            return [
                types.TextContent(
                    type="text",
                    text=f"❌ Script validation failed: {str(e)}"
                )
            ]
    
    # Determine script directory
    if script_dir_str:
        script_dir = Path(script_dir_str).expanduser().resolve()
    else:
        # Create temporary directory
        work_dir_name = f"manim_work_{uuid.uuid4().hex[:8]}"
        script_dir = BASE_DIR / work_dir_name
    
    script_dir.mkdir(parents=True, exist_ok=True)
    script_path = script_dir / f"{script_name}.py"
    
    try:
        script_path.write_text(code, encoding="utf-8")
        
        return [
            types.TextContent(
                type="text",
                text=(
                    f"✅ Script created successfully!\n\n"
                    f"📄 Script path: {script_path}\n"
                    f"📁 Directory: {script_dir}\n"
                    f"🔍 Validated: {'Yes' if validate else 'No'}\n\n"
                    f"Use 'render_animation' tool to render this script."
                )
            )
        ]
        
    except Exception as e:
        raise ManimError(f"Failed to create script: {str(e)}")


async def _handle_validate_script(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle script validation."""
    code = arguments.get("code")
    if not code:
        raise ValueError("Missing required argument: code")
    
    try:
        validate_manim_code(code)
        return [
            types.TextContent(
                type="text",
                text="✅ Script validation passed! No security issues detected."
            )
        ]
    except ScriptValidationError as e:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Script validation failed: {str(e)}"
            )
        ]


async def _handle_render_animation(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle animation rendering."""
    script_path_str = arguments.get("script_path")
    if not script_path_str:
        raise ValueError("Missing required argument: script_path")
    
    script_path = Path(script_path_str).expanduser().resolve()
    if not script_path.exists():
        raise ValueError(f"Script file not found: {script_path}")
    
    output_dir_str = arguments.get("output_dir")
    quality = arguments.get("quality", "medium")
    preview = arguments.get("preview", True)
    
    # Build Manim command
    manim_cmd = [MANIM_EXECUTABLE]
    
    # Add quality flag
    quality_flags = {
        "low": ["-ql"],
        "medium": ["-qm"], 
        "high": ["-qh"],
        "production": ["-qp"]
    }
    manim_cmd.extend(quality_flags.get(quality, ["-qm"]))
    
    # Add preview flag
    if preview:
        manim_cmd.append("-p")
    
    # Add output directory if specified
    if output_dir_str:
        output_dir = Path(output_dir_str).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        manim_cmd.extend(["--media_dir", str(output_dir)])
    
    manim_cmd.append(str(script_path))
    
    try:
        # Execute Manim
        process = await asyncio.create_subprocess_exec(
            *manim_cmd,
            cwd=str(script_path.parent),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            return [
                types.TextContent(
                    type="text",
                    text=(
                        f"✅ Animation rendered successfully!\n\n"
                        f"📄 Script: {script_path}\n"
                        f"🎬 Quality: {quality}\n"
                        f"📁 Output dir: {output_dir_str or 'default'}\n\n"
                        f"📋 Output:\n{stdout.decode('utf-8')[:500]}{'...' if len(stdout.decode('utf-8')) > 500 else ''}\n\n"
                        f"Use 'find_videos' tool to locate generated videos."
                    )
                )
            ]
        else:
            raise RenderError(f"Rendering failed: {stderr.decode('utf-8')}")
            
    except Exception as e:
        if isinstance(e, RenderError):
            raise
        raise RenderError(f"Render execution error: {str(e)}")


async def _handle_find_videos(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle video file search."""
    search_dir_str = arguments.get("search_dir")
    if not search_dir_str:
        raise ValueError("Missing required argument: search_dir")
    
    search_dir = Path(search_dir_str).expanduser().resolve()
    pattern = arguments.get("pattern", "*.mp4")
    recursive = arguments.get("recursive", True)
    
    if not search_dir.exists():
        return [
            types.TextContent(
                type="text",
                text=f"⚠️ Directory not found: {search_dir}"
            )
        ]
    
    try:
        video_files = []
        if recursive:
            video_files = list(search_dir.rglob(pattern))
        else:
            video_files = list(search_dir.glob(pattern))
        
        if video_files:
            video_list = "\n".join(f"- {video}" for video in video_files)
            return [
                types.TextContent(
                    type="text",
                    text=(
                        f"📹 Found {len(video_files)} video file(s) in {search_dir}:\n\n"
                        f"{video_list}"
                    )
                )
            ]
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"📹 No video files found in {search_dir} matching pattern '{pattern}'"
                )
            ]
            
    except Exception as e:
        raise ManimError(f"Error searching for videos: {str(e)}")


async def _handle_get_workspace_info(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle workspace information retrieval."""
    workspace_path_str = arguments.get("workspace_path")
    if not workspace_path_str:
        raise ValueError("Missing required argument: workspace_path")
    
    workspace_path = Path(workspace_path_str).expanduser().resolve()
    
    if not workspace_path.exists():
        return [
            types.TextContent(
                type="text",
                text=f"⚠️ Workspace not found: {workspace_path}"
            )
        ]
    
    try:
        info_lines = [f"📁 Workspace: {workspace_path}"]
        
        if workspace_path.is_dir():
            # Count files by type
            py_files = list(workspace_path.rglob("*.py"))
            mp4_files = list(workspace_path.rglob("*.mp4"))
            
            info_lines.extend([
                f"📄 Python files: {len(py_files)}",
                f"🎬 Video files: {len(mp4_files)}",
                f"📊 Total size: {sum(f.stat().st_size for f in workspace_path.rglob('*') if f.is_file()) / 1024 / 1024:.2f} MB"
            ])
            
            if py_files:
                info_lines.append("\n📄 Python files:")
                info_lines.extend(f"  - {f.name}" for f in py_files[:5])
                if len(py_files) > 5:
                    info_lines.append(f"  ... and {len(py_files) - 5} more")
            
            if mp4_files:
                info_lines.append("\n🎬 Video files:")
                info_lines.extend(f"  - {f.name}" for f in mp4_files[:5])
                if len(mp4_files) > 5:
                    info_lines.append(f"  ... and {len(mp4_files) - 5} more")
        
        return [
            types.TextContent(
                type="text",
                text="\n".join(info_lines)
            )
        ]
        
    except Exception as e:
        raise ManimError(f"Error getting workspace info: {str(e)}")


async def _handle_cleanup_files(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle file cleanup."""
    target_path_str = arguments.get("target_path")
    if not target_path_str:
        raise ValueError("Missing required argument: target_path")
    
    target_path = Path(target_path_str).expanduser().resolve()
    recursive = arguments.get("recursive", False)
    
    if not target_path.exists():
        return [
            types.TextContent(
                type="text",
                text=f"⚠️ Target not found: {target_path}"
            )
        ]
    
    try:
        if target_path.is_file():
            target_path.unlink()
            return [
                types.TextContent(
                    type="text",
                    text=f"✅ File deleted: {target_path}"
                )
            ]
        elif target_path.is_dir():
            if recursive:
                shutil.rmtree(target_path)
                return [
                    types.TextContent(
                        type="text",
                        text=f"✅ Directory deleted recursively: {target_path}"
                    )
                ]
            else:
                try:
                    target_path.rmdir()
                    return [
                        types.TextContent(
                            type="text",
                            text=f"✅ Empty directory deleted: {target_path}"
                        )
                    ]
                except OSError:
                    return [
                        types.TextContent(
                            type="text",
                            text=f"❌ Directory not empty. Use recursive=true to force deletion: {target_path}"
                        )
                    ]
        
    except Exception as e:
        raise ManimError(f"Error during cleanup: {str(e)}")


async def _handle_execute_manim_complete(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle complete Manim workflow (convenience function)."""
    # This is a convenience function that combines multiple tools
    # It's kept for backward compatibility
    
    code = arguments.get("code")
    if not code:
        raise ValueError("Missing required argument: code")
    
    script_dir_str = arguments.get("script_dir")
    output_dir_str = arguments.get("output_dir")
    script_name = arguments.get("script_name", "scene")
    quality = arguments.get("quality", "medium")
    
    try:
        # Step 1: Create script
        create_result = await _handle_create_script({
            "code": code,
            "script_dir": script_dir_str,
            "script_name": script_name,
            "validate": True
        })
        
        # Extract script path from result (this is a bit hacky, but works for demo)
        if script_dir_str:
            script_dir = Path(script_dir_str).expanduser().resolve()
        else:
            # Find the created temp directory
            work_dirs = [d for d in BASE_DIR.iterdir() if d.is_dir() and d.name.startswith("manim_work_")]
            script_dir = max(work_dirs, key=lambda x: x.stat().st_mtime)  # Get most recent
        
        script_path = script_dir / f"{script_name}.py"
        
        # Step 2: Render animation
        render_result = await _handle_render_animation({
            "script_path": str(script_path),
            "output_dir": output_dir_str,
            "quality": quality,
            "preview": True
        })
        
        # Step 3: Find videos
        search_dir = output_dir_str if output_dir_str else str(script_dir / "media")
        video_result = await _handle_find_videos({
            "search_dir": search_dir,
            "pattern": "*.mp4",
            "recursive": True
        })
        
        # Combine results
        combined_text = (
            "🎬 Complete Manim workflow executed successfully!\n\n"
            "📝 Step 1 - Script Creation:\n" + create_result[0].text + "\n\n"
            "🎬 Step 2 - Animation Rendering:\n" + render_result[0].text + "\n\n"
            "📹 Step 3 - Video Discovery:\n" + video_result[0].text + "\n\n"
            "Use individual tools for more granular control."
        )
        
        return [
            types.TextContent(
                type="text",
                text=combined_text
            )
        ]
        
    except Exception as e:
        raise ManimError(f"Complete workflow failed: {str(e)}")


async def main() -> None:
    """Main entry point for the server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="manim-mcp-server-refactored",
                server_version="0.2.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main()) 