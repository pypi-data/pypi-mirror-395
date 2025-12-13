"""Tasks 客户端"""

import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .errors import TaskFailedError, TaskStoppedError, TimeoutError
from .types import (
    BackoffStrategy,
    CreateTaskRequest,
    ListTasksResponse,
    PollingOptions,
    RunResult,
    Task,
    TaskInputValues,
    TaskLog,
)
from .utils import extract_result_from_logs, normalize_input_values, sleep

if TYPE_CHECKING:
    from .client import OomolConnectClient


class TasksClient:
    """Tasks API 客户端

    这是 SDK 的核心客户端，提供任务的创建、管理和监控功能。
    """

    def __init__(self, client: "OomolConnectClient") -> None:
        """初始化 Tasks 客户端

        Args:
            client: 主客户端实例
        """
        self._client = client

    async def list(self) -> ListTasksResponse:
        """列出所有任务

        Returns:
            包含任务列表的响应

        Example:
            >>> tasks_response = await client.tasks.list()
            >>> for task in tasks_response["tasks"]:
            ...     print(task["id"], task["status"])
        """
        return await self._client.request("/v1/tasks", method="GET")

    async def create(self, request: CreateTaskRequest) -> Dict[str, Any]:
        """创建任务（JSON 格式）

        Args:
            request: 创建任务请求

        Returns:
            创建的任务信息

        Example:
            >>> task = await client.tasks.create({
            ...     "manifest": "audio-lab::text-to-audio",
            ...     "inputValues": {"text": "你好"}
            ... })
            >>> print(task["id"])
        """
        # 规范化输入值
        request_data = dict(request)
        if "inputValues" in request_data and request_data["inputValues"]:
            request_data["inputValues"] = normalize_input_values(
                request_data["inputValues"]
            )

        return await self._client.request(
            "/v1/tasks",
            method="POST",
            json_data=request_data
        )

    async def create_with_files(
        self,
        manifest: str,
        input_values: Optional[TaskInputValues] = None,
        files: Optional[Union[Any, List[Any]]] = None,
    ) -> Dict[str, Any]:
        """创建任务（支持文件上传）

        Args:
            manifest: 流程/区块路径
            input_values: 输入值
            files: 文件或文件列表

        Returns:
            创建的任务信息

        Example:
            >>> with open("test.txt", "rb") as f:
            ...     task = await client.tasks.create_with_files(
            ...         "pkg::block",
            ...         {"input1": "value"},
            ...         f
            ...     )
        """
        # 准备表单数据
        data = {"manifest": manifest}

        # 规范化输入值
        if input_values:
            import json
            normalized = normalize_input_values(input_values)
            data["inputValues"] = json.dumps(normalized)

        # 准备文件数据
        files_data = None
        if files:
            if not isinstance(files, list):
                files = [files]
            files_data = [("files", f) for f in files]

        return await self._client.request(
            "/v1/tasks",
            method="POST",
            data=data,
            files=files_data
        )

    async def get(self, task_id: str) -> Task:
        """获取任务详情

        Args:
            task_id: 任务 ID

        Returns:
            任务详情

        Example:
            >>> task = await client.tasks.get("task-123")
            >>> print(task["status"])
        """
        return await self._client.request(f"/v1/tasks/{task_id}", method="GET")

    async def stop(self, task_id: str) -> Task:
        """停止任务

        Args:
            task_id: 任务 ID

        Returns:
            更新后的任务信息

        Example:
            >>> task = await client.tasks.stop("task-123")
            >>> print(task["status"])  # "stopped"
        """
        return await self._client.request(
            f"/v1/tasks/{task_id}/stop",
            method="POST"
        )

    async def get_logs(self, task_id: str) -> List[TaskLog]:
        """获取任务日志

        Args:
            task_id: 任务 ID

        Returns:
            任务日志列表

        Example:
            >>> logs = await client.tasks.get_logs("task-123")
            >>> for log in logs:
            ...     print(log["type"], log.get("event"))
        """
        response = await self._client.request(
            f"/v1/tasks/{task_id}/logs",
            method="GET"
        )
        return response.get("logs", [])

    async def wait_for_completion(
        self,
        task_id: str,
        options: Optional[PollingOptions] = None,
    ) -> Task:
        """轮询等待任务完成

        使用智能轮询策略，支持进度回调和日志实时流式处理。

        Args:
            task_id: 任务 ID
            options: 轮询配置选项

        Returns:
            完成的任务信息

        Raises:
            TaskFailedError: 任务执行失败
            TaskStoppedError: 任务被停止
            TimeoutError: 轮询超时

        Example:
            >>> task = await client.tasks.wait_for_completion(
            ...     "task-123",
            ...     {
            ...         "interval_ms": 2000,
            ...         "timeout_ms": 300000,
            ...         "on_progress": lambda t: print(t["status"]),
            ...         "on_log": lambda log: print(log["type"])
            ...     }
            ... )
        """
        options = options or {}

        # 默认配置
        interval_ms = options.get("interval_ms", 2000)
        timeout_ms = options.get("timeout_ms")
        max_interval_ms = options.get("max_interval_ms", 10000)
        backoff_strategy = options.get("backoff_strategy", BackoffStrategy.EXPONENTIAL)
        backoff_factor = options.get("backoff_factor", 1.5)
        on_progress = options.get("on_progress")
        on_log = options.get("on_log")

        start_time = time.time() * 1000  # 转换为毫秒
        current_interval = interval_ms
        attempt = 0
        last_log_id = 0

        while True:
            # 检查超时
            if timeout_ms:
                elapsed = time.time() * 1000 - start_time
                if elapsed >= timeout_ms:
                    raise TimeoutError(
                        f"Task {task_id} did not complete within {timeout_ms}ms"
                    )

            # 获取任务状态
            task = await self.get(task_id)

            # 进度回调
            if on_progress:
                on_progress(task)

            # 获取新日志
            if on_log:
                all_logs = await self.get_logs(task_id)
                new_logs = [log for log in all_logs if log["id"] > last_log_id]
                for log in new_logs:
                    on_log(log)
                    last_log_id = log["id"]

            # 检查任务状态
            status = task["status"]
            if status == "completed":
                return task
            elif status == "failed":
                raise TaskFailedError(
                    f"Task {task_id} failed",
                    task_id=task_id,
                    task=task
                )
            elif status == "stopped":
                raise TaskStoppedError(
                    f"Task {task_id} was stopped",
                    task_id=task_id,
                    task=task
                )

            # 计算下次轮询间隔（退避算法）
            if backoff_strategy == BackoffStrategy.EXPONENTIAL:
                current_interval = min(
                    max_interval_ms,
                    interval_ms * (backoff_factor ** attempt)
                )
            else:
                current_interval = interval_ms

            # 等待
            await sleep(int(current_interval))
            attempt += 1

    async def create_and_wait(
        self,
        request: CreateTaskRequest,
        polling_options: Optional[PollingOptions] = None,
    ) -> Task:
        """创建任务并等待完成

        便捷方法，组合 create() 和 wait_for_completion()。

        Args:
            request: 创建任务请求
            polling_options: 轮询配置选项

        Returns:
            完成的任务信息

        Example:
            >>> task = await client.tasks.create_and_wait({
            ...     "manifest": "flow-1",
            ...     "inputValues": {"input1": "value"}
            ... })
        """
        response = await self.create(request)
        task_id = response["task"]["id"]
        return await self.wait_for_completion(task_id, polling_options)

    async def run(
        self,
        request: CreateTaskRequest,
        polling_options: Optional[PollingOptions] = None,
    ) -> RunResult:
        """运行任务并获取结果（推荐方法）

        一步完成：创建 → 轮询 → 获取日志 → 提取结果。

        Args:
            request: 创建任务请求
            polling_options: 轮询配置选项

        Returns:
            运行结果，包含任务ID、任务信息、日志和提取的结果

        Example:
            >>> result = await client.tasks.run({
            ...     "manifest": "audio-lab::text-to-audio",
            ...     "inputValues": {"text": "你好"}
            ... })
            >>> print(result["task_id"])
            >>> print(result["result"])
        """
        # 创建任务
        response = await self.create(request)
        task_id = response["task"]["id"]

        # 等待完成
        task = await self.wait_for_completion(task_id, polling_options)

        # 获取日志
        logs = await self.get_logs(task_id)

        # 提取结果
        result = extract_result_from_logs(logs)

        return RunResult(
            task_id=task_id,
            task=task,
            logs=logs,
            result=result
        )

    async def run_with_files(
        self,
        manifest: str,
        input_values: Optional[TaskInputValues] = None,
        files: Optional[Union[Any, List[Any]]] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> RunResult:
        """运行任务（含文件上传）并获取结果

        一步完成文件上传任务：创建（含文件）→ 轮询 → 获取日志 → 提取结果。

        Args:
            manifest: 流程/区块路径
            input_values: 输入值
            files: 文件或文件列表
            polling_options: 轮询配置选项

        Returns:
            运行结果

        Example:
            >>> with open("test.txt", "rb") as f:
            ...     result = await client.tasks.run_with_files(
            ...         "pkg::block",
            ...         {"input1": "value"},
            ...         f
            ...     )
        """
        # 创建任务（含文件）
        response = await self.create_with_files(manifest, input_values, files)
        task_id = response["task"]["id"]

        # 等待完成
        task = await self.wait_for_completion(task_id, polling_options)

        # 获取日志
        logs = await self.get_logs(task_id)

        # 提取结果
        result = extract_result_from_logs(logs)

        return RunResult(
            task_id=task_id,
            task=task,
            logs=logs,
            result=result
        )
