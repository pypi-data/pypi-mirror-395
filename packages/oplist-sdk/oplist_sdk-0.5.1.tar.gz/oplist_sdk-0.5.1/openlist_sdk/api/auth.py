"""
认证命名空间
处理用户登录、登出、2FA 和会话管理。
"""
from typing import Dict, Optional, Any
from . import BaseNamespace
from ..config import Endpoints


class AuthNamespace(BaseNamespace):
    """认证和用户会话管理"""
    
    def login(self, username: str, password: str, otp_code: str = "") -> Dict[str, Any]:
        """
        使用用户名和密码登录。
        """
        payload = {"username": username, "password": password}
        if otp_code:
            payload["otp_code"] = otp_code
            
        resp = self._session.request("POST", Endpoints.AUTH_LOGIN, json=payload)
        
        if resp["code"] == 200 and isinstance(resp.get("data"), dict):
            token = resp["data"].get("token")
            if token:
                self._session.set_token(token)
        return resp

    def login_hash(self, username: str, password_hash: str, otp_code: str = "") -> Dict[str, Any]:
        """
        使用预哈希密码 (SHA256) 登录。
        """
        payload = {"username": username, "password": password_hash}
        if otp_code:
            payload["otp_code"] = otp_code
            
        resp = self._session.request("POST", Endpoints.AUTH_LOGIN_HASH, json=payload)
        
        if resp["code"] == 200 and isinstance(resp.get("data"), dict):
            token = resp["data"].get("token")
            if token:
                self._session.set_token(token)
        return resp

    def logout(self) -> Dict[str, Any]:
        """
        登出并使当前会话令牌失效。
        """
        resp = self._session.request("POST", Endpoints.AUTH_LOGOUT)
        if resp["code"] == 200:
            self._session.set_token("")
        return resp

    def get_me(self) -> Dict[str, Any]:
        """
        获取当前已认证用户的信息。
        """
        return self._session.request("GET", Endpoints.AUTH_ME)

    def update_me(self, password: str = None, **kwargs) -> Dict[str, Any]:
        """
        更新当前用户的密码或其他设置。
        """
        payload = {}
        if password:
            payload["password"] = password
        payload.update(kwargs)
        
        return self._session.request("PUT", Endpoints.AUTH_ME_UPDATE, json=payload)

    def generate_2fa(self) -> Dict[str, Any]:
        """
        生成新的 2FA 密钥。
        """
        return self._session.request("POST", Endpoints.AUTH_2FA_GENERATE)

    def verify_2fa(self, code: str, secret: str = None) -> Dict[str, Any]:
        """
        验证 TOTP 验证码。
        """
        payload = {"code": code}
        if secret:
            payload["secret"] = secret
        return self._session.request("POST", Endpoints.AUTH_2FA_VERIFY, json=payload)

    def list_ssh_keys(self) -> Dict[str, Any]:
        """
        列出当前用户的 SSH 公钥。
        """
        return self._session.request("GET", Endpoints.USER_SSH_KEYS)

    def add_ssh_key(self, title: str, key: str) -> Dict[str, Any]:
        """
        添加 SSH 公钥。
        """
        payload = {"title": title, "key": key}
        return self._session.request("POST", Endpoints.USER_SSH_KEYS, json=payload)

    def delete_ssh_key(self, key_id: int) -> Dict[str, Any]:
        """
        删除 SSH 公钥。
        """
        return self._session.request("DELETE", Endpoints.USER_SSH_KEYS, params={"id": key_id})
