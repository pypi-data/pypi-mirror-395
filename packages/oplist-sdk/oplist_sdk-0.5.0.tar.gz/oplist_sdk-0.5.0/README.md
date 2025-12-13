# OpenList Python SDK

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> 一个功能强大、类型安全、开发者友好的 Python SDK，用于与 **OpenList**（AList Fork）API 进行交互。

---

## 📑 目录

- [✨ 核心特性](#-核心特性)
- [🚀 快速开始](#-快速开始)
- [📚 完整 API 参考手册](#-完整-api-参考手册)
  - [1. 初始化](#1-初始化客户端)
  - [2. Auth (认证)](#2-auth-认证)
  - [3. Public (公共)](#3-public-公共)
  - [4. FS (文件系统)](#4-fs-文件系统)
  - [5. Share (分享)](#5-share-分享)
  - [6. Task (任务管理)](#6-task-任务管理)
  - [7. Storage (存储管理)](#7-storage-存储管理)
  - [8. Admin (管理员)](#8-admin-管理员)
- [🔧 数据结构详情](#-数据结构详情)
- [🛡️ 响应处理](#-响应处理)
- [🗓️ 路线图与改进计划](#-路线图与改进计划)

---

## ✨ 核心特性

| 特性 | 描述 |
| :--- | :--- |
| 🎯 **命名空间设计** | 清晰的 API 组织结构 (`client.fs`, `client.storage`, `client.auth`) |
| ⚡ **HTTP/2 支持** | 使用 `httpx` 作为底层引擎，支持 HTTP/2 协议 |
| 🛡️ **纯粹字典响应** | 所有 API 返回标准 JSON 字典，无自定义对象，方便直接处理和序列化 |
| 🔧 **零配置自动登录** | 支持初始化时自动完成认证 |
| 📋 **任务监控** | 内置异步任务管理器 (`client.task`)，支持进度追踪 |

---

## 🚀 快速开始

### 安装依赖

```bash
# 使用 uv (推荐)
uv pip install httpx[http2]

# 或使用 pip
pip install httpx[http2]
```

### 基础用法

#### 🎯 极简模式 (推荐用于脚本)

```python
from openlist_sdk import OpenListClient

# 一行代码初始化 + 自动登录
client = OpenListClient("http://nas:5244", username="admin", password="pwd")

# 直接调用 API (返回字典)
resp = client.fs.list("/my_drive")

if resp["code"] == 200:
    # 成功 (data 也是纯字典/列表，直接操作)
    for f in resp["data"]["content"]:
        print(f"{f['name']} ({'📁' if f['is_dir'] else '📄'} {f['size']} bytes)")
else:
    # 失败
    print(f"Error: {resp['message']}")
```

#### 🔒 严谨模式 (推荐用于 Web 服务)

```python
from openlist_sdk import OpenListClient

with OpenListClient("http://nas:5244") as client:
    # 登录并检查结果
    resp = client.login("admin", "pwd")
    if resp["code"] != 200:
        print("登录失败:", resp["message"])
        exit(1)
    
    # 创建文件夹
    client.fs.mkdir("/local/new_folder")
    
    # 监控任务 (返回任务信息字典)
    task = client.task.copy.wait_for_path(src_path="/src/file.txt")
    if task and task["state"] == 2: # 2 = SUCCEEDED
        print("复制成功")
```

---

## 📚 完整 API 参考手册

### 1. 初始化客户端

使用 `OpenListClient` 作为 SDK 的主要入口。

```python
client = OpenListClient(
    host="http://alist.example.com:5244",
    username="admin",    # 可选
    password="password", # 可选
    otp_code="123456",   # 可选 (2FA) 
    token="xxx",         # 可选
    timeout=30.0,        # 可选
    verify_token=True    # 可选 (初始化时验证 Token)
)
```

### 2. Auth (认证)

命名空间：`client.auth`

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `login(...)` | 用户登录 | `username`, `password`, `otp_code` |
| `logout()` | 用户登出 | 无 |
| `get_me()` | 获取当前用户信息 | 无 |
| `update_me(...)` | 更新用户信息 | `base_path`, `sso_id` |
| `generate_2fa()` | 生成 2FA | 无 |
| `verify_2fa(...)` | 验证 2FA | `code` |
| `list_ssh_keys()` | 列出 SSH 密钥 | 无 |
| `add_ssh_key(...)` | 添加 SSH 密钥 | `title`, `content` |

### 3. Public (公共)

命名空间：`client.public` (无需认证)

| 方法 | 描述 |
| :--- | :--- |
| `settings()` | 获取公共设置 |
| `offline_download_tools()` | 获取离线下载工具列表 |
| `archive_extensions()` | 获取支持的压缩包格式 |

### 4. FS (文件系统)

命名空间：`client.fs`

#### 基础操作

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `list(...)` | 列出目录 | `path`, `password`, `page`, `per_page`, `refresh` |
| `get(...)` | 获取详情 | `path`, `password` |
| `mkdir(...)` | 创建目录 | `path` |
| `rename(...)` | 重命名 | `path`, `name` |
| `remove(...)` | 删除 | `path` |
| `search(...)` | 搜索 | `parent`, `keyword`, `scope` |

#### 移动与复制

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `move(...)` | 移动 | `src_dir`, `dst_dir`, `names` (若空则全移) |
| `copy(...)` | 复制 | `src_dir`, `dst_dir`, `names` (若空则全复制) |
| `recursive_move(...)` | 递归移动 | `src_dir`, `dst_dir` |

#### 上传与下载

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `upload(...)` | 流式上传 | `local_path`, `remote_path` |
| `upload_form(...)` | 表单上传 | `local_path`, `remote_path` |
| `offline_download(...)` | 离线下载 | `urls`, `path`, `tool` |

### 5. Share (分享)

命名空间：`client.share`

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `list(...)` | 列出分享 | `page`, `per_page` |
| `create(...)` | 创建分享 | `path`, `password`, `expire_days` |
| `delete(...)` | 删除分享 | `share_id` |

### 6. Task (任务管理)

SDK 提供了统一的任务监控接口，支持 6 种任务类型：`copy`, `move`, `upload`, `decompress`, `decompress_upload`, `offline_download`。

访问方式：`client.task.{type}.{method}` (例如 `client.task.copy.done()`)

#### 通用管理方法

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `done()` / `undone()` | 获取 已完成/进行中 任务 | 无 |
| `cancel(...)` | 取消任务 | `task_id` |
| `retry(...)` | 重试任务 | `task_id` |
| `clear_done()` | 清除记录 | 无 |
| `wait_all(...)` | 等待所有完成 | `timeout`, `interval` |

#### 智能查找方法

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `find_by_path(...)` | 按 `src_path`/`dst_path` 查找任务 | `src_path`, `dst_path`, `include_done` |
| `find_exact(...)` | 按路径精确查获取任务 | `src_path`, `dst_path` |
| `wait_for_path(...)` | 等待特定路径的任务完成 | `src_path`, `dst_path`, `timeout` |
| `has_pending_for_path(...)` | 检查是否有进行中的任务 | `src_path`, `dst_path` |

### 7. Storage (存储管理)

命名空间：`client.storage` (原 `client.admin.storage`)

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `list(...)` | 列出所有挂载的存储 | `page`, `per_page` |
| `get(...)` | 获取指定存储详情 | `storage_id` |
| `create(...)` | 挂载新存储 (支持详细驱动配置) | `mount_path`, `driver`, `cache`, `remark`, `**config` |
| `update(...)` | 更新存储配置 | `storage_id`, `**kwargs` |
| `delete(...)` | 删除/卸载存储 | `storage_id` |
| `enable(...)` | 启用存储 | `storage_id` |
| `disable(...)` | 禁用存储 | `storage_id` |
| `reload()` | 重新加载所有存储 | 无 |

### 8. Admin (管理员)

命名空间：`client.admin`

#### 用户管理 (`.user`)

| 方法 | 描述 | 参数 |
| :--- | :--- | :--- |
| `list(...)` | 列出用户 | `page`, `per_page` |
| `create(...)` | 创建用户 | `username`, `password`, `role`, `base_path` |
| `update(...)` | 更新用户 | `user_id`, `**kwargs` |
| `delete(...)` | 删除用户 | `user_id` |

#### 设置与元数据 (`.setting` / `.meta`)

| 命名空间 | 方法 | 描述 | 参数 |
| :--- | :--- | :--- | :--- |
| `setting` | `list(...)` | 列出设置 | `page`, `per_page` |
| `setting` | `get(...)` | 获取设置 | `key` |
| `setting` | `save(...)` | 保存设置 | `items` (List) |
| `meta` | `list(...)` | 列出元数据 | `page`, `per_page` |
| `meta` | `create(...)` | 创建元数据 | `path`, `password`, `hide`, `readme` |
| `meta` | `delete(...)` | 删除元数据 | `meta_id` |

#### 其他管理 (`.index` / `.driver`)

| 命名空间 | 方法 | 描述 | 参数 |
| :--- | :--- | :--- | :--- |
| `index` | `build(...)` | 重建搜索索引 | `path` |
| `index` | `stop()` | 停止构建 | 无 |
| `index` | `progress()`| 获取构建进度 | 无 |
| `driver` | `list()` | 列出可用驱动 | 无 |
| `driver` | `info(...)` | 获取驱动参数 | `driver_name` |

---

## 🔧 数据结构详情

SDK 完全返回 Python 原生字典类型，`data` 字段的结构完全对应 API JSON 响应。

- **`fs.list` / `fs.get`**: `{"name": "foo", "is_dir": true, "size": 1024, ...}`
- **`task.*`**: `{"id": "...", "state": 2, "name": "...", ...}`

---

## 🛡️ 响应处理

所有 API 方法都返回一个标准的 Python 字典（`dict`）。

**统一响应结构：**

```python
{
    "code": 200,      # HTTP 状态码或业务状态码 (200=成功)
    "message": "success", # 状态描述或错误信息
    "data": ...       # 业务数据 (可能是对象、列表或 None)
}
```

**示例：**

```python
resp = client.fs.list("/")

if resp["code"] == 200:
    files = resp["data"]["content"] # 直接像操作 JSON 一样操作
    print(files[0]["name"])
else:
    # 失败
    print(f"Error: {resp.get('message')}")
```

---

## 🗓️ 路线图与改进计划

### 🛠️ 近期计划 (Coming Soon)
- [ ] **完善测试套件**: 增加单元测试，移除测试代码中的硬编码凭据，改用 `.env` 配置。
- [ ] **日志系统**: 添加基于 `logging` 模块的日志记录，方便调试。
- [ ] **CLI 工具**: 开发基于 `Typer` 的命令行工具，支持 `oplist ls`, `oplist cp` 等命令。

### 🔮 远期规划
- [ ] **异步支持**: 提供 `AsyncOpenListClient`，基于 `httpx` 的异步能力支持高并发操作。
- [ ] **重试机制**: 对网络请求添加自动重试策略。

---

<p align="center">
  Made with ❤️ for OpenList Community
</p>




