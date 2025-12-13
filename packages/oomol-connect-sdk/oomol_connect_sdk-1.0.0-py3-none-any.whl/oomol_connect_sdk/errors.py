"""自定义错误类"""

from typing import Any, Optional


class OomolConnectError(Exception):
    """所有 Oomol Connect SDK 错误的基类"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ApiError(OomolConnectError):
    """HTTP API 错误"""

    def __init__(self, message: str, status: int, response: Any = None) -> None:
        super().__init__(message)
        self.status = status
        self.response = response

    def __str__(self) -> str:
        return f"ApiError({self.status}): {self.message}"


class TaskFailedError(OomolConnectError):
    """任务执行失败错误"""

    def __init__(self, message: str, task_id: str, task: Optional[Any] = None) -> None:
        super().__init__(message)
        self.task_id = task_id
        self.task = task

    def __str__(self) -> str:
        return f"TaskFailedError: Task {self.task_id} failed - {self.message}"


class TaskStoppedError(OomolConnectError):
    """任务被停止错误"""

    def __init__(self, message: str, task_id: str, task: Optional[Any] = None) -> None:
        super().__init__(message)
        self.task_id = task_id
        self.task = task

    def __str__(self) -> str:
        return f"TaskStoppedError: Task {self.task_id} was stopped - {self.message}"


class TimeoutError(OomolConnectError):
    """轮询超时错误"""

    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"TimeoutError: {self.message}"


class InstallFailedError(OomolConnectError):
    """包安装失败错误"""

    def __init__(self, message: str, task_id: str, task: Optional[Any] = None) -> None:
        super().__init__(message)
        self.task_id = task_id
        self.task = task

    def __str__(self) -> str:
        return f"InstallFailedError: Install task {self.task_id} failed - {self.message}"
