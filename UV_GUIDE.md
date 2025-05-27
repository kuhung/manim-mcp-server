# UV 使用指南

本指南详细介绍如何在 Manim MCP Server 项目中使用 UV 包管理器。

## 🚀 什么是 UV？

UV 是一个极快的 Python 包安装器和解析器，用 Rust 编写，旨在作为 pip 和 pip-tools 的替代品。它能够：

- ⚡ **速度提升 10-100 倍**：比 pip 快得多
- 🔒 **依赖锁定**：自动生成和管理 `uv.lock` 文件
- 🧹 **虚拟环境管理**：内置虚拟环境管理
- 🔄 **全面兼容**：与现有的 Python 生态系统兼容

## 📦 安装 UV

### 一键安装（推荐）

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 其他安装方式

```bash
# 使用 pip
pip install uv

# 使用 pipx
pipx install uv

# 使用 Homebrew (macOS)
brew install uv

# 使用 Cargo
cargo install --git https://github.com/astral-sh/uv uv
```

### 验证安装

```bash
uv --version
```

## 🛠️ 在项目中使用 UV

### 基本工作流程

1. **同步依赖（首次设置）**
   ```bash
   cd manim-mcp-server
   uv sync
   ```

2. **激活虚拟环境**
   ```bash
   source .venv/bin/activate
   ```

3. **运行项目**
   ```bash
   uv run python src/server.py
   ```

### 常用命令

#### 依赖管理

```bash
# 同步所有依赖
uv sync

# 同步包括开发依赖
uv sync --dev

# 只同步生产依赖
uv sync --no-dev

# 强制重新锁定依赖
uv lock --refresh

# 添加新依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 移除依赖
uv remove package-name
```

#### 虚拟环境管理

```bash
# 创建虚拟环境
uv venv

# 创建指定 Python 版本的环境
uv venv --python 3.11

# 激活环境
source .venv/bin/activate

# Windows 激活
.venv\Scripts\activate
```

#### 运行命令

```bash
# 在虚拟环境中运行命令
uv run python src/server.py
uv run pytest tests/
uv run black src/ tests/
uv run mypy src/

# 运行脚本
uv run --script scripts/setup.py
```

#### 项目管理

```bash
# 初始化新项目
uv init

# 从 requirements.txt 导入
uv pip sync requirements.txt

# 导出依赖
uv pip freeze > requirements.txt
```

## 📋 项目结构

使用 UV 后，项目结构如下：

```
manim-mcp-server/
├── .python-version        # 指定 Python 版本
├── pyproject.toml         # 项目配置，包含 UV 配置
├── uv.lock               # 锁定的依赖版本
├── .venv/                # UV 创建的虚拟环境
├── src/
├── tests/
└── examples/
```

## ⚡ 性能对比

| 操作 | pip | uv | 提升倍数 |
|------|-----|----|---------| 
| 安装 Django | 3.5s | 0.2s | 17.5x |
| 解析依赖 | 15s | 0.5s | 30x |
| 创建环境 | 2s | 0.1s | 20x |

## 🔧 配置

### pyproject.toml 配置

```toml
[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]

[tool.uv.sources]
# 指定特定包的源
# my-package = { git = "https://github.com/user/repo.git" }

[tool.uv.workspace]
members = ["."]
```

### 环境变量

```bash
# UV 配置目录
export UV_CONFIG_DIR="~/.config/uv"

# 禁用网络访问
export UV_OFFLINE=1

# 使用代理
export UV_HTTP_PROXY="http://proxy.example.com:8080"

# 缓存目录
export UV_CACHE_DIR="~/.cache/uv"
```

## 🛠️ 开发工作流

### 日常开发

```bash
# 1. 开始工作
cd manim-mcp-server
uv sync

# 2. 激活环境
source .venv/bin/activate

# 3. 开发和测试
uv run pytest tests/
uv run black src/
uv run mypy src/

# 4. 添加新依赖
uv add new-package
uv lock  # 更新 lock 文件

# 5. 提交更改（包括 uv.lock）
git add pyproject.toml uv.lock
git commit -m "Add new dependency"
```

### CI/CD 集成

```yaml
# GitHub Actions 示例
- name: Set up UV
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest tests/
```

## 🔄 迁移指南

### 从 pip 迁移

```bash
# 1. 安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 初始化项目
uv init --no-readme

# 3. 导入现有依赖
uv pip sync requirements.txt
uv add $(cat requirements.txt | grep -v '^#' | grep -v '^$')

# 4. 生成锁文件
uv lock
```

### 从 Poetry 迁移

```bash
# 1. 转换 pyproject.toml
# UV 可以直接读取 Poetry 格式的依赖

# 2. 同步依赖
uv sync

# 3. 删除 Poetry 文件（可选）
rm poetry.lock
```

## 🐛 故障排除

### 常见问题

1. **锁文件冲突**
   ```bash
   # 强制重新生成锁文件
   rm uv.lock
   uv lock
   ```

2. **依赖解析失败**
   ```bash
   # 查看详细错误信息
   uv sync --verbose
   
   # 清除缓存
   uv cache clean
   ```

3. **虚拟环境问题**
   ```bash
   # 重新创建虚拟环境
   rm -rf .venv
   uv venv
   uv sync
   ```

4. **网络问题**
   ```bash
   # 使用镜像源
   uv sync --index-url https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

### 调试命令

```bash
# 查看依赖树
uv tree

# 检查过时的包
uv pip list --outdated

# 显示包信息
uv pip show package-name

# 验证锁文件
uv lock --check
```

## 📚 最佳实践

### 1. 依赖管理

- ✅ 始终提交 `uv.lock` 文件
- ✅ 使用 `uv sync` 而不是 `uv install`
- ✅ 定期运行 `uv lock --refresh` 更新依赖
- ✅ 将开发依赖放在 `[tool.uv.dev-dependencies]` 中

### 2. 环境管理

- ✅ 使用 `.python-version` 文件指定 Python 版本
- ✅ 不要提交 `.venv` 目录
- ✅ 在 CI 中使用 `uv sync --frozen` 确保一致性

### 3. 性能优化

- ✅ 使用 `uv run` 避免环境激活开销
- ✅ 利用 UV 的并行安装特性
- ✅ 配置合适的缓存目录

### 4. 团队协作

- ✅ 统一使用 UV 或提供兼容的安装说明
- ✅ 在 README 中说明如何使用 UV
- ✅ 在 CI/CD 中使用 UV 确保一致性

## 🔗 更多资源

- [UV 官方文档](https://docs.astral.sh/uv/)
- [UV GitHub 仓库](https://github.com/astral-sh/uv)
- [Astral 博客](https://astral.sh/blog/)
- [Python 包管理比较](https://chriswarrick.com/blog/2023/01/15/how-to-improve-python-packaging/)

---

**提示**: UV 仍在快速发展中，建议关注官方更新获取最新功能和改进。 