# MCP 配置故障排查指南

## 🔴 常见问题：Cursor 中 MCP 配置显示红点

### 问题描述
- Cursor 中配置 MCP 后显示红点报错
- 单独运行 `python -m mobile_mcp.mcp.mcp_server` 可以执行
- 但在 Cursor 中无法使用

---

## ✅ 完整配置流程（从零开始）

### 第一步：安装 mobile-mcp-ai

```bash
# 基础安装（推荐）
pip install mobile-mcp-ai

# 或者完整安装（包含AI功能）
pip install mobile-mcp-ai[ai]

# 验证安装
pip show mobile-mcp-ai
python -c "import mobile_mcp; print('✅ 安装成功')"
```

### 第二步：找到正确的 Python 路径

**这是最关键的一步！** MCP 配置失败最常见的原因就是 Python 路径不对。

#### macOS/Linux：

```bash
# 查看当前使用的 Python 路径
which python
# 或
which python3

# 如果使用虚拟环境
which python  # 在激活虚拟环境后运行
```

常见路径示例：
- 系统 Python：`/usr/bin/python3`
- Homebrew Python：`/opt/homebrew/bin/python3`
- 虚拟环境：`/Users/你的用户名/Desktop/mobile_mcp/venv/bin/python`

#### Windows：

```bash
# 在命令提示符中运行
where python
```

常见路径示例：
- `C:\Python311\python.exe`
- `C:\Users\你的用户名\AppData\Local\Programs\Python\Python311\python.exe`
- 虚拟环境：`C:\path\to\venv\Scripts\python.exe`

### 第三步：配置 Cursor MCP

#### 配置文件位置

**macOS/Linux：**
```
~/.cursor/mcp.json
```

**Windows：**
```
%APPDATA%\Cursor\mcp.json
```

或者在你的项目根目录创建：
```
/path/to/your/project/.cursor/mcp.json
```

#### 配置内容（⭐ 推荐配置）

```json
{
  "mcpServers": {
    "mobile-automation": {
      "command": "/absolute/path/to/python",
      "args": ["-m", "mobile_mcp.mcp.mcp_server"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

**关键点说明：**

1. **`command`** - 必须是 Python 的**绝对路径**
   - ✅ 正确：`"/opt/homebrew/bin/python3"`
   - ✅ 正确：`"/Users/mac/Desktop/mobile_mcp/venv/bin/python"`
   - ❌ 错误：`"python"`（相对路径可能找不到）
   - ❌ 错误：`"python3"`（相对路径可能找不到）

2. **`args`** - 模块启动参数
   - ✅ 正确：`["-m", "mobile_mcp.mcp.mcp_server"]`
   - ❌ 错误：`["mcp_server.py"]`
   - ❌ 错误：`["-m", "mcp.mcp_server"]`

3. **`cwd`** - 工作目录（可选但推荐）
   - 设置为你的项目根目录
   - 测试脚本会保存到 `{cwd}/tests/` 目录

#### 实际配置示例

**示例 1：使用系统 Python（macOS）**

```json
{
  "mcpServers": {
    "mobile-automation": {
      "command": "/opt/homebrew/bin/python3",
      "args": ["-m", "mobile_mcp.mcp.mcp_server"],
      "cwd": "/Users/mac/Desktop/mobile_mcp"
    }
  }
}
```

**示例 2：使用虚拟环境（macOS）**

```json
{
  "mcpServers": {
    "mobile-automation": {
      "command": "/Users/mac/Desktop/mobile_mcp/venv/bin/python",
      "args": ["-m", "mobile_mcp.mcp.mcp_server"],
      "cwd": "/Users/mac/Desktop/mobile_mcp"
    }
  }
}
```

**示例 3：Windows 配置**

```json
{
  "mcpServers": {
    "mobile-automation": {
      "command": "C:\\Python311\\python.exe",
      "args": ["-m", "mobile_mcp.mcp.mcp_server"],
      "cwd": "C:\\Users\\YourName\\Desktop\\mobile_mcp"
    }
  }
}
```

**示例 4：完整版配置（带环境变量）**

```json
{
  "mcpServers": {
    "mobile-automation": {
      "command": "/opt/homebrew/bin/python3",
      "args": ["-m", "mobile_mcp.mcp.mcp_server"],
      "cwd": "/Users/mac/Desktop/mobile_mcp",
      "env": {
        "MOBILE_MCP_MODE": "full",
        "MOBILE_DEVICE_ID": "auto",
        "DEFAULT_PLATFORM": "android"
      }
    }
  }
}
```

**示例 5：简化版配置（32个工具）**

```json
{
  "mcpServers": {
    "mobile-automation": {
      "command": "/opt/homebrew/bin/python3",
      "args": ["-m", "mobile_mcp.mcp.mcp_server"],
      "env": {
        "MOBILE_MCP_MODE": "simple"
      }
    }
  }
}
```

### 第四步：验证配置

#### 1. 测试 Python 和模块是否正常

在终端运行（使用你配置的 Python 路径）：

```bash
# 替换成你的 Python 路径
/opt/homebrew/bin/python3 -m mobile_mcp.mcp.mcp_server --version

