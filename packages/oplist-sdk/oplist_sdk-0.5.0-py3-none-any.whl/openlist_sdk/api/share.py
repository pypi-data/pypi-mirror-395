"""
分享命名空间
文件和文件夹分享管理。
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from . import BaseNamespace
from ..config import Endpoints


class ShareNamespace(BaseNamespace):
    """文件/文件夹分享操作"""
    
    def list(self, page: int = 1, per_page: int = 0) -> Dict[str, Any]:
        """
        列出当前用户创建的所有分享。
        """
        params = {"page": page, "per_page": per_page}
        return self._session.request("GET", Endpoints.SHARE_LIST, params=params)

    def get(self, share_id: str) -> Dict[str, Any]:
        """
        根据 ID 获取分享详情。
        """
        return self._session.request("GET", Endpoints.SHARE_GET, params={"id": share_id})

    def create(self, path: str, password: str = "", 
               expire_days: int = 0, remark: str = "") -> Dict[str, Any]:
        """
        创建新的文件/文件夹分享。
        """
        payload = {
            "path": path,
            "password": password,
            "remark": remark
        }
        
        if expire_days > 0:
            expire_time = datetime.now().timestamp() + (expire_days * 86400)
            payload["expire"] = int(expire_time)
        
        return self._session.request("POST", Endpoints.SHARE_CREATE, json=payload)

    def update(self, share_id: str, password: str = None, 
               expire_days: int = None, remark: str = None) -> Dict[str, Any]:
        """
        更新现有分享。
        """
        payload = {"id": share_id}
        
        if password is not None:
            payload["password"] = password
        if expire_days is not None:
            if expire_days > 0:
                expire_time = datetime.now().timestamp() + (expire_days * 86400)
                payload["expire"] = int(expire_time)
            else:
                payload["expire"] = 0
        if remark is not None:
            payload["remark"] = remark
        
        return self._session.request("PUT", Endpoints.SHARE_UPDATE, json=payload)

    def delete(self, share_id: str) -> Dict[str, Any]:
        """
        删除分享。
        """
        return self._session.request("DELETE", Endpoints.SHARE_DELETE, params={"id": share_id})

    def enable(self, share_id: str) -> Dict[str, Any]:
        """
        重新启用已禁用的分享。
        """
        return self._session.request("POST", Endpoints.SHARE_ENABLE, json={"id": share_id})

    def disable(self, share_id: str) -> Dict[str, Any]:
        """
        临时禁用分享。
        """
        return self._session.request("POST", Endpoints.SHARE_DISABLE, json={"id": share_id})

    def create_quick(self, path: str, password: str = "") -> Dict[str, Any]:
        """
        快速创建分享 - 仅返回分享链接。
        """
        resp = self.create(path, password=password)
        if resp["code"] == 200 and isinstance(resp.get("data"), dict):
            share = resp["data"]
            # 原始字典操作
            resp["data"] = share.get("short_link") or share.get("id")
        return resp
