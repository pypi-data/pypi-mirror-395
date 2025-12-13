# Midjourney Best Experience MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Midjourney Best Experience API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-midjourney_best_experience`）
5. 🎉 点击 **"安装 MCP"** 按钮
6. ✅ 完成！即可在您的应用中使用

### EMCP 平台优势：

- ✨ **零配置**：无需手动编辑配置文件
- 🎨 **可视化管理**：图形界面轻松管理所有 MCP 服务器
- 🔐 **安全可靠**：统一管理 API 密钥和认证信息
- 🚀 **一键安装**：MCP 广场提供丰富的服务器选择
- 📊 **使用统计**：实时查看服务调用情况

立即访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)** 开始您的 MCP 之旅！


---

## 简介

这是一个 MCP 服务器，用于访问 Midjourney Best Experience API。

- **PyPI 包名**: `bach-midjourney_best_experience`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-midjourney_best_experience
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-midjourney_best_experience bach_midjourney_best_experience

# 或指定版本
uvx --from bach-midjourney_best_experience@latest bach_midjourney_best_experience
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-midjourney_best_experience

# 运行（命令名使用下划线）
bach_midjourney_best_experience
```

## 配置

### API 认证

此 API 需要认证。请设置环境变量:

```bash
export API_KEY="your_api_key_here"
```

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `API_KEY` | API 密钥 | 是 |
| `PORT` | 不适用 | 否 |
| `HOST` | 不适用 | 否 |



### 在 Cursor 中使用

编辑 Cursor MCP 配置文件 `~/.cursor/mcp.json`:


```json
{
  "mcpServers": {
    "bach-midjourney_best_experience": {
      "command": "uvx",
      "args": ["--from", "bach-midjourney_best_experience", "bach_midjourney_best_experience"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 在 Claude Desktop 中使用

编辑 Claude Desktop 配置文件 `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bach-midjourney_best_experience": {
      "command": "uvx",
      "args": ["--from", "bach-midjourney_best_experience", "bach_midjourney_best_experience"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `action_relaxuu0026v`

- Do the relax action  - You can perform upsample (same as the UI, U2...), variation (V1, V2...), zoom out 1.5x, zoom out 2x, pan, and other operations on the images generated in the first step

**端点**: `POST /mj/action-relax`


**参数**:

- `action` (string) *必需*: the action is the enumeration values returned in the action list in the callback

- `image_id` (string) *必需*: the params image_id in the relax job callback or task_id eg: 9c4410a2-2bb4-2428-b0e4-0a3b41f48e3b

- `hook_url` (string): if set will notify the result to your hook_url



---


### `action_fastuu0026v`

- Do the fast action  - You can perform upsample (same as the UI, U2...), variation (V1, V2...), zoom out 1.5x, zoom out 2x, pan, and other operations on the images generated in the first step

**端点**: `POST /mj/action-fast`


**参数**:

- `action` (string) *必需*: the action is the enumeration values returned in the action list in the callback

- `image_id` (string) *必需*: the params image_id in the fast job callback or task_id eg: 6a028074-884e-7840-2ef4-715a5ab3b6c7

- `hook_url` (string): Example value: https://www.google.com



---


### `generate_relax`

generate the images relax Generate queue asynchronous notifications to hook_ url, overall generation time is Depends on account status and task queuing

**端点**: `POST /mj/generate-relax`


**参数**:

- `prompt` (string) *必需*: Example value: a beautiful cat --ar 1920:1080

- `hook_url` (string): if set will notify the result to your hook_url



---


### `generate_fast`

generate the images fast   Generate queue asynchronous notifications to hook_ url, overall generation time is around 40-60s

**端点**: `POST /mj/generate-fast`


**参数**:

- `prompt` (string) *必需*: Example value: a beautiful cat --ar 1920:1080

- `hook_url` (string): if set will notify the result to your hook_url



---


### `get_job_by_task_id`

you can get the generate job  and  action job status by the task_id, and the task_id will expired at 24 hours after

**端点**: `GET /mj/get-task-id`


**参数**:

- `task_id` (string) *必需*: Example value: 6ddd8121-2ae4-af61-b73d-eaefc8318d09



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
