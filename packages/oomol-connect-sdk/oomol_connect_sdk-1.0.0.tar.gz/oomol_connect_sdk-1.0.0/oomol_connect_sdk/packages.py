"""Packages 客户端"""

import time
from typing import TYPE_CHECKING, Optional

from .errors import InstallFailedError, TimeoutError
from .types import (
    BackoffStrategy,
    InstallTask,
    ListInstallTasksResponse,
    ListPackagesResponse,
    PollingOptions,
)
from .utils import sleep

if TYPE_CHECKING:
    from .client import OomolConnectClient


class PackagesClient:
    """Packages API 客户端

    用于管理包的安装和查询。
    """

    def __init__(self, client: "OomolConnectClient") -> None:
        """初始化 Packages 客户端

        Args:
            client: 主客户端实例
        """
        self._client = client

    async def list(self) -> ListPackagesResponse:
        """列出已安装的包

        Returns:
            包含包列表的响应

        Example:
            >>> packages_response = await client.packages.list()
            >>> for pkg in packages_response["packages"]:
            ...     print(pkg["name"], pkg["version"])
        """
        return await self._client.request("/packages", method="GET")

    async def install(
        self,
        name: str,
        version: Optional[str] = None,
    ) -> InstallTask:
        """安装包

        Args:
            name: 包名
            version: 版本（可选）

        Returns:
            安装任务信息

        Example:
            >>> install_task = await client.packages.install("audio-lab", "1.0.0")
            >>> print(install_task["id"], install_task["status"])
        """
        data = {"name": name}
        if version:
            data["version"] = version

        return await self._client.request(
            "/packages/install",
            method="POST",
            json_data=data
        )

    async def list_install_tasks(self) -> ListInstallTasksResponse:
        """列出安装任务

        Returns:
            包含安装任务列表的响应

        Example:
            >>> tasks_response = await client.packages.list_install_tasks()
            >>> for task in tasks_response["tasks"]:
            ...     print(task["name"], task["status"])
        """
        return await self._client.request("/packages/install", method="GET")

    async def get_install_task(self, task_id: str) -> InstallTask:
        """获取安装任务详情

        Args:
            task_id: 安装任务 ID

        Returns:
            安装任务详情

        Example:
            >>> task = await client.packages.get_install_task("task-123")
            >>> print(task["status"])
        """
        return await self._client.request(
            f"/packages/install/{task_id}",
            method="GET"
        )

    async def wait_for_install_completion(
        self,
        task_id: str,
        options: Optional[PollingOptions] = None,
    ) -> InstallTask:
        """轮询等待安装完成

        Args:
            task_id: 安装任务 ID
            options: 轮询配置选项

        Returns:
            完成的安装任务信息

        Raises:
            InstallFailedError: 安装失败
            TimeoutError: 轮询超时

        Example:
            >>> task = await client.packages.wait_for_install_completion(
            ...     "task-123",
            ...     {"interval_ms": 1000, "timeout_ms": 60000}
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

        start_time = time.time() * 1000  # 转换为毫秒
        current_interval = interval_ms
        attempt = 0

        while True:
            # 检查超时
            if timeout_ms:
                elapsed = time.time() * 1000 - start_time
                if elapsed >= timeout_ms:
                    raise TimeoutError(
                        f"Install task {task_id} did not complete within {timeout_ms}ms"
                    )

            # 获取安装任务状态
            task = await self.get_install_task(task_id)

            # 进度回调
            if on_progress:
                on_progress(task)  # type: ignore

            # 检查状态
            status = task["status"]
            if status == "success":
                return task
            elif status == "failed":
                error = task.get("error", "Unknown error")
                raise InstallFailedError(
                    f"Install task {task_id} failed: {error}",
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

    async def install_and_wait(
        self,
        name: str,
        version: Optional[str] = None,
        polling_options: Optional[PollingOptions] = None,
    ) -> InstallTask:
        """安装包并等待完成

        便捷方法，组合 install() 和 wait_for_install_completion()。

        Args:
            name: 包名
            version: 版本（可选）
            polling_options: 轮询配置选项

        Returns:
            完成的安装任务信息

        Example:
            >>> task = await client.packages.install_and_wait("audio-lab", "1.0.0")
            >>> print(task["packagePath"])
        """
        install_task = await self.install(name, version)
        task_id = install_task["id"]
        return await self.wait_for_install_completion(task_id, polling_options)
