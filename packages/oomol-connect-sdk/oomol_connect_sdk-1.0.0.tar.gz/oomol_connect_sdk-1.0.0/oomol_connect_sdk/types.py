"""类型定义"""

from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union


# ============ 通用类型 ============

TaskStatus = Literal["created", "pending", "running", "completed", "failed", "stopped"]


class InputHandle(TypedDict, total=False):
    """输入句柄"""
    handle: str
    json_schema: Optional[Dict[str, Any]]


class InputValue(TypedDict):
    """输入值"""
    handle: str
    value: Any


class NodeInputs(TypedDict):
    """节点输入"""
    nodeId: str
    inputs: List[InputValue]


# 输入值的三种格式
TaskInputValues = Union[
    Dict[str, Any],  # 格式1: 简单对象格式
    List[InputValue],  # 格式2: 数组格式
    List[NodeInputs]  # 格式3: 节点格式（多节点）
]


# ============ Task 相关类型 ============

class Task(TypedDict, total=False):
    """任务"""
    id: str
    status: TaskStatus
    project_id: str
    manifest_path: str
    inputValues: Optional[List[NodeInputs]]
    created_at: int  # Unix 时间戳（毫秒）
    updated_at: int


class CreateTaskRequest(TypedDict, total=False):
    """创建任务请求"""
    manifest: str
    inputValues: Optional[TaskInputValues]


class TaskLog(TypedDict, total=False):
    """任务日志"""
    id: int
    project_name: str
    session_id: str
    node_id: str
    manifest_path: str
    type: str
    event: Optional[Dict[str, Any]]
    created_at: int


class ListTasksResponse(TypedDict):
    """列出任务响应"""
    tasks: List[Task]


# ============ Flow 相关类型 ============

class FlowInputNode(TypedDict, total=False):
    """Flow 输入节点"""
    id: str
    inputs: Optional[List[InputHandle]]


class Flow(TypedDict, total=False):
    """流程"""
    name: str
    path: str
    description: Optional[str]
    inputs: Optional[List[FlowInputNode]]


class ListFlowsResponse(TypedDict):
    """列出流程响应"""
    flows: List[Flow]


# ============ Block 相关类型 ============

class Block(TypedDict, total=False):
    """区块"""
    package: str
    name: str
    path: str
    description: Optional[str]
    inputs: Optional[List[InputHandle]]


class ListBlocksResponse(TypedDict):
    """列出区块响应"""
    blocks: List[Block]


# ============ Package 相关类型 ============

InstallTaskStatus = Literal["pending", "running", "success", "failed"]


class PackageDependency(TypedDict, total=False):
    """包依赖"""
    name: str
    version: Optional[str]


class Package(TypedDict, total=False):
    """包"""
    name: str
    version: str
    path: str
    description: Optional[str]


class InstallTask(TypedDict, total=False):
    """安装任务"""
    id: str
    name: str
    version: Optional[str]
    status: InstallTaskStatus
    packagePath: Optional[str]
    dependencies: Optional[List[PackageDependency]]
    error: Optional[str]
    createdAt: int
    updatedAt: int


class ListPackagesResponse(TypedDict):
    """列出包响应"""
    packages: List[Package]


class ListInstallTasksResponse(TypedDict):
    """列出安装任务响应"""
    tasks: List[InstallTask]


# ============ 配置类型 ============

class BackoffStrategy(str, Enum):
    """退避策略"""
    FIXED = "fixed"
    EXPONENTIAL = "exponential"


class PollingOptions(TypedDict, total=False):
    """轮询选项"""
    interval_ms: int  # 轮询间隔，默认 2000ms
    timeout_ms: Optional[int]  # 超时时间，默认无限制
    max_interval_ms: int  # 最大间隔，默认 10000ms
    backoff_strategy: BackoffStrategy  # 退避策略
    backoff_factor: float  # 退避系数，默认 1.5
    on_progress: Optional[Callable[[Task], None]]  # 进度回调
    on_log: Optional[Callable[[TaskLog], None]]  # 日志回调


class ClientOptions(TypedDict, total=False):
    """客户端配置"""
    base_url: str  # 基础 URL，默认 "/api"
    api_token: Optional[str]  # API Token（自动添加为 Bearer token）
    default_headers: Optional[Dict[str, str]]  # 默认请求头
    timeout: Optional[float]  # 请求超时时间（秒）


# ============ 运行任务结果类型 ============

class RunResult(TypedDict, total=False):
    """运行任务结果"""
    task_id: str
    task: Task
    logs: List[TaskLog]
    result: Optional[Any]  # 从日志中自动提取的结果
