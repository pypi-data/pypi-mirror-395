"""Flows 客户端"""

from typing import TYPE_CHECKING

from .types import ListFlowsResponse

if TYPE_CHECKING:
    from .client import OomolConnectClient


class FlowsClient:
    """Flows API 客户端

    用于列出系统中可用的流程。
    """

    def __init__(self, client: "OomolConnectClient") -> None:
        """初始化 Flows 客户端

        Args:
            client: 主客户端实例
        """
        self._client = client

    async def list(self) -> ListFlowsResponse:
        """列出所有可用的流程

        Returns:
            包含流程列表的响应

        Example:
            >>> flows_response = await client.flows.list()
            >>> for flow in flows_response["flows"]:
            ...     print(flow["name"], flow["path"])
        """
        return await self._client.request("/v1/flows", method="GET")
