# Manim MCP Server

![Manim MCP Demo](Demo-manim-mcp.gif)

上图演示了通过 MCP 客户端与 Manim MCP Server 交互，输入 Manim 代码并实时生成动画的过程。

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

## 📖 Overview

**Manim MCP Server** 是一个符合 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 标准的服务器，用于执行 Manim 动画代码并生成视频文件。它为通过 MCP 兼容客户端（如 Claude Desktop、Cursor 等）创建数学动画提供了安全且标准化的方式。

**🎯 一次配置，随处可用**：配置完成后，无需手动启动服务器，MCP 客户端会在需要时自动启动和管理服务器进程。

## ✨ 特性

- ✅ **安全代码执行**: 基础验证以防止危险代码模式
- 🎬 **视频生成**: 使用 Manim 创建高质量动画
- 📂 **自定义路径**: 支持自定义脚本存放位置和视频输出位置
- 🧹 **工作区管理**: 自动清理临时文件
- 📁 **文件跟踪**: 列出和管理生成的视频文件
- 🔧 **标准 MCP API**: 完全符合 Model Context Protocol 标准
- ⚡ **异步支持**: 非阻塞执行和正确的异步处理
- 🛡️ **错误处理**: 详细的错误信息和优雅降级
- 🎯 **类型安全**: 完整的类型注解和验证

## 🎯 重要提示：按需启动

**Manim MCP Server 采用按需启动模式，您无需手动启动服务器！**
*   配置到 MCP 客户端后，服务器会在需要时由客户端自动启动。
*   任务完成后，服务器会自动结束，以节省系统资源。
*   这意味着您可以专注于创作，无需担心服务器的运行状态。

## 🚀 安装

详细的安装指南，包括系统依赖和多种环境配置，请参阅 [INSTALL.md](INSTALL.md)。
对于 `uv` 包管理器的详细使用方法，请参阅 [UV 使用指南](UV_GUIDE.md)。

### 前提条件

- Python 3.10 或更高版本
- Manim Community Edition
- MCP Python SDK

### 快速安装（推荐使用 uv）

我们推荐使用 `uv` 进行安装。最简单的方式是使用一键设置脚本：

```bash
# 克隆仓库
git clone https://github.com/abhiemj/manim-mcp-server.git
cd manim-mcp-server

# 运行快速设置脚本（自动安装 UV 和依赖）
bash scripts/setup-uv.sh
```
更多 `uv` 安装选项和传统 `pip` 安装方式，请参见 [INSTALL.md](INSTALL.md)。

## 🔗 MCP 客户端集成

### Claude Desktop 配置

**一次配置，随处可用！** 将以下配置添加到你的 `claude_desktop_config.json` 文件中，之后就可以在 Claude Desktop 中直接使用 Manim 功能，无需手动启动服务器。

请确保将 `/absolute/path/to/manim-mcp-server/src/server.py` 替换为你本地的实际绝对路径。

```json
{
  "mcpServers": {
    "manim-server": {
      "command": "python",
      "args": [
        "/absolute/path/to/manim-mcp-server/src/server.py"
      ],
      "env": {
        "MANIM_EXECUTABLE": "manim"
      }
    }
  }
}
```

### Cursor 配置

在 Cursor 中，通过设置 → Extensions → MCP 或在配置文件中添加：

```json
{
  "mcp": {
    "servers": {
      "manim-server": {
        "command": "python",
        "args": ["/absolute/path/to/manim-mcp-server/src/server.py"],
        "env": {
          "MANIM_EXECUTABLE": "manim"
        }
      }
    }
  }
}
```

### 其他 MCP 客户端

对于其他支持 MCP 的客户端，配置格式类似，核心参数为：
- **command**: `python`（或你的 Python 解释器路径）
- **args**: `["/path/to/manim-mcp-server/src/server.py"]`
- **env**: `{"MANIM_EXECUTABLE": "manim"}`

### 🚀 配置完成后的使用

配置完成并重启 MCP 客户端后：

1. **自动发现**：MCP 客户端会自动发现并加载 Manim MCP 服务器
2. **按需启动**：当你请求创建动画时，服务器会自动启动
3. **透明使用**：你只需要在对话中提及创建动画，无需关心技术细节
4. **自动清理**：任务完成后，服务器进程会自动结束

**在 Claude Desktop 中的示例对话**：
```
用户：请帮我创建一个显示勾股定理的动画
Claude：我来为你创建一个勾股定理的动画...（自动调用 execute_manim 工具）
```

**在 Cursor 中的使用**：
```
用户：@manim 创建一个函数图像动画
Cursor：我将使用 Manim 为你创建函数图像动画...
```

