"""
管理员元数据命名空间
路径元数据配置。
"""
from typing import List, Optional, Dict, Any
from ...core.session import SessionManager
from ...config import Endpoints
from ...api import BaseNamespace

class AdminMetaNamespace(BaseNamespace):
    """元数据配置管理"""
    
    def list(self, page: int = 1, per_page: int = 0) -> Dict[str, Any]:
        """
        列出所有元数据配置。
        """
        params = {"page": page, "per_page": per_page}
        return self._session.request("GET", Endpoints.ADMIN_META_LIST, params=params)

    def get(self, meta_id: int) -> Dict[str, Any]:
        """
        根据 ID 获取元数据配置。
        """
        return self._session.request("GET", Endpoints.ADMIN_META_GET, params={"id": meta_id})

    def create(self, path: str, 
               password: str = "",
               hide: str = "",
               readme: str = "",
               header: str = "",
               upload: bool = False) -> Dict[str, Any]:
        """
        创建新的元数据配置。
        """
        payload = {
            "path": path,
            "password": password,
            "hide": hide,
            "readme": readme,
            "header": header,
            "upload": upload
        }
        return self._session.request("POST", Endpoints.ADMIN_META_CREATE, json=payload)

    def update(self, meta_id: int, **kwargs) -> Dict[str, Any]:
        """
        更新元数据配置。
        """
        payload = {"id": meta_id, **kwargs}
        return self._session.request("PUT", Endpoints.ADMIN_META_UPDATE, json=payload)

    def delete(self, meta_id: int) -> Dict[str, Any]:
        """
        删除元数据配置。
        """
        return self._session.request("DELETE", Endpoints.ADMIN_META_DELETE, params={"id": meta_id})
