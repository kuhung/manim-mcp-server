# Manim MCP Server

![Manim MCP Demo](Demo-manim-mcp.gif)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
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

### 前提条件

- Python 3.8 或更高版本
- Manim Community Edition
- MCP Python SDK

### 快速安装

```bash
# 克隆仓库
git clone https://github.com/abhiemj/manim-mcp-server.git
cd manim-mcp-server

# 安装核心依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

### 开发环境安装

```bash
# 以开发模式安装
pip install -e .

# 使用 uv（推荐）
uv pip install -e .

# 设置 pre-commit 钩子（推荐）
pre-commit install
```

### 验证安装

```bash
# 检查 Manim 是否正确安装
manim --version

# 运行测试
pytest tests/

# 运行服务器测试
python src/server.py --help
```

## 🔧 使用方法

### 可用工具

服务器提供三个主要工具：

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `execute_manim` | 执行 Manim 代码并生成动画视频 | `code`: Manim Python 代码 |
| `cleanup_workspace` | 清理临时文件和目录 | `work_dir`: 工作目录路径 |
| `list_generated_videos` | 列出所有生成的视频文件 | 无参数 |

### 运行服务器

```bash
# 直接运行
python src/server.py

# 作为模块运行
python -m src

# 如果已安装，可以使用命令行工具
manim-mcp-server
```

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

将以下配置添加到你的 `claude_desktop_config.json` 文件中：

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

### macOS 配置示例

```json
{
  "mcpServers": {
    "manim-server": {
      "command": "/usr/local/bin/python3",
      "args": [
        "/Users/username/manim-mcp-server/src/server.py"
      ],
      "env": {
        "MANIM_EXECUTABLE": "/usr/local/bin/manim"
      }
    }
  }
}
```

### Windows 配置示例

```json
{
  "mcpServers": {
    "manim-server": {
      "command": "C:\\Python\\python.exe",
      "args": [
        "C:\\path\\to\\manim-mcp-server\\src\\server.py"
      ],
      "env": {
        "MANIM_EXECUTABLE": "C:\\path\\to\\manim.exe"
      }
    }
  }
}
```

### 环境变量配置

| 变量名 | 描述 | 默认值 | 示例 |
|--------|------|--------|------|
| `MANIM_EXECUTABLE` | Manim 可执行文件路径 | `manim` | `/usr/local/bin/manim` |

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

## 🛠️ 开发指南

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/abhiemj/manim-mcp-server.git
cd manim-mcp-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 安装开发依赖
pip install -r requirements-dev.txt
pip install -e .

# 设置 pre-commit
pre-commit install
```

### 代码质量工具

```bash
# 代码格式化
black src/ tests/

# 导入排序
isort src/ tests/

# 类型检查
mypy src/

# 运行测试
pytest tests/

# 运行所有检查
pre-commit run --all-files
```

### 添加新功能

1. 创建功能分支
2. 编写代码和测试
3. 运行代码质量检查
4. 提交并创建 Pull Request

## 🔍 故障排除

### 常见问题

#### 1. Manim 未找到

**错误**：`FileNotFoundError: [Errno 2] No such file or directory: 'manim'`

**解决方案**：
```bash
# 检查 Manim 安装
which manim

# 如果未安装，安装 Manim
pip install manim

# 设置环境变量
export MANIM_EXECUTABLE=/path/to/manim
```

#### 2. 权限错误

**错误**：`PermissionError: [Errno 13] Permission denied`

**解决方案**：
```bash
# 检查目录权限
ls -la src/media/

# 修复权限
chmod 755 src/media/
```

#### 3. 依赖冲突

**错误**：版本冲突或导入错误

**解决方案**：
```bash
# 创建新的虚拟环境
python -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

### 调试模式

```bash
# 启用详细日志
export PYTHONPATH=$PWD/src
python -m src --debug

# 检查服务器状态
python -c "from src.server import server; print(server.get_capabilities())"
```

### 性能优化

- 使用 SSD 存储临时文件
- 增加可用内存
- 使用多核 CPU 进行渲染

## 📚 API 参考

### 工具详细说明

#### execute_manim

执行 Manim 代码并生成动画视频。

**参数**：
- `code` (string, required): 要执行的 Manim Python 代码

**返回**：
- 成功：工作目录路径、输出信息、生成的视频文件列表
- 失败：错误信息

**示例**：
```python
{
  "code": "from manim import *\n\nclass Test(Scene):\n    def construct(self):\n        self.play(Create(Circle()))"
}
```

#### cleanup_workspace

清理指定的工作目录。

**参数**：
- `work_dir` (string, required): 要清理的工作目录路径

**返回**：
- 清理状态信息

#### list_generated_videos

列出所有生成的视频文件。

**参数**：无

**返回**：
- 视频文件列表

## 🤝 贡献指南

我们欢迎所有级别的贡献者！

### 贡献流程

1. Fork 仓库
2. 创建功能分支：
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. 提交更改：
   ```bash
   git commit -m "Add amazing feature"
   ```
4. 推送到分支：
   ```bash
   git push origin feature/amazing-feature
   ```
5. 创建 Pull Request

### 贡献类型

- 🐛 Bug 修复
- ✨ 新功能
- 📚 文档改进
- 🧪 测试增强
- 🎨 代码优化

## 📄 许可证

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