# 或者测试导入
/opt/homebrew/bin/python3 -c "from mobile_mcp.mcp import mcp_server; print('✅ 模块正常')"
```

如果这一步失败，说明：
- Python 环境中没有安装 mobile-mcp-ai
- 需要在正确的环境中安装：`/opt/homebrew/bin/python3 -m pip install mobile-mcp-ai`

#### 2. 检查 JSON 格式是否正确

使用在线工具验证 JSON 格式：https://jsonlint.com/

常见 JSON 错误：
- ❌ 多余的逗号：`"cwd": "/path",` ← 最后一项不应有逗号
- ❌ 路径分隔符错误（Windows）：用 `\\` 或 `/`，不能用单个 `\`
- ❌ 引号不匹配

### 第五步：重启 Cursor

**⚠️ 非常重要！**

1. **完全退出** Cursor（不是关闭窗口）
   - macOS：`Cmd + Q` 或菜单 → Quit Cursor
   - Windows：完全关闭应用

2. 重新启动 Cursor

3. 等待 10-20 秒让 MCP 服务器启动

### 第六步：查看 MCP 日志

#### 在 Cursor 中查看日志

1. 打开 Cursor
2. 按 `Cmd/Ctrl + Shift + P` 打开命令面板
3. 搜索 "MCP" 或 "Output"
4. 查看 MCP 相关日志

#### 手动查找日志文件

**macOS/Linux：**
```bash
# 在 Cursor 的日志目录中查找
ls -la ~/.cursor/logs/
cat ~/.cursor/logs/user-mobile-automation.log
```

**Windows：**
```
%APPDATA%\Cursor\logs\
```

---

## 🔍 常见错误及解决方案

### 错误 1：`ModuleNotFoundError: No module named 'mobile_mcp'`

**原因**：Python 环境中没有安装 mobile-mcp-ai

**解决方案**：
```bash
# 使用配置中的 Python 路径安装
/opt/homebrew/bin/python3 -m pip install mobile-mcp-ai

# 或者在虚拟环境中安装
source /path/to/venv/bin/activate
pip install mobile-mcp-ai
```

### 错误 2：`command not found: python`

**原因**：配置中的 Python 路径不正确

**解决方案**：
1. 找到正确的 Python 路径：`which python3`
2. 使用绝对路径更新 mcp.json
3. 重启 Cursor

### 错误 3：`Permission denied`

**原因**：Python 文件没有执行权限

**解决方案**（macOS/Linux）：
```bash
chmod +x /path/to/python
```

### 错误 4：JSON 解析错误

**原因**：mcp.json 格式不正确

**解决方案**：
1. 检查所有引号、逗号、括号是否匹配
2. 使用 https://jsonlint.com/ 验证
3. Windows 路径使用 `\\` 或 `/`

### 错误 5：工具列表为空

**原因**：MCP 服务器启动了但没有注册工具

**解决方案**：
1. 检查版本：`pip show mobile-mcp-ai`
2. 升级到最新版：`pip install --upgrade mobile-mcp-ai`
3. 清除缓存重启

### 错误 6：`adb: command not found`（使用时报错）

**原因**：没有安装 Android SDK Platform Tools

**解决方案**：

**macOS：**
```bash
brew install android-platform-tools
```

**Linux：**
```bash
sudo apt install adb
```

**Windows：**
下载 [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)

---

## 📋 完整检查清单

逐项检查以下内容：

- [ ] Python 已安装：`python3 --version`
- [ ] mobile-mcp-ai 已安装：`pip show mobile-mcp-ai`
- [ ] Python 路径正确：`which python3`
- [ ] 模块可导入：`python3 -c "import mobile_mcp"`
- [ ] mcp.json 格式正确（用 jsonlint 验证）
- [ ] mcp.json 中的 Python 路径是绝对路径
- [ ] 已完全退出并重启 Cursor
- [ ] 等待 10-20 秒后测试
- [ ] 查看 MCP 日志确认启动成功

---

## 🎯 快速测试步骤

### 1. 验证 Python 环境

```bash
# 找到 Python 路径
which python3

# 测试安装
/your/python/path -c "import mobile_mcp; print('✅')"
```

### 2. 创建最小化配置

```json
{
  "mcpServers": {
    "mobile-automation": {
      "command": "/your/python/path",
      "args": ["-m", "mobile_mcp.mcp.mcp_server"]
    }
  }
}
```

### 3. 重启 Cursor 并测试

在 Cursor 中输入：
```
@MCP 列出所有连接的移动设备
```

如果看到设备列表，说明配置成功！

---

## 🆘 仍然无法解决？

### 收集诊断信息

```bash
# 1. Python 信息
python3 --version
which python3

# 2. 包信息
pip show mobile-mcp-ai
pip list | grep mobile

# 3. 测试导入
python3 -c "import mobile_mcp; print(mobile_mcp.__file__)"

# 4. 查看 MCP 配置
cat ~/.cursor/mcp.json
```

### 提供以下信息以获取帮助

1. 操作系统版本
2. Python 版本
3. mobile-mcp-ai 版本
4. mcp.json 配置内容（去掉敏感信息）
5. Cursor 版本
6. 完整的错误日志

### 联系方式

- GitHub Issues：https://github.com/test111ddff-hash/mobile-mcp-ai/issues
- Gitee Issues：https://gitee.com/chang-xinping/mobile-automation-mcp-service/issues
- 微信：见 README.md

---

## 💡 最佳实践建议

1. **使用虚拟环境**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows
   pip install mobile-mcp-ai
   ```

2. **配置中使用虚拟环境的 Python**
   ```json
   {
     "mcpServers": {
       "mobile-automation": {
         "command": "/absolute/path/to/venv/bin/python",
         "args": ["-m", "mobile_mcp.mcp.mcp_server"]
       }
     }
   }
   ```

3. **定期更新**
   ```bash
   pip install --upgrade mobile-mcp-ai
   ```

4. **查看日志**
   - 遇到问题先看 MCP 日志
   - 日志中通常有明确的错误信息

---

**祝你配置成功！如果还有问题，欢迎通过微信或 Issues 反馈。**






