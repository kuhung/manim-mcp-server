# 详细安装指南

本文档提供了 Manim MCP Server 的详细安装说明，包括各种操作系统和环境的配置指南。

## 📋 系统要求

### 最低要求
- **Python**: 3.10 或更高版本
- **内存**: 最少 2GB RAM（推荐 4GB+）
- **存储**: 至少 1GB 可用空间
- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### 推荐配置
- **Python**: 3.10+
- **内存**: 8GB+ RAM
- **存储**: SSD 存储器
- **CPU**: 多核处理器（用于更快的渲染）

## 🔧 分步安装指南

### 步骤 1: 安装 Python

#### Windows
```powershell
# 使用 winget 安装 Python
winget install Python.Python.3.11

# 或者从官网下载安装器
# https://www.python.org/downloads/windows/
```

#### macOS
```bash
# 使用 Homebrew
brew install python@3.11

# 或者使用 pyenv
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

#### Ubuntu/Debian
```bash
# 更新包管理器
sudo apt update

# 安装 Python
sudo apt install python3.11 python3.11-pip python3.11-venv

# 创建软链接（可选）
sudo ln -sf /usr/bin/python3.11 /usr/bin/python3
```

### 步骤 2: 验证 Python 安装

```bash
# 检查 Python 版本
python3 --version

# 检查 pip
python3 -m pip --version
```

### 步骤 3: 安装系统依赖

#### macOS
```bash
# 安装 Cairo（Manim 依赖）
brew install cairo pango ffmpeg

# 安装 LaTeX（用于数学公式）
brew install --cask mactex-no-gui
```

#### Ubuntu/Debian
```bash
# 安装系统依赖
sudo apt install \
    build-essential \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    texlive-full

# 对于最小安装，只需要：
sudo apt install \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg
```

#### Windows
```powershell
# 使用 chocolatey 安装 FFmpeg
choco install ffmpeg

# 或者手动下载 FFmpeg 并添加到 PATH
# https://ffmpeg.org/download.html
```

### 步骤 4: 克隆和设置项目

```bash
# 克隆仓库
git clone https://github.com/abhiemj/manim-mcp-server.git
cd manim-mcp-server

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 步骤 5: 安装 Python 依赖

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装核心依赖
pip install -r requirements.txt

# 开发环境额外安装
pip install -r requirements-dev.txt

# 以可编辑模式安装项目
pip install -e .
```

### 步骤 6: 验证安装

```bash
# 检查 Manim 安装
manim --version

# 检查 MCP 安装
python -c "import mcp; print('MCP installed successfully')"

# 运行简单测试
python src/server.py --help
```

## 🛠️ 高级安装选项

### 使用 Poetry（推荐）

```bash
# 安装 Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 使用 Poetry 安装依赖
poetry install

# 激活 Poetry 环境
poetry shell

# 运行服务器
poetry run python src/server.py
```

### 使用 UV（推荐 - 现代化高速工具）

UV 是一个极快的 Python 包管理器，比 pip 快 10-100 倍！更多关于 UV 的详细介绍、高级用法和配置，请参阅 [UV 使用指南](UV_GUIDE.md)。

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆项目后，一键同步所有依赖
cd manim-mcp-server
uv sync

# 激活虚拟环境
source .venv/bin/activate

# 运行服务器
uv run python src/server.py

# 安装开发依赖
uv sync --dev

# 运行开发工具
uv run pytest tests/
uv run black src/ tests/
uv run mypy src/
```

#### UV 的优势

- ⚡ **极快速度**: 比 pip 快 10-100 倍
- 🔒 **依赖锁定**: 自动生成 `uv.lock` 文件
- 🧹 **清洁环境**: 自动管理虚拟环境
- 🔄 **兼容性**: 完全兼容 pip 和 pyproject.toml
- 📦 **内置工具**: 包含 pip、pipx、poetry 等功能

### Docker 安装

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制源代码
COPY src/ ./src/
COPY examples/ ./examples/

# 创建媒体目录
RUN mkdir -p src/media

EXPOSE 8000

CMD ["python", "src/server.py"]
```

构建和运行：

```bash
# 构建镜像
docker build -t manim-mcp-server .

# 运行容器
docker run -p 8000:8000 -v $(pwd)/src/media:/app/src/media manim-mcp-server
```

## 🔧 配置

### 环境变量设置

创建 `.env` 文件：

```bash
# Manim 可执行文件路径
MANIM_EXECUTABLE=manim

