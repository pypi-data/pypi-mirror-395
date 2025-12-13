"""
文件系统命名空间
核心文件操作：列出、上传、下载、重命名、移动、复制、删除、搜索、压缩包处理。
"""
import os
from pathlib import Path
from typing import Iterator, Literal, Union, BinaryIO, List, Optional, Dict, Any
from . import BaseNamespace
from ..config import Endpoints


class ArchiveHelper:
    """远程压缩包操作助手，无需下载即可操作"""
    
    def __init__(self, path: str, session):
        self.path = path
        self._session = session

    def meta(self, password: str = "") -> Dict[str, Any]:
        """
        获取压缩包元数据，无需解压。
        """
        payload = {"path": self.path, "password": password}
        return self._session.request("POST", Endpoints.FS_ARCHIVE_META, json=payload)

    def list(self, password: str = "", inner_path: str = "") -> Dict[str, Any]:
        """
        列出压缩包内容，无需下载。
        """
        payload = {
            "path": self.path, 
            "password": password,
            "inner_path": inner_path
        }
        return self._session.request("POST", Endpoints.FS_ARCHIVE_LIST, json=payload)

    def decompress(self, dest_path: str = "", password: str = "", 
                   cache_full_path: bool = True, put_into_new_dir: bool = False) -> Dict[str, Any]:
        """
        解压压缩包到目标文件夹。
        """
        payload = {
            "src_dir": str(Path(self.path).parent),
            "dst_dir": dest_path or str(Path(self.path).parent),
            "names": [Path(self.path).name],
            "password": password,
            "cache_full_path": cache_full_path,
            "put_into_new_dir": put_into_new_dir
        }
        return self._session.request("POST", Endpoints.FS_ARCHIVE_DECOMPRESS, json=payload)


