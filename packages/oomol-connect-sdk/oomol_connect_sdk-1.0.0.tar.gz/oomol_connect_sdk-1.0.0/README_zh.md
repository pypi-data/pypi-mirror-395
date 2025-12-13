# Oomol Connect SDK for Python

[English](README.md) | 中文

Oomol Connect 的官方 Python SDK，提供完整、类型安全的接口与 Oomol Connect 服务交互。

## 特性

- ✨ **完整的 API 支持** - 完全覆盖所有 Oomol Connect API 端点
- 🔄 **智能轮询** - 支持指数退避策略的智能轮询
- 📊 **进度监控** - 任务进度和日志的实时回调
- 📁 **文件上传** - 支持单文件和多文件上传
- 🎯 **类型安全** - 基于 TypedDict 的完整类型注解
- ⚡ **异步优先** - 基于 asyncio 和 httpx 的现代异步设计
- 🛡️ **错误处理** - 全面的错误分类和处理

## 安装

```bash
pip install oomol-connect-sdk
```

## 快速开始

```python
import asyncio
from oomol_connect_sdk import OomolConnectClient

async def main():
    async with OomolConnectClient(
        base_url="http://localhost:3000/api",
        api_token="your-api-token"
    ) as client:
        # 运行任务并获取结果
        result = await client.tasks.run({
            "manifest": "audio-lab::text-to-audio",
            "inputValues": {"text": "你好，世界"}
        })

        print(f"任务 ID: {result['task_id']}")
        print(f"结果: {result['result']}")

asyncio.run(main())
```

## 核心概念

### 客户端初始化

```python
from oomol_connect_sdk import OomolConnectClient

client = OomolConnectClient(
    base_url="/api",              # API 基础 URL
    api_token="your-token",       # API Token（自动添加为 Bearer token）
    default_headers={},           # 自定义请求头（可选）
    timeout=30.0                  # 请求超时时间（秒）
)
```

### 任务管理

```python
# 简单的任务执行（推荐）
result = await client.tasks.run({
    "manifest": "flow-name",
    "inputValues": {"input1": "value1"}
})

# 带进度监控
result = await client.tasks.run(
    {
        "manifest": "flow-name",
        "inputValues": {"input": "value"}
    },
    {
        "interval_ms": 1000,
        "timeout_ms": 60000,
        "on_progress": lambda task: print(f"状态: {task['status']}"),
        "on_log": lambda log: print(f"日志: {log['type']}")
    }
)
```

### 输入值格式

SDK 自动规范化三种输入格式：

```python
# 格式 1: 简单对象格式（最常用）
{"input1": "value1", "input2": 123}

# 格式 2: 数组格式
[
    {"handle": "input1", "value": "value1"},
    {"handle": "input2", "value": 123}
]

# 格式 3: 节点格式（多节点场景）
[
    {
        "nodeId": "node1",
        "inputs": [{"handle": "input1", "value": "value1"}]
    }
]
```

### 文件上传

```python
# 单文件上传
with open("test.txt", "rb") as f:
    result = await client.tasks.run_with_files(
        "pkg::file-processor",
        {"input1": "value"},
        f
    )

# 多文件上传
with open("file1.txt", "rb") as f1, open("file2.txt", "rb") as f2:
    result = await client.tasks.run_with_files(
        "pkg::multi-file-processor",
        {"input1": "value"},
        [f1, f2]
    )
```

## API 参考

### 任务客户端 (TasksClient)

核心任务管理 API：

- `list()` - 列出所有任务
- `create(request)` - 创建任务（JSON 格式）
- `create_with_files(manifest, input_values, files)` - 创建任务并上传文件
- `get(task_id)` - 获取任务详情
- `stop(task_id)` - 停止任务
- `get_logs(task_id)` - 获取任务日志
- `wait_for_completion(task_id, options)` - 轮询直到任务完成
- `create_and_wait(request, polling_options)` - 创建并等待完成
- `run(request, polling_options)` - **推荐** - 一步运行并获取结果
- `run_with_files(manifest, input_values, files, polling_options)` - 一步运行（含文件）

### 流程客户端 (FlowsClient)

```python
# 列出所有流程
flows_response = await client.flows.list()
for flow in flows_response["flows"]:
    print(flow["name"], flow["path"])
```

### 区块客户端 (BlocksClient)

```python
# 列出所有区块
blocks_response = await client.blocks.list()
for block in blocks_response["blocks"]:
    print(block["package"], block["name"])
```

### 包管理客户端 (PackagesClient)

```python
# 列出已安装的包
packages = await client.packages.list()

# 安装包
install_task = await client.packages.install("package-name", "1.0.0")

# 安装并等待完成
install_task = await client.packages.install_and_wait("package-name", "1.0.0")
```

## 轮询选项

```python
from oomol_connect_sdk import BackoffStrategy

polling_options = {
    "interval_ms": 2000,                    # 轮询间隔（毫秒）
    "timeout_ms": 300000,                   # 超时时间（毫秒）
    "max_interval_ms": 10000,               # 最大间隔（毫秒）
    "backoff_strategy": BackoffStrategy.EXPONENTIAL,  # 退避策略
    "backoff_factor": 1.5,                  # 退避系数
    "on_progress": lambda task: ...,        # 进度回调
    "on_log": lambda log: ...               # 日志回调
}
```

## 错误处理

```python
from oomol_connect_sdk import (
    OomolConnectError,      # 基类
    ApiError,               # HTTP 错误
    TaskFailedError,        # 任务执行失败
    TaskStoppedError,       # 任务被停止
    TimeoutError,           # 轮询超时
    InstallFailedError      # 包安装失败
)

try:
    result = await client.tasks.run({
        "manifest": "flow-1",
        "inputValues": {"input": "test"}
    })
except TaskFailedError as e:
    print(f"任务失败: {e.task_id}")
except ApiError as e:
    print(f"HTTP {e.status}: {e.message}")
```

## 高级用法

### 并发任务

```python
import asyncio

tasks = [
    client.tasks.run({
        "manifest": "flow-1",
        "inputValues": {"input": f"test-{i}"}
    })
    for i in range(5)
]

results = await asyncio.gather(*tasks)
```

### 自定义退避策略

```python
from oomol_connect_sdk import BackoffStrategy

result = await client.tasks.run(
    {"manifest": "long-running-flow", "inputValues": {}},
    {
        "interval_ms": 1000,
        "max_interval_ms": 5000,
        "backoff_strategy": BackoffStrategy.EXPONENTIAL,
        "backoff_factor": 2.0
    }
)
```

## 示例

查看 `examples/` 目录获取更多示例：

- `basic_usage.py` - 基础使用示例
- `advanced_usage.py` - 高级功能和模式

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 类型检查
mypy oomol_connect_sdk
```

## 依赖要求

- Python >= 3.8
- httpx >= 0.27.0

## 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情

## 链接

- **PyPI**: https://pypi.org/project/oomol-connect-sdk/
- **源代码**: https://github.com/oomol/oomol-connect-sdk-py
- **问题追踪**: https://github.com/oomol/oomol-connect-sdk-py/issues
- **TypeScript 版本**: https://github.com/oomol/oomol-connect-sdk-ts

## 贡献

欢迎贡献！请随时提交 Pull Request。
