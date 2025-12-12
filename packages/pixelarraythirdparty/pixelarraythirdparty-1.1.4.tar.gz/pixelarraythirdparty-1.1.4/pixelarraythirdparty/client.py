import aiohttp
from typing import Dict, Any, Tuple


class AsyncClient:
    def __init__(self, api_key: str):
        self.base_url = "https://thirdparty.pixelarrayai.com"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

    async def _request(
        self, method: str, url: str, **kwargs
    ) -> Tuple[Dict[str, Any], bool]:
        # 如果kwargs中有headers，则合并headers
        headers = self.headers.copy()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
            kwargs = {k: v for k, v in kwargs.items() if k != "headers"}

        async with aiohttp.ClientSession() as session:
            req_method = getattr(session, method.lower())
            async with req_method(
                f"{self.base_url}{url}", headers=headers, **kwargs
            ) as resp:
                if resp.status == 200:
                    try:
                        result = await resp.json()
                        if result.get("success") is True:
                            return result.get("data", {}), True
                    except:
                        # 如果不是JSON响应，返回空
                        pass
                return {}, False

    async def _request_raw(
        self, method: str, url: str, **kwargs
    ) -> Tuple[int, Dict[str, Any]]:
        headers = self.headers.copy()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
            kwargs = {k: v for k, v in kwargs.items() if k != "headers"}

        async with aiohttp.ClientSession() as session:
            req_method = getattr(session, method.lower())
            async with req_method(
                f"{self.base_url}{url}", headers=headers, **kwargs
            ) as resp:
                try:
                    data = await resp.json()
                except:
                    data = {}
                return resp.status, data