class FileSystemNamespace(BaseNamespace):
    """文件系统操作"""
    
    # ==================== 基础操作 ====================
    
    def list(self, path: str, page: int = 1, per_page: int = 0, 
             refresh: bool = False, password: str = "") -> Dict[str, Any]:
        """
        列出目录中的文件。
        """
        payload = {
            "path": path,
            "page": page,
            "per_page": per_page,
            "refresh": refresh,
            "password": password
        }
        return self._session.request("POST", Endpoints.FS_LIST, json=payload)

    def get(self, path: str, password: str = "") -> Dict[str, Any]:
        """
        获取文件或文件夹信息。
        """
        payload = {"path": path, "password": password}
        return self._session.request("POST", Endpoints.FS_GET, json=payload)

    def dirs(self, path: str, password: str = "", force_root: bool = False) -> Dict[str, Any]:
        """
        获取目录树 (仅文件夹)。
        """
        payload = {"path": path, "password": password, "force_root": force_root}
        return self._session.request("POST", Endpoints.FS_DIRS, json=payload)

    def other(self, path: str, method: str, password: str = "") -> Dict[str, Any]:
        """
        获取存储提供商特定的附加操作。
        """
        payload = {"path": path, "method": method, "password": password}
        return self._session.request("POST", Endpoints.FS_OTHER, json=payload)

    # ==================== 目录操作 ====================
    
    def mkdir(self, path: str) -> Dict[str, Any]:
        """
        创建目录 (递归创建)。
        """
        return self._session.request("POST", Endpoints.FS_MKDIR, json={"path": path})

    # ==================== 重命名操作 ====================
    
    def rename(self, path: str, new_name: str) -> Dict[str, Any]:
        """
        重命名文件或文件夹。
        """
        return self._session.request("POST", Endpoints.FS_RENAME, json={
            "path": path, 
            "name": new_name
        })

    def batch_rename(self, path: str, rename_objects: List[dict]) -> Dict[str, Any]:
        """
        批量重命名多个文件。
        """
        return self._session.request("POST", Endpoints.FS_BATCH_RENAME, json={
            "src_dir": path,
            "rename_objects": rename_objects
        })

    def rename_regex(self, path: str, pattern: str, replace: str) -> Dict[str, Any]:
        """
        使用正则表达式重命名文件。
        """
        payload = {
            "src_dir": path,
            "src_name_regex": pattern,
            "new_name_regex": replace
        }
        return self._session.request("POST", Endpoints.FS_REGEX_RENAME, json=payload)

    # ==================== 移动 & 复制 ====================
    
    def move(self, src_dir: str, dst_dir: str, names: List[str] = None) -> Dict[str, Any]:
        """
        移动文件或文件夹到另一位置。
        """
        if not names:
            # 如果 names 为空，列出 src_dir 下的所有内容
            resp = self.list(src_dir, per_page=0)
            if resp["code"] != 200:
                return resp
            
            # 手动解析字典
            data = resp.get("data")
            content = data.get("content", []) if isinstance(data, dict) else []
            names = [f.get("name") for f in content if f.get("name")]
            
            if not names:
                return {"code": 200, "message": "No files to move", "data": None}

        return self._session.request("POST", Endpoints.FS_MOVE, json={
            "src_dir": src_dir,
            "dst_dir": dst_dir,
            "names": names
        })

    def recursive_move(self, src_dir: str, dst_dir: str) -> Dict[str, Any]:
        """
        递归移动目录，保留结构。
        """
        return self._session.request("POST", Endpoints.FS_RECURSIVE_MOVE, json={
            "src_dir": src_dir,
            "dst_dir": dst_dir
        })

    def copy(self, src_dir: str, dst_dir: str, names: List[str] = None) -> Dict[str, Any]:
        """
        复制文件或文件夹到另一位置。
        """
        if not names:
            # 如果 names 为空，列出 src_dir 下的所有内容
            resp = self.list(src_dir, per_page=0)
            if resp["code"] != 200:
                return resp
            
            data = resp.get("data")
            content = data.get("content", []) if isinstance(data, dict) else []
            names = [f.get("name") for f in content if f.get("name")]
            
            if not names:
                return {"code": 200, "message": "No files to copy", "data": None}

        return self._session.request("POST", Endpoints.FS_COPY, json={
            "src_dir": src_dir,
            "dst_dir": dst_dir,
            "names": names
        })

    # ==================== 删除操作 ====================
    
    def remove(self, path: str, names: List[str] = None) -> Dict[str, Any]:
        """
        删除文件或目录。
        """
        if names is None:
            # 单路径模式
            parent, name = path.rsplit("/", 1) if "/" in path else ("", path)
            payload = {"dir": parent or "/", "names": [name]}
        else:
            # 批量模式
            payload = {"dir": path, "names": names}
            
        return self._session.request("POST", Endpoints.FS_REMOVE, json=payload)

    def remove_empty_dirs(self, path: str) -> Dict[str, Any]:
        """
        递归删除空目录。
        """
        return self._session.request("POST", Endpoints.FS_REMOVE_EMPTY_DIR, json={"src_dir": path})

    # ==================== 上传操作 ====================
    
    def upload(self, local_path: Union[str, Path, BinaryIO], remote_path: str, 
               as_task: bool = False) -> Dict[str, Any]:
        """
        使用流式上传文件 (PUT 方法)。
        """
        # 确定文件内容和大小
        if isinstance(local_path, (str, Path)):
            file_path = Path(local_path)
            file_size = file_path.stat().st_size
            file_obj = open(file_path, 'rb')
            should_close = True
        else:
            # 文件对象
            file_obj = local_path
            file_obj.seek(0, 2)  # 移动到末尾
            file_size = file_obj.tell()
            file_obj.seek(0)  # 重置到开头
            should_close = False
        
        try:
            headers = {
                "File-Path": remote_path,
                "Content-Length": str(file_size),
                "Content-Type": "application/octet-stream",
                "As-Task": str(as_task).lower()
            }
            
            resp = self._session.request(
                "PUT", 
                Endpoints.FS_PUT, 
                content=file_obj,
                headers=headers
            )
            
            # 原始返回不需要转换，如果 data 是 task_id 字典，它本身就是字典
            return resp
            
        finally:
            if should_close:
                file_obj.close()

    def upload_form(self, local_path: Union[str, Path], remote_dir: str, 
                    filename: str = None) -> Dict[str, Any]:
        """
        使用多部分表单上传文件 (POST 方法)。
        """
        file_path = Path(local_path)
        upload_name = filename or file_path.name
        
        with open(file_path, 'rb') as f:
            files = {'file': (upload_name, f, 'application/octet-stream')}
            return self._session.request(
                "PUT",
                Endpoints.FS_FORM,
                files=files,
                headers={"File-Path": f"{remote_dir.rstrip('/')}/{upload_name}"}
            )

    # ==================== 离线下载 ====================
    
    def offline_download(self, urls: Union[str, List[str]], path: str, 
                         tool: str = "") -> Dict[str, Any]:
        """
        添加离线下载任务。
        """
        if isinstance(urls, str):
            urls = [urls]
            
        payload = {
            "urls": urls,
            "path": path
        }
        if tool:
            payload["tool"] = tool
            
        return self._session.request("POST", Endpoints.FS_OFFLINE_DOWNLOAD, json=payload)

    # ==================== 压缩包操作 ====================
    
    def archive(self, path: str) -> ArchiveHelper:
        """
        获取远程压缩包操作助手。
        """
        return ArchiveHelper(path, self._session)

    # ==================== 搜索操作 ====================

    def search(self, 
               path: str, 
               keyword: str, 
               scope: int = 0,
               page: int = 1,
               per_page: int = 100,
               password: str = "") -> Dict[str, Any]:
        """
        使用服务端索引搜索文件。
        """
        payload = {
            "parent": path,
            "keywords": keyword,
            "scope": scope,
            "page": page,
            "per_page": per_page,
            "password": password
        }
        return self._session.request("POST", Endpoints.FS_SEARCH, json=payload)

    def walk(self, path: str, keyword: str = "", refresh: bool = False, 
             max_depth: int = 5) -> Iterator[Dict[str, Any]]:
        """
        递归遍历目录树，返回文件对象字典。
        """
        yield from self._walk_recursive(path, keyword, refresh, max_depth, 0)

    def _walk_recursive(self, path: str, keyword: str, refresh: bool, 
                        max_depth: int, current_depth: int) -> Iterator[Dict[str, Any]]:
        """内部递归遍历实现"""
        if current_depth > max_depth:
            return

        resp = self.list(path, per_page=0, refresh=refresh)
        if resp["code"] != 200 or not resp.get("data"):
            return
            
        data = resp["data"]
        content = data.get("content", []) if isinstance(data, dict) else []

        for item in content:
            # 如果提供了关键词则匹配
            # item 是字典
            name = item.get("name", "")
            if not keyword or keyword.lower() in name.lower():
                item["parent"] = path # 注入父路径信息
                yield item

            # 递归进入子目录
            if item.get("is_dir"):
                sub_path = f"{path.rstrip('/')}/{name}"
                yield from self._walk_recursive(
                    sub_path, keyword, refresh, max_depth, current_depth + 1
                )