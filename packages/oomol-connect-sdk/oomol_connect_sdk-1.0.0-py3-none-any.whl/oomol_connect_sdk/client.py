"""主客户端"""

import json
from typing import Any, Dict, Optional

import httpx

from .errors import ApiError
from .types import ClientOptions
from .utils import build_url


class OomolConnectClient:
    """Oomol Connect 主客户端

    这是 SDK 的主入口，提供对所有子客户端的访问。

    示例:
        >>> client = OomolConnectClient(
        ...     base_url="https://api.example.com/api",
        ...     api_token="your-token"
        ... )
        >>> flows = await client.flows.list()
    """

    def __init__(self, options: Optional[ClientOptions] = None) -> None:
        """初始化客户端

        Args:
            options: 客户端配置选项
        """
        options = options or {}

        self._base_url = options.get("base_url", "/api")
        self._timeout = options.get("timeout", 30.0)
        self._default_headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        # 添加自定义 headers
        if options.get("default_headers"):
            self._default_headers.update(options["default_headers"])

        # 处理 API Token
        api_token = options.get("api_token")
        if api_token:
            self._default_headers["Authorization"] = f"Bearer {api_token}"

        # 创建 HTTP 客户端
        self._http_client = httpx.AsyncClient(
            timeout=self._timeout,
            headers=self._default_headers
        )

        # 延迟导入避免循环依赖
        from .blocks import BlocksClient
        from .flows import FlowsClient
        from .packages import PackagesClient
        from .tasks import TasksClient

        # 初始化子客户端
        self.flows = FlowsClient(self)
        self.blocks = BlocksClient(self)
        self.tasks = TasksClient(self)
        self.packages = PackagesClient(self)

    async def request(
        self,
        path: str,
        method: str = "GET",
        json_data: Optional[Any] = None,
        data: Optional[Any] = None,
        files: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """发送 HTTP 请求

        Args:
            path: 请求路径
            method: HTTP 方法
            json_data: JSON 数据
            data: 表单数据
            files: 文件数据
            headers: 额外的请求头

        Returns:
            响应数据（自动解析 JSON）

        Raises:
            ApiError: API 请求失败时抛出
        """
        url = build_url(self._base_url, path)

        # 合并请求头
        request_headers = dict(self._default_headers)
        if headers:
            request_headers.update(headers)

        # 如果有文件上传，移除 Content-Type（让 httpx 自动设置）
        if files:
            request_headers.pop("Content-Type", None)

        try:
            response = await self._http_client.request(
                method=method,
                url=url,
                json=json_data,
                data=data,
                files=files,
                headers=request_headers,
            )

            # 检查状态码
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_message = error_data.get("message", response.text)
                except Exception:
                    error_message = response.text

                raise ApiError(
                    message=error_message,
                    status=response.status_code,
                    response=response.text
                )

            # 尝试解析 JSON
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            else:
                return response.text

        except httpx.HTTPError as e:
            raise ApiError(
                message=str(e),
                status=0,
                response=None
            )

    def get_base_url(self) -> str:
        """获取基础 URL"""
        return self._base_url

    def get_default_headers(self) -> Dict[str, str]:
        """获取默认请求头"""
        return dict(self._default_headers)

    async def close(self) -> None:
        """关闭客户端，释放资源"""
        await self._http_client.aclose()

    async def __aenter__(self) -> "OomolConnectClient":
        """支持异步上下文管理器"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """支持异步上下文管理器"""
        await self.close()
