"""Blocks 客户端"""

from typing import TYPE_CHECKING

from .types import ListBlocksResponse

if TYPE_CHECKING:
    from .client import OomolConnectClient


class BlocksClient:
    """Blocks API 客户端

    用于列出系统中可用的区块（原始计算单元）。
    """

    def __init__(self, client: "OomolConnectClient") -> None:
        """初始化 Blocks 客户端

        Args:
            client: 主客户端实例
        """
        self._client = client

    async def list(self) -> ListBlocksResponse:
        """列出所有可用的区块

        Returns:
            包含区块列表的响应

        Example:
            >>> blocks_response = await client.blocks.list()
            >>> for block in blocks_response["blocks"]:
            ...     print(block["package"], block["name"])
        """
        return await self._client.request("/v1/blocks", method="GET")
