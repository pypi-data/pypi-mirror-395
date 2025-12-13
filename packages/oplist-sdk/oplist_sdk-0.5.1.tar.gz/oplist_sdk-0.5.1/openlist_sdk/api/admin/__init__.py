"""
管理员命名空间
聚合所有管理员子命名空间。
"""
from ...core.session import SessionManager
from .. import BaseNamespace
from .user import AdminUserNamespace
from .driver import AdminDriverNamespace
from .setting import AdminSettingNamespace
from .meta import AdminMetaNamespace
from .index import AdminIndexNamespace


class AdminNamespace(BaseNamespace):
    """
    管理员命名空间聚合器。
    
    使用方法:
        client.admin.user.create(...)
        client.admin.driver.names()
        client.admin.setting.save([...])
        client.admin.meta.create(...)
        client.admin.index.build()
    """
    
    def __init__(self, session: SessionManager):
        super().__init__(session)
        
        # 子命名空间
        self.user = AdminUserNamespace(session)
        self.driver = AdminDriverNamespace(session)
        self.setting = AdminSettingNamespace(session)
        self.meta = AdminMetaNamespace(session)
        self.index = AdminIndexNamespace(session)