# 媒体输出目录
MEDIA_DIR=./src/media

# 日志级别
LOG_LEVEL=INFO

# 最大工作目录数量
MAX_WORKSPACES=10
```

### Claude Desktop 配置

#### 查找 Python 路径

```bash
# Linux/macOS
which python3

# Windows
where python
```

#### 配置文件位置

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

#### 完整配置示例

```json
{
  "mcpServers": {
    "manim-server": {
      "command": "/usr/local/bin/python3",
      "args": [
        "/Users/username/manim-mcp-server/src/server.py"
      ],
      "env": {
        "MANIM_EXECUTABLE": "/usr/local/bin/manim",
        "PYTHONPATH": "/Users/username/manim-mcp-server"
      }
    }
  }
}
```

## 🧪 测试安装

### 基本功能测试

#### 使用 UV（推荐）

```bash
# 进入项目目录
cd manim-mcp-server

# 同步依赖并运行测试
uv sync
uv run pytest tests/ -v

# 测试代码验证
uv run python -c "
from src.server import validate_manim_code
print('Code validation:', validate_manim_code('from manim import *'))
"

# 测试 Manim 渲染
uv run manim -pql examples/basic_animation.py BasicShapes

# 运行服务器
uv run python src/server.py
```

#### 传统方式

```bash
# 激活虚拟环境
source .venv/bin/activate  # 如果使用 uv
# 或
source venv/bin/activate   # 如果使用 pip

# 运行测试
pytest tests/ -v
python -c "from src.server import validate_manim_code; print('OK')"
manim -pql examples/basic_animation.py BasicShapes
```

### 集成测试

```bash
# 启动服务器（后台运行）
python src/server.py &
SERVER_PID=$!

# 等待服务器启动
sleep 2

# 测试 MCP 连接（需要 MCP 客户端）
# 这里需要实际的 MCP 客户端来测试

# 停止服务器
kill $SERVER_PID
```

## 🔍 故障排除

### 常见问题

#### 1. FFmpeg 未找到

**错误**: `FFmpeg not found`

**解决方案**:
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# Windows
# 下载 FFmpeg 并添加到 PATH
```

#### 2. Cairo 相关错误

**错误**: `ImportError: cannot import name '_cairo'`

**解决方案**:
```bash
# macOS
brew install cairo pango

# Ubuntu
sudo apt install libcairo2-dev libpango1.0-dev

# 重新安装 pycairo
pip uninstall pycairo cairocffi
pip install pycairo cairocffi
```

#### 3. LaTeX 渲染问题

**错误**: `LaTeX Error: File not found`

**解决方案**:
```bash
# 安装完整的 LaTeX 发行版
# macOS
brew install --cask mactex

# Ubuntu
sudo apt install texlive-full

# 或者最小安装
sudo apt install texlive-latex-base texlive-latex-extra
```

#### 4. 权限错误

**错误**: `Permission denied`

**解决方案**:
```bash
# 检查并修复目录权限
chmod -R 755 src/
mkdir -p src/media
chmod 755 src/media/

# 确保虚拟环境权限正确
chmod -R 755 venv/
```

### 性能优化

#### 加速 Manim 渲染

```bash
# 设置环境变量
export MANIM_QUALITY=low    # 低质量快速预览
export MANIM_QUALITY=high   # 高质量最终渲染

# 使用 GPU 加速（如果可用）
export MANIM_OPENGL_RENDERER=True
```

#### 内存优化

```python
# 在代码中设置较低的分辨率
config.pixel_height = 480
config.pixel_width = 854
config.frame_rate = 15
```

## 📚 后续步骤

安装完成后，你可以：

1. 阅读 [README.md](README.md) 了解基本用法
2. 查看 [examples/](examples/) 目录的示例代码
3. 配置 Claude Desktop 集成
4. 开始创建你的第一个 Manim 动画！

## 💡 获取帮助

如果遇到问题：

1. 检查 [故障排除](#故障排除) 部分
2. 搜索 [GitHub Issues](https://github.com/abhiemj/manim-mcp-server/issues)
3. 创建新的 Issue 描述你的问题
4. 访问 [Manim Community](https://www.manim.community/) 获取 Manim 相关帮助 