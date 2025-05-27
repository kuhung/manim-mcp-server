# Manim MCP Server

![Manim MCP Demo](Demo-manim-mcp.gif)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

## 📖 Overview

**Manim MCP Server** 是一个符合 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 标准的服务器，用于执行 Manim 动画代码并生成视频文件。它为通过 MCP 兼容客户端（如 Claude Desktop）创建数学动画提供了安全且标准化的方式。

## ✨ 特性

- ✅ **安全代码执行**: 基础验证以防止危险代码模式
- 🎬 **视频生成**: 使用 Manim 创建高质量动画
- 🧹 **工作区管理**: 自动清理临时文件
- 📁 **文件跟踪**: 列出和管理生成的视频文件
- 🔧 **标准 MCP API**: 完全符合 Model Context Protocol 标准
- ⚡ **异步支持**: 非阻塞执行和正确的异步处理
- 🛡️ **错误处理**: 详细的错误信息和优雅降级
- 🎯 **类型安全**: 完整的类型注解和验证

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

## 🔧 使用方法

### 可用工具

服务器提供三个主要工具：

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `execute_manim` | 执行 Manim 代码并生成动画视频 | `code`: Manim Python 代码 |
| `cleanup_workspace` | 清理临时文件和目录 | `work_dir`: 工作目录路径 |
| `list_generated_videos` | 列出所有生成的视频文件 | 无参数 |

### 运行服务器

推荐使用 `uv` 运行服务器：
```bash
# 使用 uv（推荐）
uv run python src/server.py
```
或者，激活虚拟环境后：
```bash
source .venv/bin/activate # Linux/macOS 或 uv 创建的环境
# .venv\Scripts\activate # Windows
python src/server.py
```
更多运行选项请参见 [INSTALL.md](INSTALL.md)。

### 基本使用示例

#### 1. 创建简单动画

```python
from manim import *

class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello, Manim!", font_size=72)
        self.play(Write(text))
        self.play(text.animate.scale(1.5).set_color(BLUE))
        self.wait(1)
```

#### 2. 数学公式动画

```python
from manim import *

class MathFormula(Scene):
    def construct(self):
        # 创建数学公式
        formula = MathTex(r"E = mc^2")
        
        # 动画效果
        self.play(Write(formula))
        self.play(formula.animate.scale(2).set_color(YELLOW))
        self.wait(1)
        
        # 变换公式
        new_formula = MathTex(r"F = ma").move_to(formula.get_center())
        self.play(Transform(formula, new_formula))
        self.wait(1)
```

#### 3. 几何图形动画

```python
from manim import *

class GeometryAnimation(Scene):
    def construct(self):
        # 创建图形
        circle = Circle(radius=1, color=BLUE)
        square = Square(side_length=2, color=RED).next_to(circle, RIGHT, buff=1)
        triangle = Triangle(color=GREEN).next_to(square, RIGHT, buff=1)
        
        # 动画序列
        self.play(Create(circle))
        self.play(Create(square))
        self.play(Create(triangle))
        
        # 同时变换
        self.play(
            circle.animate.shift(UP * 2),
            square.animate.rotate(PI/4),
            triangle.animate.scale(1.5)
        )
        self.wait(1)
```

## 🔗 Claude Desktop 集成

### 配置文件设置

将以下配置添加到你的 `claude_desktop_config.json` 文件中。请确保将 `/absolute/path/to/manim-mcp-server/src/server.py` 替换为你本地的实际绝对路径。

```json
{
  "mcpServers": {
    "manim-server": {
      "command": "python", // 或你系统中 python3 的可执行文件路径
      "args": [
        "/absolute/path/to/manim-mcp-server/src/server.py"
      ],
      "env": {
        "MANIM_EXECUTABLE": "manim" // 或你系统中 manim 的可执行文件路径
      }
    }
  }
}
```
**注意**: 
- `command` 应指向你的 Python 解释器。
- `MANIM_EXECUTABLE` 应指向 `manim` 的可执行文件。
根据你的操作系统 (macOS, Windows, Linux) 和 Python/Manim 安装位置，这些路径可能需要调整。详细的特定平台配置示例请参考 [INSTALL.md](INSTALL.md) 中的相关部分或项目文档。

## 🎯 完整使用流程

### 1. 启动服务器
```bash
python src/server.py
```

### 2. 在 Claude 中使用工具

**创建动画**：
```
请使用 execute_manim 工具创建一个显示圆形变成方形的动画。
```

**查看生成的视频**：
```
请使用 list_generated_videos 工具显示所有生成的视频文件。
```

**清理工作区**：
```
请使用 cleanup_workspace 工具清理临时文件。
```

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

**主要作者**：[abhiemj](https://github.com/abhiemj)

### 致谢

- 感谢 [Manim Community](https://www.manim.community/) 提供的出色动画库
- 感谢 [Model Context Protocol](https://modelcontextprotocol.io/) 团队的标准化工作
- 灵感来源于开源 MCP 生态系统

### 特色推荐

本仓库被收录在 [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) 的 **Animation & Video** 分类中！

## 📞 联系方式

- GitHub: [@abhiemj](https://github.com/abhiemj)
- Instagram: [@aiburner_official](https://www.instagram.com/aiburner_official)

## 🔗 相关链接

- [Manim Community](https://www.manim.community/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/desktop)

---

**如果这个项目对你有帮助，请考虑给个 ⭐️ star！**
