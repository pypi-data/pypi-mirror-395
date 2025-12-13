"""
OpenList Python SDK 主客户端
提供类型安全、开发者友好的 API 接口。

使用方法:
    from openlist_sdk import OpenListClient
    
    # 快捷模式 - 自动登录
    client = OpenListClient("http://nas:5244", username="admin", password="pwd")
    resp = client.fs.list("/")
    if resp["code"] == 200:
        files = resp["data"]["content"]
    
    # 上下文管理器模式
    with OpenListClient("http://nas:5244") as client:
        client.login("admin", "pwd")
        client.fs.mkdir("/local/new_folder")
"""
from typing import Optional, Dict, Any
from .core.session import SessionManager
from .api.auth import AuthNamespace
from .api.fs import FileSystemNamespace
from .api.share import ShareNamespace
from .api.public import PublicNamespace
from .api.admin import AdminNamespace
from .api.task import TaskNamespace
from .api.storage import StorageNamespace


class OpenListClient:
    """
    SDK 主入口类。
    
    命名空间:
        - auth: 认证和用户会话
        - fs: 文件系统操作
        - share: 文件分享管理
        - storage: 存储挂载管理 (原 admin.storage)
        - public: 公共 API (无需认证)
        - task: 任务管理 (复制/移动/上传/解压/离线下载)
        - admin: 管理员操作
            - admin.user: 用户管理
            - admin.driver: 驱动信息
            - admin.setting: 系统设置
            - admin.meta: 元数据配置
            - admin.index: 搜索索引管理
    
    示例:
        # 基础用法
        client = OpenListClient("http://nas:5244", "admin", "password")
        resp = client.fs.list("/")
        if resp["code"] == 200:
            print(resp["data"]["content"])
        else:
            print(resp["message"])
    """
    
    def __init__(self, host: str, username: str = "", password: str = "", 
                 otp_code: str = "", token: str = "", timeout: float = 30.0,
                 verify_token: bool = False):
        """
        初始化 OpenList 客户端。
        
        :param host: OpenList 服务器地址 (如 http://127.0.0.1:5244)
        :param username: (可选) 自动登录用户名
        :param password: (可选) 自动登录密码
        :param otp_code: (可选) 2FA 验证码
        :param token: (可选) 已有的认证令牌
        :param timeout: 请求超时时间(秒)，默认 30
        :param verify_token: 是否在初始化时验证 Token 有效性 (默认 False)
        """
        self._session = SessionManager(host, token, timeout)
        
        # 初始化命名空间
        self.auth = AuthNamespace(self._session)
        self.fs = FileSystemNamespace(self._session)
        self.share = ShareNamespace(self._session)
        self.storage = StorageNamespace(self._session)
        self.public = PublicNamespace(self._session)
        self.task = TaskNamespace(self._session)
        self.admin = AdminNamespace(self._session)
        
        # 如果提供了凭据则自动登录
        if username and password and not token:
            self.login(username, password, otp_code)
            
        # 验证 Token (如果启用)
        if verify_token and self.token:
            resp = self.auth.get_me()
            if resp["code"] != 200:
                raise Exception(f"Token verification failed: code={resp.get('code')}, msg={resp.get('message')}")

    @property
    def host(self) -> str:
        """获取服务器地址。"""
        return self._session.host

    @property
    def token(self) -> str:
        """获取当前认证令牌。"""
        return self._session.token

    def login(self, username: str, password: str, otp_code: str = "") -> Dict[str, Any]:
        """
        登录快捷方法。
        
        :param username: 用户名
        :param password: 密码
        :param otp_code: 可选的 2FA 验证码
        :return: 响应字典 (含 token)
        """
        return self.auth.login(username, password, otp_code)

    def logout(self) -> Dict[str, Any]:
        """登出并清除会话。"""
        return self.auth.logout()

    def close(self):
        """关闭底层 HTTP 会话。"""
        try:
            self._session.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        """析构函数，确保资源被释放。"""
        self.close()

    def __repr__(self) -> str:
        return f"<OpenListClient host={self.host} authenticated={bool(self.token)}>"
