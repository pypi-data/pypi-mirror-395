"""
管理员驱动命名空间
存储驱动信息和配置。
"""
from typing import List, Dict, Any
from ...core.session import SessionManager
from ...config import Endpoints
from ...api import BaseNamespace

class AdminDriverNamespace(BaseNamespace):
    """存储驱动信息"""
    
    def list(self) -> Dict[str, Any]:
        """
        列出所有可用的存储驱动及其配置。
        """
        resp = self._session.request("GET", Endpoints.ADMIN_DRIVER_LIST)
        if resp["code"] != 200:
            resp["data"] = []
        return resp

    def names(self) -> Dict[str, Any]:
        """
        获取可用驱动名称列表。
        """
        resp = self._session.request("GET", Endpoints.ADMIN_DRIVER_NAMES)
        if resp["code"] != 200:
             resp["data"] = []
        return resp

    def info(self, driver_name: str) -> Dict[str, Any]:
        """
        获取特定驱动的配置模式。
        """
        return self._session.request("GET", Endpoints.ADMIN_DRIVER_INFO, 
                                     params={"driver": driver_name})
