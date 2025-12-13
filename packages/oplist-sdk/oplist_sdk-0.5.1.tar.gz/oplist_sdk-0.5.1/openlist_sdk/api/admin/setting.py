"""
管理员设置命名空间
系统设置管理。
"""
from typing import List, Any, Dict
from ...core.session import SessionManager
from ...config import Endpoints
from ...api import BaseNamespace

class AdminSettingNamespace(BaseNamespace):
    """系统设置管理"""
    
    def list(self, group: int = None) -> Dict[str, Any]:
        """
        列出所有系统设置。
        """
        params = {}
        if group is not None:
            params["group"] = group
            
        return self._session.request("GET", Endpoints.ADMIN_SETTING_LIST, params=params)

    def get(self, key: str) -> Dict[str, Any]:
        """
        获取特定设置的值。
        """
        return self._session.request("GET", Endpoints.ADMIN_SETTING_GET, params={"key": key})

    def save(self, settings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        保存一个或多个设置。
        """
        return self._session.request("POST", Endpoints.ADMIN_SETTING_SAVE, json=settings)

    def set(self, key: str, value: Any) -> Dict[str, Any]:
        """
        设置单个值。便捷方法。
        """
        return self.save([{"key": key, "value": value}])

    def delete(self, key: str) -> Dict[str, Any]:
        """
        删除自定义设置。
        """
        return self._session.request("DELETE", Endpoints.ADMIN_SETTING_DELETE, params={"key": key})

    def reset_token(self) -> Dict[str, Any]:
        """
        生成新的 API 令牌。
        """
        resp = self._session.request("POST", Endpoints.ADMIN_SETTING_RESET_TOKEN)
        # 保持原始字典返回
        return resp
