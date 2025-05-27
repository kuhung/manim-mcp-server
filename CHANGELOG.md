# 更新日志

本文档记录了 Manim MCP Server 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.1] - 2024-01-XX

### ✨ 新增功能

#### UV 包管理器集成
- **现代化工具**: 集成 UV 作为推荐的包管理器
- **性能提升**: 比 pip 快 10-100 倍的依赖安装速度
- **依赖锁定**: 自动生成 `uv.lock` 文件确保环境一致性
- **简化工作流**: 一键同步所有依赖 (`uv sync`)

#### 文档更新
- **UV 使用指南**: 新增详细的 UV 使用指南 ([UV_GUIDE.md](UV_GUIDE.md))
- **安装说明**: 更新 README 和 INSTALL 文档以推荐 UV
- **最佳实践**: 提供 UV 的最佳实践和故障排除指南

### 🔧 技术变更

#### Python 版本要求
- **最低版本更新**: 从 Python 3.8+ 更新到 Python 3.10+（符合 MCP 要求）
- **版本文件**: 添加 `.python-version` 文件指定推荐版本

#### 项目配置
- **pyproject.toml**: 添加 UV 配置段落
- **依赖管理**: 新增开发依赖到 `[tool.uv.dev-dependencies]`
- **工作区配置**: 配置 UV 工作区支持

### 🛠️ 改进

#### 开发体验
- **命令简化**: 使用 `uv run` 简化命令执行
- **环境管理**: 自动虚拟环境创建和管理
- **缓存优化**: 利用 UV 的智能缓存机制

#### 文档改进
- **多种安装方式**: 提供 UV 和传统 pip 两种安装选项
- **性能对比**: 展示 UV 相比传统工具的性能优势
- **详细示例**: 提供完整的工作流程示例

## [0.1.0] - 2024-01-XX

### 🔄 重大重构

#### 重构为标准 MCP 架构
- **迁移到标准 MCP API**: 从 `FastMCP` 迁移到官方 `mcp.server` API
- **异步支持**: 完全重写为异步架构，提供更好的性能
- **标准化工具**: 实现标准的 `@server.list_tools()` 和 `@server.call_tool()` 装饰器

#### 项目结构重组
- **标准包结构**: 重新组织为标准 Python 包结构
- **配置标准化**: 添加 `pyproject.toml` 配置文件
- **依赖管理**: 分离核心依赖和开发依赖
- **测试框架**: 添加完整的测试结构

### ✨ 新增功能

#### 新增工具
- **`execute_manim`**: 执行 Manim 代码并生成动画视频
- **`cleanup_workspace`**: 清理临时文件和目录
- **`list_generated_videos`**: 列出所有生成的视频文件

#### 安全增强
- **代码验证**: 添加基础的代码验证以防止危险操作
- **路径安全**: 实现安全的文件路径检查
- **工作区隔离**: 每个执行任务使用独立的工作目录

#### 开发工具
- **代码质量**: 集成 Black、isort、MyPy
- **Pre-commit 钩子**: 自动代码质量检查
- **类型注解**: 完整的类型安全支持

### 🛠️ 改进

#### 错误处理
- **自定义异常**: 添加 `ManimExecutionError` 异常类
- **详细错误信息**: 提供更有用的错误消息
- **优雅降级**: 更好的错误恢复机制

#### 性能优化
- **异步执行**: 非阻塞的 Manim 代码执行
- **内存管理**: 更好的临时文件管理
- **并发支持**: 支持多个并发执行任务

#### 用户体验
- **详细文档**: 完全重写的 README 和安装指南
- **示例代码**: 提供丰富的 Manim 动画示例
- **配置简化**: 更简单的 Claude Desktop 配置

### 🔧 技术变更

#### API 变更
- **工具签名**: 更新为标准 MCP 工具签名
- **返回格式**: 使用标准 MCP 内容类型
- **参数验证**: 增强的输入参数验证

#### 依赖更新
- **MCP SDK**: 升级到最新版本 (>=1.0.0)
- **Manim**: 支持最新版本 (>=0.17.0)
- **Python**: 支持 Python 3.8+

### 📚 文档

#### 新增文档
- **详细安装指南**: [INSTALL.md](INSTALL.md)
- **API 参考**: 完整的工具和参数文档
- **故障排除**: 常见问题和解决方案
- **开发指南**: 贡献者指南和开发环境设置

#### 文档改进
- **多语言支持**: 中文文档
- **视觉改进**: 添加徽章和图标
- **结构优化**: 更清晰的文档组织

### 🗂️ 文件结构变更

#### 新增文件
```
src/
├── __init__.py          # 包初始化
├── __main__.py          # 主入口点
└── server.py            # 重写的服务器

tests/
├── __init__.py          # 测试包
└── test_server.py       # 基础测试

examples/
└── basic_animation.py   # 示例动画

pyproject.toml           # 项目配置
requirements.txt         # 核心依赖
requirements-dev.txt     # 开发依赖
.pre-commit-config.yaml  # 代码质量工具
INSTALL.md              # 详细安装指南
CHANGELOG.md            # 本文件
```

#### 删除文件
- `src/manim_server.py` - 旧的服务器实现

### 🔄 迁移指南

#### 从旧版本迁移

1. **重新安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **更新 Claude Desktop 配置**：
   ```json
   {
     "mcpServers": {
       "manim-server": {
         "command": "python",
         "args": ["/path/to/manim-mcp-server/src/server.py"]
       }
     }
   }
   ```

3. **API 变更**：
   - 工具名称保持不变
   - 参数格式遵循 MCP 标准
   - 返回格式为标准 MCP 内容类型

### 🎯 下一步计划

#### v0.2.0 计划功能
- [ ] 更多安全功能（代码沙箱）
- [ ] 高级动画模板
- [ ] 批量处理支持
- [ ] 实时预览功能
- [ ] 性能监控

#### 长期目标
- [ ] GUI 界面
- [ ] 云端渲染支持
- [ ] 更多输出格式
- [ ] 协作功能

### 💝 致谢

感谢所有参与重构工作的贡献者和提供反馈的用户。特别感谢：

- [Model Context Protocol](https://modelcontextprotocol.io/) 团队的标准化工作
- [Manim Community](https://www.manim.community/) 的持续支持
- 开源社区的宝贵反馈

---

**注意**: 这是一个重大重构版本，建议所有用户重新安装和配置。 