**配置注意事项**：
- `command` 应指向你的 Python 解释器
- 如果您使用了 `scripts/setup-uv.sh` 脚本通过 `uv` 安装，该脚本会在项目根目录下创建名为 `.venv` 的虚拟环境。在这种情况下：
    - **macOS/Linux**: `command` 应指向 `/absolute/path/to/manim-mcp-server/.venv/bin/python`。
    - **Windows**: `command` 应指向 `C:\absolute\path\to\manim-mcp-server\.venv\Scripts\python.exe`。
    - 请将 `/absolute/path/to/manim-mcp-server/` 替换为您项目的实际绝对路径。
- `MANIM_EXECUTABLE` 应指向 `manim` 的可执行文件。您可以通过在终端运行 `which manim` (Linux/macOS) 或 `where manim` (Windows) 来查找其路径。
- **路径必须是绝对路径。**
- **根据操作系统调整路径格式（例如 Windows 使用反斜杠 `\` 而 macOS/Linux 使用 `/`）。**

## 🎯 完整使用流程

### 1. 配置 MCP 服务器
按照上述 [MCP 客户端集成](#-mcp-客户端集成) 部分配置你的 MCP 客户端。

### 2. 在 MCP 客户端中使用

**无需手动启动服务器！** 配置完成后，直接在你的 MCP 客户端中使用即可：

**创建动画**：
```
请创建一个显示圆形变成方形的动画
```

**使用自定义路径创建动画**：
```
请创建一个动画，并将脚本保存到 ~/Documents/manim_scripts，视频输出到 ~/Documents/manim_videos
```

**查看生成的视频**：
```
请显示所有生成的视频文件
```

**查看特定目录的视频**：
```
请显示 ~/Documents/manim_videos 目录中的所有视频文件
```

**清理工作区**：
```
请清理临时文件
```

### 3. 支持的 MCP 客户端

- ✅ **Claude Desktop** - 官方桌面应用
- ✅ **Cursor** - AI 代码编辑器  
- ✅ **其他 MCP 兼容客户端** - 任何支持 MCP 标准的应用

### ❓ 常见问题与故障排除

*   **问题：配置后，MCP 客户端提示找不到服务器或无法连接。**
    *   **解答：**
        1.  请仔细检查 `claude_desktop_config.json` (Claude Desktop) 或 Cursor 设置中 `manim-server` 的配置路径，确保 `args` 中的 `/absolute/path/to/manim-mcp-server/src/server.py` 是您本地正确的绝对路径。
        2.  确认 `MANIM_EXECUTABLE` 环境变量设置正确，并指向了 `manim` 的可执行文件。您可以通过 `which manim` (Linux/macOS) 或 `where manim` (Windows) 命令在终端中查找此路径。
        3.  检查 Python 解释器路径 (`command`) 是否正确。
        4.  尝试重启您的 MCP 客户端。

*   **问题：Manim 代码执行失败或视频未生成。**
    *   **解答：**
        1.  检查您的 Manim 代码本身是否存在语法错误或运行时错误。可以在本地环境中单独运行 Manim 代码进行测试。
        2.  确保 Manim 所需的依赖（如 LaTeX、ffmpeg）已正确安装并配置在系统路径中。详细依赖请参考 Manim 官方文档和本项目的 `INSTALL.md`。
        3.  查看 MCP 客户端或服务器日志（如果可用）以获取更详细的错误信息。

*   **问题：生成的视频在哪里？**
    *   **解答：** 视频文件默认生成在 `manim-mcp-server/src/media/` 目录下。您可以使用 `list_generated_videos` 工具列出所有已生成的视频。如果使用了自定义输出路径，视频将保存在您指定的目录中。

## 📁 项目结构

```
manim-mcp-server/
├── src/                           # 源代码
│   ├── __init__.py               # 包初始化
│   ├── __main__.py               # 主入口点
│   ├── server.py                 # MCP 服务器实现
│   └── media/                    # 生成的媒体文件
├── tests/                        # 测试文件
│   ├── __init__.py
│   └── test_server.py
├── examples/                     # 示例代码
│   └── basic_animation.py
├── pyproject.toml               # 项目配置
├── requirements.txt             # 核心依赖
├── requirements-dev.txt         # 开发依赖
├── .pre-commit-config.yaml      # 代码质量工具
└── README.md                    # 说明文档
```

## 🤝 贡献

我们欢迎各种贡献！如果你想为项目做出贡献，请查看贡献指南（如果未来添加）或直接提交 Pull Request。
对于开发环境的搭建，请参考 [INSTALL.md](INSTALL.md) 中的开发设置部分或 [UV_GUIDE.md](UV_GUIDE.md)。

## 📜 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE.txt](LICENSE.txt) 文件获取详细信息。

## 👥 作者与致谢

**原始作者**：[abhiemj](https://github.com/abhiemj)

### 致谢

- 感谢 [Manim Community](https://www.manim.community/) 提供的出色动画库
- 感谢 [Model Context Protocol](https://modelcontextprotocol.io/) 团队的标准化工作
- 灵感来源于开源 MCP 生态系统


## 🔗 相关链接

- [Manim Community](https://www.manim.community/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/desktop)

---

**如果这个项目对你有帮助，请考虑给个 ⭐️ star！**
