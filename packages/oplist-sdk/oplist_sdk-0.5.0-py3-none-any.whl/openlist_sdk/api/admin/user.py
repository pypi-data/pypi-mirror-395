"""
管理员用户命名空间
管理员用户管理操作。
"""
from typing import List, Optional, Dict, Any
from ...core.session import SessionManager
from ...config import Endpoints
from ...api import BaseNamespace

class AdminUserNamespace(BaseNamespace):
    """管理员用户管理操作"""
    
    def list(self, page: int = 1, per_page: int = 0) -> Dict[str, Any]:
        """
        列出所有用户。
        """
        params = {"page": page, "per_page": per_page}
        return self._session.request("GET", Endpoints.ADMIN_USER_LIST, params=params)

    def get(self, user_id: int) -> Dict[str, Any]:
        """
        根据 ID 获取用户。
        """
        return self._session.request("GET", Endpoints.ADMIN_USER_GET, params={"id": user_id})

    def create(self, username: str, password: str, 
               base_path: str = "/", role: int = 1, 
               permission: int = 0, disabled: bool = False) -> Dict[str, Any]:
        """
        创建新用户。
        """
        payload = {
            "username": username,
            "password": password,
            "base_path": base_path,
            "role": role,
            "permission": permission,
            "disabled": disabled
        }
        return self._session.request("POST", Endpoints.ADMIN_USER_CREATE, json=payload)

    def update(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """
        更新用户信息。
        """
        payload = {"id": user_id, **kwargs}
        return self._session.request("PUT", Endpoints.ADMIN_USER_UPDATE, json=payload)

    def delete(self, user_id: int) -> Dict[str, Any]:
        """
        删除用户。
        """
        return self._session.request("DELETE", Endpoints.ADMIN_USER_DELETE, params={"id": user_id})

    def cancel_2fa(self, user_id: int) -> Dict[str, Any]:
        """
        取消/禁用用户的 2FA。
        """
        return self._session.request("POST", Endpoints.ADMIN_USER_CANCEL_2FA, json={"id": user_id})

    def clear_cache(self, user_id: int) -> Dict[str, Any]:
        """
        清除用户的缓存数据。
        """
        return self._session.request("POST", Endpoints.ADMIN_USER_DEL_CACHE, json={"id": user_id})
