"""
公共命名空间
无需认证的公共 API。
"""
from typing import List, Union, Dict, Any
from . import BaseNamespace
from ..config import Endpoints


class PublicNamespace(BaseNamespace):
    """公共 API - 无需认证"""
    
    def settings(self) -> Dict[str, Any]:
        """
        获取公共系统设置。
        """
        return self._session.request("GET", Endpoints.PUBLIC_SETTINGS)

    def offline_download_tools(self) -> Dict[str, Any]:
        """
        获取可用的离线下载工具。
        返回列表，统一格式化为字典: `{"name": "...", "enabled": ...}`
        """
        resp = self._session.request("GET", Endpoints.PUBLIC_OFFLINE_DOWNLOAD_TOOLS)
        if resp["code"] == 200 and isinstance(resp.get("data"), list):
            result = []
            for item in resp["data"]:
                # API 可能返回字符串列表或对象列表
                if isinstance(item, str):
                    result.append({"name": item, "enabled": True})
                elif isinstance(item, dict):
                    result.append(item)
            resp["data"] = result
        elif resp["code"] == 200:
            resp["data"] = []
        return resp

    def archive_extensions(self) -> Dict[str, Any]:
        """
        获取支持的压缩包文件扩展名。
        """
        resp = self._session.request("GET", Endpoints.PUBLIC_ARCHIVE_EXTENSIONS)
        if resp["code"] == 200 and not isinstance(resp.get("data"), list):
             resp["data"] = []
        return resp
