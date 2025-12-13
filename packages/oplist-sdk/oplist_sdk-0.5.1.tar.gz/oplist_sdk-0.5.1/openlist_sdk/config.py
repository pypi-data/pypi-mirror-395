from enum import Enum
from typing import Any

class Endpoints(str, Enum):
    """
    OpenList API 路由端点
    完整的 API 端点配置
    """
    
    # --- 认证 (Auth) ---
    AUTH_LOGIN = "/api/auth/login"
    AUTH_LOGIN_HASH = "/api/auth/login/hash"
    AUTH_LOGOUT = "/api/auth/logout"
    AUTH_2FA_GENERATE = "/api/auth/2fa/generate"
    AUTH_2FA_VERIFY = "/api/auth/2fa/verify"
    AUTH_ME = "/api/me"
    AUTH_ME_UPDATE = "/api/me"  # PUT 方法
    
    # --- 用户 SSH 密钥 ---
    USER_SSH_KEYS = "/api/me/sshkeys"
    
    # --- 文件系统 (FS) ---
    FS_LIST = "/api/fs/list"
    FS_GET = "/api/fs/get"
    FS_DIRS = "/api/fs/dirs"
    FS_OTHER = "/api/fs/other"
    FS_MKDIR = "/api/fs/mkdir"
    FS_RENAME = "/api/fs/rename"
    FS_BATCH_RENAME = "/api/fs/batch_rename"
    FS_REGEX_RENAME = "/api/fs/regex_rename"
    FS_SEARCH = "/api/fs/search"
    FS_REMOVE = "/api/fs/remove"
    FS_REMOVE_EMPTY_DIR = "/api/fs/remove_empty_directory"
    FS_MOVE = "/api/fs/move"
    FS_RECURSIVE_MOVE = "/api/fs/recursive_move"
    FS_COPY = "/api/fs/copy"
    FS_PUT = "/api/fs/put"       # 流式上传
    FS_FORM = "/api/fs/form"     # 表单上传
    
    # --- 离线下载 & 压缩包 ---
    FS_OFFLINE_DOWNLOAD = "/api/fs/add_offline_download"
    FS_ARCHIVE_META = "/api/fs/archive/meta"
    FS_ARCHIVE_LIST = "/api/fs/archive/list"
    FS_ARCHIVE_DECOMPRESS = "/api/fs/archive/decompress"

    # --- 管理员 - 存储 ---
    ADMIN_STORAGE_LIST = "/api/admin/storage/list"
    ADMIN_STORAGE_GET = "/api/admin/storage/get"
    ADMIN_STORAGE_CREATE = "/api/admin/storage/create"
    ADMIN_STORAGE_UPDATE = "/api/admin/storage/update"
    ADMIN_STORAGE_DELETE = "/api/admin/storage/delete"
    ADMIN_STORAGE_ENABLE = "/api/admin/storage/enable"
    ADMIN_STORAGE_DISABLE = "/api/admin/storage/disable"
    ADMIN_STORAGE_RELOAD = "/api/admin/storage/reload"
    
    # --- 管理员 - 驱动 ---
    ADMIN_DRIVER_LIST = "/api/admin/driver/list"
    ADMIN_DRIVER_NAMES = "/api/admin/driver/names"
    ADMIN_DRIVER_INFO = "/api/admin/driver/info"
    
    # --- 管理员 - 用户 ---
    ADMIN_USER_LIST = "/api/admin/user/list"
    ADMIN_USER_GET = "/api/admin/user/get"
    ADMIN_USER_CREATE = "/api/admin/user/create"
    ADMIN_USER_UPDATE = "/api/admin/user/update"
    ADMIN_USER_DELETE = "/api/admin/user/delete"
    ADMIN_USER_CANCEL_2FA = "/api/admin/user/cancel_2fa"
    ADMIN_USER_DEL_CACHE = "/api/admin/user/del_cache"
    
    # --- 管理员 - 设置 ---
    ADMIN_SETTING_LIST = "/api/admin/setting/list"
    ADMIN_SETTING_GET = "/api/admin/setting/get"
    ADMIN_SETTING_SAVE = "/api/admin/setting/save"
    ADMIN_SETTING_DELETE = "/api/admin/setting/delete"
    ADMIN_SETTING_RESET_TOKEN = "/api/admin/setting/reset_token"
    
    # --- 管理员 - 元数据 ---
    ADMIN_META_LIST = "/api/admin/meta/list"
    ADMIN_META_GET = "/api/admin/meta/get"
    ADMIN_META_CREATE = "/api/admin/meta/create"
    ADMIN_META_UPDATE = "/api/admin/meta/update"
    ADMIN_META_DELETE = "/api/admin/meta/delete"
    
    # --- 管理员 - 搜索索引 ---
    ADMIN_INDEX_BUILD = "/api/admin/index/build"
    ADMIN_INDEX_UPDATE = "/api/admin/index/update"
    ADMIN_INDEX_STOP = "/api/admin/index/stop"
    ADMIN_INDEX_CLEAR = "/api/admin/index/clear"
    ADMIN_INDEX_PROGRESS = "/api/admin/index/progress"
    
    # --- 公共接口 ---
    PUBLIC_SETTINGS = "/api/public/settings"
    PUBLIC_OFFLINE_DOWNLOAD_TOOLS = "/api/public/offline_download_tools"
    PUBLIC_ARCHIVE_EXTENSIONS = "/api/public/archive_extensions"
    
    # --- 分享 ---
    SHARE_LIST = "/api/share/list"
    SHARE_GET = "/api/share/get"
    SHARE_CREATE = "/api/share/create"
    SHARE_UPDATE = "/api/share/update"
    SHARE_DELETE = "/api/share/delete"
    SHARE_ENABLE = "/api/share/enable"
    SHARE_DISABLE = "/api/share/disable"
    
    # --- 任务管理 (Task) ---
    # 复制任务
    TASK_COPY_DONE = "/api/task/copy/done"
    TASK_COPY_UNDONE = "/api/task/copy/undone"
    TASK_COPY_DELETE = "/api/task/copy/delete"
    TASK_COPY_CANCEL = "/api/task/copy/cancel"
    TASK_COPY_CLEAR_DONE = "/api/task/copy/clear_done"
    TASK_COPY_CLEAR_SUCCEEDED = "/api/task/copy/clear_succeeded"
    TASK_COPY_RETRY = "/api/task/copy/retry"
    
    # 移动任务
    TASK_MOVE_DONE = "/api/task/move/done"
    TASK_MOVE_UNDONE = "/api/task/move/undone"
    TASK_MOVE_DELETE = "/api/task/move/delete"
    TASK_MOVE_CANCEL = "/api/task/move/cancel"
    TASK_MOVE_CLEAR_DONE = "/api/task/move/clear_done"
    TASK_MOVE_CLEAR_SUCCEEDED = "/api/task/move/clear_succeeded"
    TASK_MOVE_RETRY = "/api/task/move/retry"
    
    # 上传任务
    TASK_UPLOAD_DONE = "/api/task/upload/done"
    TASK_UPLOAD_UNDONE = "/api/task/upload/undone"
    TASK_UPLOAD_DELETE = "/api/task/upload/delete"
    TASK_UPLOAD_CANCEL = "/api/task/upload/cancel"
    TASK_UPLOAD_CLEAR_DONE = "/api/task/upload/clear_done"
    TASK_UPLOAD_CLEAR_SUCCEEDED = "/api/task/upload/clear_succeeded"
    TASK_UPLOAD_RETRY = "/api/task/upload/retry"
    
    # 解压任务
    TASK_DECOMPRESS_DONE = "/api/task/decompress/done"
    TASK_DECOMPRESS_UNDONE = "/api/task/decompress/undone"
    TASK_DECOMPRESS_DELETE = "/api/task/decompress/delete"
    TASK_DECOMPRESS_CANCEL = "/api/task/decompress/cancel"
    TASK_DECOMPRESS_CLEAR_DONE = "/api/task/decompress/clear_done"
    TASK_DECOMPRESS_CLEAR_SUCCEEDED = "/api/task/decompress/clear_succeeded"
    TASK_DECOMPRESS_RETRY = "/api/task/decompress/retry"
    
    # 解压上传任务
    TASK_DECOMPRESS_UPLOAD_DONE = "/api/task/decompress_upload/done"
    TASK_DECOMPRESS_UPLOAD_UNDONE = "/api/task/decompress_upload/undone"
    TASK_DECOMPRESS_UPLOAD_DELETE = "/api/task/decompress_upload/delete"
    TASK_DECOMPRESS_UPLOAD_CANCEL = "/api/task/decompress_upload/cancel"
    TASK_DECOMPRESS_UPLOAD_CLEAR_DONE = "/api/task/decompress_upload/clear_done"
    TASK_DECOMPRESS_UPLOAD_CLEAR_SUCCEEDED = "/api/task/decompress_upload/clear_succeeded"
    TASK_DECOMPRESS_UPLOAD_RETRY = "/api/task/decompress_upload/retry"
    
    # 离线下载任务
    TASK_OFFLINE_DOWNLOAD_DONE = "/api/task/offline_download/done"
    TASK_OFFLINE_DOWNLOAD_UNDONE = "/api/task/offline_download/undone"
    TASK_OFFLINE_DOWNLOAD_DELETE = "/api/task/offline_download/delete"
    TASK_OFFLINE_DOWNLOAD_CANCEL = "/api/task/offline_download/cancel"
    TASK_OFFLINE_DOWNLOAD_CLEAR_DONE = "/api/task/offline_download/clear_done"
    TASK_OFFLINE_DOWNLOAD_CLEAR_SUCCEEDED = "/api/task/offline_download/clear_succeeded"
    TASK_OFFLINE_DOWNLOAD_RETRY = "/api/task/offline_download/retry"
    
    @staticmethod
    def join(host: str, endpoint: Any) -> str:
        """拼接主机地址和端点路径"""
        path = endpoint.value if hasattr(endpoint, 'value') else str(endpoint)
        return f"{host.rstrip('/')}{path}"
