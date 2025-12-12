# Linux SSH MCP - WindTerm-like Terminal Emulator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/linux-ssh-mcp.svg)](https://pypi.org/project/linux-ssh-mcp/)

🚀 **WindTerm风格的终端模拟器，集成AI助手**

一个功能类似WindTerm的终端模拟器，通过Model Context Protocol (MCP)与AI助手集成，提供多标签页SSH会话管理、交互式终端、会话持久化和脚本自动化功能。

## 核心功能

### 🖥️ 终端模拟器
- **多标签页管理**: 类似浏览器的多标签页SSH会话管理
- **交互式终端**: 真实的PTY模拟，支持完整的终端交互体验
- **终端协议支持**: 支持ANSI/VT100/xterm-256color协议
- **实时输出流**: 流式传输终端输出，支持增量更新

### 🤖 AI助手集成
- **自然语言控制**: 通过AI助手使用自然语言控制终端操作
- **丰富的MCP工具**: 提供完整的终端管理工具集
- **智能命令执行**: AI助手可以理解并执行复杂的终端命令序列

### 💾 会话管理
- **会话持久化**: 保存和恢复完整的终端工作区
- **自动断线重连**: 支持断线重连和会话状态自动恢复
- **多工作区支持**: 可以保存不同的服务器组合配置

### ⚡ 高级功能
- **脚本自动化**: 支持脚本执行和自动化任务
- **性能监控**: 实时连接状态和性能指标监控
- **安全设计**: 多种认证方式，安全凭证管理

## 系统要求

- Python 3.9+
- Linux/macOS/Windows (支持跨平台PTY操作)
- SSH 服务器访问权限

## 快速开始

### 安装

```bash
# 从PyPI安装
pip install linux-ssh-mcp

# Claude Code配置
claude mcp add linux-ssh-mcp python -m linux_ssh_mcp.cli_v2
```

### 服务器配置

配置文件会自动创建在 `~/.ssh-mcp/servers.json`，或手动创建:

```json
{
  "version": "1.0",
  "servers": {
    "server-01": {
      "id": "server-01",
      "host": "192.168.1.100",
      "port": 22,
      "username": "root",
      "password": "your_password"
    }
  }
}
```

### 配置文件搜索路径 (按优先级)

1. `SSH_MCP_CONFIG_PATH` 环境变量指定的路径
2. `~/.ssh-mcp/servers.json` (用户主目录)
3. 平台特定配置目录:
   - Windows: `%APPDATA%/ssh-mcp/servers.json`
   - Linux/Mac: `~/.config/ssh-mcp/servers.json`
4. 当前工作目录 `./servers.json`
5. 项目根目录 `servers.json` (开发环境)

## AI助手命令示例

### 终端会话管理
- "创建一个新的终端标签页连接到 web-server-01"
- "切换到名为 production 的终端标签页"
- "关闭 database-server 的终端会话"
- "调整当前终端窗口大小为 120x40"

### 交互式终端操作
- "在当前终端输入 'ls -la' 并回车"
- "在 web-server 终端中执行 'sudo systemctl status nginx'"
- "获取 database-server 终端的最新输出"
- "查看当前终端的命令历史"

### 多终端管理
- "在所有服务器上批量检查磁盘空间"
- "同时查看三个不同服务器的系统负载"
- "保存当前所有终端会话为 '日常巡检' 工作区"
- "恢复昨天的 '开发调试' 工作区"

## 命令行工具

### 启动 MCP 服务器
```bash
# 启动 MCP 服务器
linux-ssh-mcp server

# 或使用 Python 模块
python -m linux_ssh_mcp.mcp_server_v2
```

### 初始化配置
```bash
# 创建示例配置文件
linux-ssh-mcp init
```

### 测试连接
```bash
# 测试终端连接
linux-ssh-mcp test localhost username

# 指定端口和密码
linux-ssh-mcp test 192.168.1.100 admin --password your_password --port 22
```

### 调试模式
```bash
# 启用调试日志
linux-ssh-mcp server --debug
```

## Python API

```python
from linux_ssh_mcp import SSHManager, ServerConfig

# 创建管理器
ssh_manager = SSHManager(use_pooling=True)

# 添加服务器
config = ServerConfig(
    id="web-server-01",
    host="192.168.1.100",
    port=22,
    username="admin",
    password="password",
    timeout=30
)
ssh_manager.add_server(config)

# 执行命令
result = await ssh_manager.execute_command("web-server-01", "uptime")
print(f"输出: {result.stdout}")
```

## 安全特性

- **多种认证方式**: 密码、SSH密钥
- **连接安全**: SSL/TLS加密
- **访问控制**: 支持IP白名单
- **审计日志**: 完整的操作记录

## 性能特点

- **连接管理**: <100ms建立连接(池化)，<500ms(新建)
- **命令执行**: 简单命令平均<1秒
- **批量操作**: 支持并发执行
- **资源占用**: 基础~50MB，每连接~1MB

## 测试

```bash
# 运行测试套件
python -m pytest tests/
```

## 许可证

MIT License

## 支持

- **问题反馈**: GitHub Issues
- **讨论**: GitHub Discussions

---

**Built with ❤️ for the Linux SSH management community**