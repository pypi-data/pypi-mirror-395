"""
存储管理命名空间
存储挂载管理操作。
"""
import json
from typing import List, Dict, Any, Optional
from ..core.session import SessionManager
from ..config import Endpoints
from . import BaseNamespace

class StorageNamespace(BaseNamespace):
    """存储管理操作"""
    
    def list(self, page: int = 1, per_page: int = 0) -> Dict[str, Any]:
        """
        列出所有已挂载的存储。
        """
        params = {"page": page, "per_page": per_page}
        return self._session.request("GET", Endpoints.ADMIN_STORAGE_LIST, params=params)

    def get(self, storage_id: int) -> Dict[str, Any]:
        """
        根据 ID 获取存储。
        """
        return self._session.request("GET", Endpoints.ADMIN_STORAGE_GET, params={"id": storage_id})

    def create(self, mount_path: str, driver: str, 
               cache_expiration: int = 30, 
               order: int = 0,
               remark: str = "",
               **driver_config) -> Dict[str, Any]:
        """
        挂载新存储。
        """
        payload = {
            "mount_path": mount_path,
            "driver": driver,
            "cache_expiration": cache_expiration,
            "order": order,
            "remark": remark,
            "addition": json.dumps(driver_config) if driver_config else "{}"
        }
        return self._session.request("POST", Endpoints.ADMIN_STORAGE_CREATE, json=payload)

    def update(self, storage_id: int, **kwargs) -> Dict[str, Any]:
        """
        更新存储配置。
        """
        # 处理 driver_config -> addition 转换
        if "driver_config" in kwargs:
            kwargs["addition"] = json.dumps(kwargs.pop("driver_config"))
            
        payload = {"id": storage_id, **kwargs}
        return self._session.request("PUT", Endpoints.ADMIN_STORAGE_UPDATE, json=payload)

    def delete(self, storage_id: int) -> Dict[str, Any]:
        """
        删除/卸载存储。
        """
        return self._session.request("DELETE", Endpoints.ADMIN_STORAGE_DELETE, params={"id": storage_id})

    def enable(self, storage_id: int) -> Dict[str, Any]:
        """
        启用已禁用的存储。
        """
        return self._session.request("POST", Endpoints.ADMIN_STORAGE_ENABLE, json={"id": storage_id})

    def disable(self, storage_id: int) -> Dict[str, Any]:
        """
        临时禁用存储。
        """
        return self._session.request("POST", Endpoints.ADMIN_STORAGE_DISABLE, json={"id": storage_id})

    def reload(self) -> Dict[str, Any]:
        """强制重新加载所有存储。"""
        return self._session.request("POST", Endpoints.ADMIN_STORAGE_RELOAD)
