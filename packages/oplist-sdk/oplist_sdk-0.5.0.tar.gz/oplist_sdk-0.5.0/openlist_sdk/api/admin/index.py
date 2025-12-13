"""
管理员索引命名空间
搜索索引管理。
"""
from typing import List, Optional, Dict, Any
from ...core.session import SessionManager
from ...config import Endpoints
from ...api import BaseNamespace

class AdminIndexNamespace(BaseNamespace):
    """搜索索引管理"""
    
    def build(self, paths: List[str] = None, max_depth: int = 0) -> Dict[str, Any]:
        """
        构建全文搜索索引。
        """
        payload = {}
        if paths:
            payload["paths"] = paths
        if max_depth > 0:
            payload["max_depth"] = max_depth
            
        return self._session.request("POST", Endpoints.ADMIN_INDEX_BUILD, json=payload)

    def update(self, paths: List[str]) -> Dict[str, Any]:
        """
        更新特定路径的搜索索引。
        """
        return self._session.request("POST", Endpoints.ADMIN_INDEX_UPDATE, json={"paths": paths})

    def stop(self) -> Dict[str, Any]:
        """停止当前索引操作。"""
        return self._session.request("POST", Endpoints.ADMIN_INDEX_STOP)

    def clear(self) -> Dict[str, Any]:
        """清除所有搜索索引数据。"""
        return self._session.request("POST", Endpoints.ADMIN_INDEX_CLEAR)

    def progress(self) -> Dict[str, Any]:
        """
        获取当前索引操作进度。
        """
        return self._session.request("GET", Endpoints.ADMIN_INDEX_PROGRESS)
