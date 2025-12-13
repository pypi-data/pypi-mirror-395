"""
OpenList SDK API 命名空间包
"""
from ..core.session import SessionManager


class BaseNamespace:
    """所有 API 命名空间的基类"""
    
    def __init__(self, session: SessionManager):
        self._session = session
