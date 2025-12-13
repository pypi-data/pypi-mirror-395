"""工具函数"""

import asyncio
from typing import Any, Dict, List
from urllib.parse import urljoin

from .types import InputValue, NodeInputs, TaskInputValues


def normalize_input_values(input_values: TaskInputValues) -> List[NodeInputs]:
    """规范化输入值，转换为 NodeInputs[] 格式

    支持三种格式：
    1. 对象格式：{"input1": "value1", "input2": 123}
    2. 数组格式：[{"handle": "input1", "value": "value1"}, ...]
    3. 节点格式：[{"nodeId": "node1", "inputs": [...]}]

    Args:
        input_values: 输入值（三种格式之一）

    Returns:
        标准化的 NodeInputs 列表
    """
    if not input_values:
        return []

    # 格式3：已经是 NodeInputs[] 格式
    if isinstance(input_values, list) and len(input_values) > 0:
        first = input_values[0]
        if isinstance(first, dict) and "nodeId" in first:
            return input_values  # type: ignore

    # 格式2：数组格式 [{"handle": ..., "value": ...}]
    if isinstance(input_values, list):
        return [
            NodeInputs(
                nodeId="_",
                inputs=input_values  # type: ignore
            )
        ]

    # 格式1：对象格式 {"input1": "value1"}
    if isinstance(input_values, dict):
        inputs: List[InputValue] = [
            InputValue(handle=key, value=value)
            for key, value in input_values.items()
        ]
        return [
            NodeInputs(
                nodeId="_",
                inputs=inputs
            )
        ]

    return []


def build_url(base_url: str, path: str) -> str:
    """构建完整 URL

    Args:
        base_url: 基础 URL
        path: 路径

    Returns:
        完整的 URL
    """
    # 确保 base_url 以 / 结尾
    if not base_url.endswith("/"):
        base_url += "/"

    # 确保 path 不以 / 开头
    if path.startswith("/"):
        path = path[1:]

    return urljoin(base_url, path)


async def sleep(ms: int) -> None:
    """睡眠指定毫秒数

    Args:
        ms: 毫秒数
    """
    await asyncio.sleep(ms / 1000.0)


def extract_result_from_logs(logs: List[Any]) -> Any:
    """从日志中提取结果

    查找 BlockFinished 类型的日志，提取其中的结果

    Args:
        logs: 任务日志列表

    Returns:
        提取的结果，如果未找到则返回 None
    """
    for log in reversed(logs):  # 从后往前找，最新的结果
        if isinstance(log, dict) and log.get("type") == "BlockFinished":
            event = log.get("event")
            if event and isinstance(event, dict):
                return event.get("result")
    return None
