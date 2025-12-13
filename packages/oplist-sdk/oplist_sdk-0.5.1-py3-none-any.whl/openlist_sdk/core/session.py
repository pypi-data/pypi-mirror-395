"""
OpenList SDK 会话管理器
处理 HTTP 通信、认证和错误处理。
"""
import httpx
from typing import Any, Dict, Optional, Union, BinaryIO

from ..config import Endpoints


class SessionManager:
    """
    管理 HTTP 会话、认证和全局错误处理。
    
    特性:
    - 通过 httpx 支持 HTTP/2
    - 自动注入认证令牌
    - 业务错误检测 (HTTP 200 但 code != 200)
    - 统一的异常处理
    """
    
    def __init__(self, host: str, token: str = "", timeout: float = 30.0):
        """
        初始化会话管理器。
        
        :param host: OpenList 服务器地址
        :param token: 可选的已有认证令牌
        :param timeout: 请求超时时间(秒)
        """
        self.host = host.rstrip("/")
        self.token = token
        self.timeout = timeout
        # 注意: HTTP/2 需要安装 'pip install httpx[http2]' (h2 包)
        # 为了更好的兼容性，默认使用 HTTP/1.1
        self._client = httpx.Client(
            timeout=timeout, 
            http2=False,  # 如果安装了 h2，可设为 True
            verify=True,
            follow_redirects=True
        )

    def close(self):
        """关闭 HTTP 客户端。"""
        if self._client:
            self._client.close()

    def set_token(self, token: str):
        """更新认证令牌。"""
        self.token = token

    def request(self, method: str, endpoint: Union[str, Endpoints], **kwargs) -> Dict[str, Any]:
        """
        执行 HTTP 请求，返回统一的字典响应。
        结构: {"code": int, "message": str, "data": Any}
        """
        # 解析 URL
        path = endpoint.value if hasattr(endpoint, 'value') else str(endpoint)
        url = f"{self.host}{path}"

        # 构建请求头
        req_headers = {
            "User-Agent": "OpenList-SDK-Python/0.3.0",
        }
        custom_headers = kwargs.pop("headers", {})
        req_headers.update(custom_headers)
        
        if "json" in kwargs and "Content-Type" not in req_headers:
            req_headers["Content-Type"] = "application/json"
        
        if self.token:
            req_headers["Authorization"] = self.token
        
        try:
            response = self._client.request(method, url, headers=req_headers, **kwargs)
            
            # 尝试解析 JSON
            try:
                res_json = response.json()
            except ValueError:
                # 非 JSON
                status = response.status_code
                code = 200 if 200 <= status < 300 else status
                return {"code": code, "message": "OK" if code==200 else f"HTTP {status}", "data": response.content}

            # 标准 API 响应
            if isinstance(res_json, dict) and "code" in res_json:
                return {
                    "code": res_json.get("code"),
                    "message": res_json.get("message", "Success"),
                    "data": res_json.get("data")
                }
            
            # 非标准 JSON
            status = response.status_code
            code = 200 if 200 <= status < 300 else status
            return {"code": code, "message": "Success" if code==200 else "Error", "data": res_json}

        except Exception as e:
            # 捕获所有错误
            return {"code": -1, "message": str(e), "data": None}
