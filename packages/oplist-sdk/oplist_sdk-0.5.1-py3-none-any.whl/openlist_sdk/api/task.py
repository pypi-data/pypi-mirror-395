"""
任务命名空间
异步任务管理：复制、移动、上传、解压、离线下载任务的监控和控制。
"""
import time
import re
from typing import List, Literal, Union, Optional, Dict, Any
from . import BaseNamespace
from ..config import Endpoints

TaskType = Literal["copy", "move", "upload", "decompress", "decompress_upload", "offline_download"]

class TaskState:
    """任务状态常量"""
    PENDING = 0      # 等待中
    RUNNING = 1      # 运行中
    SUCCEEDED = 2    # 成功
    CANCELING = 3    # 取消中
    CANCELED = 4     # 已取消
    ERRORED = 5      # 出错
    FAILING = 6      # 失败中
    FAILED = 7       # 已失败
    WAIT_RETRY = 8   # 等待重试
    BEFORE_RETRY = 9 # 重试前


def _parse_task_name(name: str) -> dict:
    """内部辅助：解析任务名称"""
    result = {
        "action": "",
        "src_mount": "",
        "src_path": "",
        "dst_mount": "",
        "dst_path": ""
    }
    if not name:
        return result
    
    # 解析格式: "action [mount](path) to [mount](path)"
    pattern = r'^(\w+)\s+\[([^\]]*)\]\(([^)]*)\)(?:\s+to\s+\[([^\]]*)\]\(([^)]*)\))?'
    match = re.match(pattern, name)
    
    if match:
        result["action"] = match.group(1) or ""
        result["src_mount"] = match.group(2) or ""
        result["src_path"] = match.group(3) or ""
        result["dst_mount"] = match.group(4) or ""
        result["dst_path"] = match.group(5) or ""
    return result

def _get_full_path(mount: str, path: str) -> str:
    """内部辅助：获取完整路径"""
    if mount and path:
        return f"{mount.rstrip('/')}/{path.lstrip('/')}" if path != "/" else mount
    return path or mount

def _task_matches_path(task: dict, src_path: str = None, dst_path: str = None) -> bool:
    """内部辅助：检查任务是否匹配路径"""
    name = task.get("name", "")
    parsed = _parse_task_name(name)
    
    if src_path:
        full_src = _get_full_path(parsed["src_mount"], parsed["src_path"])
        if src_path not in full_src and full_src not in src_path:
            return False
            
    if dst_path:
        full_dst = _get_full_path(parsed["dst_mount"], parsed["dst_path"])
        if dst_path not in full_dst and full_dst not in dst_path:
            return False
            
    return True


class TaskTypeHelper:
    """单一任务类型的操作助手"""
    
    def __init__(self, session, task_type: TaskType):
        self._session = session
        self._task_type = task_type
        self._endpoints = self._get_endpoints()
    
    def _get_endpoints(self) -> dict:
        """获取该任务类型的所有端点"""
        type_upper = self._task_type.upper()
        return {
            "done": getattr(Endpoints, f"TASK_{type_upper}_DONE"),
            "undone": getattr(Endpoints, f"TASK_{type_upper}_UNDONE"),
            "delete": getattr(Endpoints, f"TASK_{type_upper}_DELETE"),
            "cancel": getattr(Endpoints, f"TASK_{type_upper}_CANCEL"),
            "clear_done": getattr(Endpoints, f"TASK_{type_upper}_CLEAR_DONE"),
            "clear_succeeded": getattr(Endpoints, f"TASK_{type_upper}_CLEAR_SUCCEEDED"),
            "retry": getattr(Endpoints, f"TASK_{type_upper}_RETRY"),
        }

    def get(self, task_id: str) -> Dict[str, Any]:
        """
        根据 ID 获取单个任务详情。
        """
        # 1. 优先查找进行中的任务 (最常用的场景)
        r_undone = self.undone()
        if r_undone["code"] == 200 and isinstance(r_undone.get("data"), list):
            for task in r_undone["data"]:
                if task.get("id") == task_id:
                    return {"code": 200, "message": "success", "data": task}
        elif r_undone["code"] != 200:
            return r_undone
            
        # 2. 查找已完成的任务
        r_done = self.done()
        if r_done["code"] == 200 and isinstance(r_done.get("data"), list):
            for task in r_done["data"]:
                if task.get("id") == task_id:
                     return {"code": 200, "message": "success", "data": task}
        elif r_done["code"] != 200:
            return r_done
            
        return {"code": 404, "message": f"Task {task_id} not found", "data": None}

    def get_batch(self, task_ids: List[str]) -> Dict[str, Any]:
        """
        批量获取任务详情。
        返回一个字典，Key 为 task_id，Value 为任务对象 (没找到则为 None)。
        """
        target_ids = set(task_ids)
        result_map = {tid: None for tid in task_ids}
        
        # 获取所有任务 (只请求两次 API)
        r_undone = self.undone()
        r_done = self.done()
        
        all_tasks = []
        if r_undone["code"] == 200:
            all_tasks.extend(r_undone.get("data") or [])
        if r_done["code"] == 200:
            all_tasks.extend(r_done.get("data") or [])
            
        for task in all_tasks:
            tid = task.get("id")
            if tid in target_ids:
                result_map[tid] = task
                
        # 包装统一的返回结构，虽然 data 是 dict 这里的 code=200 表示查询过程成功
        return {"code": 200, "message": "success", "data": result_map}
    
    def done(self) -> Dict[str, Any]:
        """获取已完成的任务列表"""
        return self._session.request("GET", self._endpoints["done"])
    
    def undone(self) -> Dict[str, Any]:
        """获取进行中/未完成的任务列表"""
        return self._session.request("GET", self._endpoints["undone"])
    
    def all(self) -> Dict[str, Any]:
        """获取所有任务 (已完成 + 进行中)"""
        r1 = self.done()
        r2 = self.undone()
        
        if r1["code"] != 200: return r1
        if r2["code"] != 200: return r2
        
        combined = (r1.get("data") or []) + (r2.get("data") or [])
        return {"code": 200, "message": "success", "data": combined}
    
    def delete(self, task_id: str) -> Dict[str, Any]:
        """删除一个任务记录"""
        return self._session.request("POST", self._endpoints["delete"], params={"tid": task_id})
    
    def cancel(self, task_id: str) -> Dict[str, Any]:
        """取消一个进行中的任务"""
        return self._session.request("POST", self._endpoints["cancel"], params={"tid": task_id})
    
    def retry(self, task_id: str) -> Dict[str, Any]:
        """重试一个失败的任务"""
        return self._session.request("POST", self._endpoints["retry"], params={"tid": task_id})
    
    def clear_done(self) -> Dict[str, Any]:
        """清除所有已完成的任务记录"""
        return self._session.request("POST", self._endpoints["clear_done"])
    
    def clear_succeeded(self) -> Dict[str, Any]:
        """清除所有成功的任务记录"""
        return self._session.request("POST", self._endpoints["clear_succeeded"])
    
    def count_pending(self) -> int:
        """获取进行中的任务数量"""
        resp = self.undone()
        if resp["code"] == 200 and isinstance(resp.get("data"), list):
            return len(resp["data"])
        return -1
    
    def count_done(self) -> int:
        """获取已完成的任务数量"""
        resp = self.done()
        if resp["code"] == 200 and isinstance(resp.get("data"), list):
            return len(resp["data"])
        return -1
    
    def is_all_done(self) -> bool:
        """检查是否所有任务都已完成"""
        return self.count_pending() == 0
    
    def wait_all(self, timeout: int = 300, interval: float = 2.0) -> bool:
        """等待所有任务完成"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_all_done():
                return True
            time.sleep(interval)
        return False
    
    def find_by_path(self, src_path: str = None, dst_path: str = None, 
                     include_done: bool = True) -> Dict[str, Any]:
        """
        根据源路径或目标路径查找任务。
        """
        result = []
        
        # 搜索进行中的任务
        r_undone = self.undone()
        if r_undone["code"] == 200 and isinstance(r_undone.get("data"), list):
            for task in r_undone["data"]:
                if _task_matches_path(task, src_path, dst_path):
                    result.append(task)
        elif r_undone["code"] != 200:
            return r_undone
        
        # 搜索已完成的任务
        if include_done:
            r_done = self.done()
            if r_done["code"] == 200 and isinstance(r_done.get("data"), list):
                for task in r_done["data"]:
                    if _task_matches_path(task, src_path, dst_path):
                        result.append(task)
            elif r_done["code"] != 200:
                return r_done
        
        return {"code": 200, "message": "success", "data": result}
    
    def find_exact(self, src_path: str, dst_path: str) -> Dict[str, Any]:
        """
        通过精确匹配源和目标路径来获取任务。
        """
        if src_path != "/": src_path = src_path.rstrip("/")
        if dst_path != "/": dst_path = dst_path.rstrip("/")
            
        def is_match(task: dict) -> bool:
            name = task.get("name", "")
            parsed = _parse_task_name(name)
            t_src = _get_full_path(parsed["src_mount"], parsed["src_path"])
            t_dst = _get_full_path(parsed["dst_mount"], parsed["dst_path"])
            
            if t_src != "/": t_src = t_src.rstrip("/")
            if t_dst != "/": t_dst = t_dst.rstrip("/")
            return t_src == src_path and t_dst == dst_path

        # 1. 优先查找进行中的
        r_undone = self.undone()
        if r_undone["code"] == 200 and isinstance(r_undone.get("data"), list):
            for task in r_undone["data"]:
                if is_match(task):
                    return {"code": 200, "message": "success", "data": task}

        # 2. 查找已完成的
        r_done = self.done()
        if r_done["code"] == 200 and isinstance(r_done.get("data"), list):
            for task in r_done["data"]:
                if is_match(task):
                    return {"code": 200, "message": "success", "data": task}
        
        return {"code": 200, "message": "success", "data": None}

    def find_one_by_path(self, src_path: str = None, dst_path: str = None) -> Dict[str, Any]:
        """根据路径查找单个任务"""
        resp = self.find_by_path(src_path, dst_path, include_done=False)
        if resp["code"] == 200 and resp.get("data"):
            return {"code": 200, "message": "success", "data": resp["data"][0]}
        
        resp = self.find_by_path(src_path, dst_path, include_done=True)
        if resp["code"] == 200 and resp.get("data"):
            return {"code": 200, "message": "success", "data": resp["data"][0]}
            
        return resp
    
    def wait_for_path(self, src_path: str = None, dst_path: str = None,
                      timeout: int = 300, interval: float = 2.0) -> Optional[Dict[str, Any]]:
        """
        等待指定路径的任务完成。通过不断轮询状态。
        返回任务字典，或 None。
        """
        start_time = time.time()
        last_task = None
        
        while time.time() - start_time < timeout:
            resp = self.find_one_by_path(src_path, dst_path)
            if resp["code"] == 200 and resp.get("data"):
                task = resp["data"]
                # 检查状态
                state = task.get("state")
                if state in (TaskState.SUCCEEDED, TaskState.FAILED, TaskState.CANCELED, TaskState.ERRORED):
                    return task
                last_task = task
            time.sleep(interval)
        
        return last_task
    
    def has_pending_for_path(self, src_path: str = None, dst_path: str = None) -> bool:
        """检查是否有指定路径的进行中任务"""
        resp = self.find_by_path(src_path, dst_path, include_done=False)
        return bool(resp["code"] == 200 and resp.get("data"))
    
    def get_status_for_path(self, src_path: str = None, dst_path: str = None) -> dict:
        """获取指定路径任务的状态摘要"""
        result = {
            "exists": False,
            "is_pending": False,
            "is_done": False,
            "is_success": False,
            "progress": 0,
            "task": None
        }
        resp = self.find_one_by_path(src_path, dst_path)
        if resp["code"] == 200 and resp.get("data"):
            task = resp["data"]
            state = task.get("state")
            result["exists"] = True
            result["task"] = task
            result["is_pending"] = state == TaskState.PENDING or state == TaskState.RUNNING
            result["is_done"] = state in (TaskState.SUCCEEDED, TaskState.FAILED, TaskState.CANCELED, TaskState.ERRORED)
            result["is_success"] = state == TaskState.SUCCEEDED
            result["progress"] = task.get("progress", 0)
        return result


class TaskNamespace(BaseNamespace):
    """任务管理命名空间"""
    
    def __init__(self, session):
        super().__init__(session)
        self.copy = TaskTypeHelper(session, "copy")
        self.move = TaskTypeHelper(session, "move")
        self.upload = TaskTypeHelper(session, "upload")
        self.decompress = TaskTypeHelper(session, "decompress")
        self.decompress_upload = TaskTypeHelper(session, "decompress_upload")
        self.offline_download = TaskTypeHelper(session, "offline_download")
    
    def all_pending(self) -> List[Dict[str, Any]]:
        """获取所有类型的进行中任务"""
        result = []
        for helper in [self.copy, self.move, self.upload, self.decompress, self.decompress_upload, self.offline_download]:
            resp = helper.undone()
            if resp["code"] == 200 and isinstance(resp.get("data"), list):
                result.extend(resp["data"])
        return result
        
    def summary(self) -> dict:
        return {
            "copy": {"pending": self.copy.count_pending(), "done": self.copy.count_done()},
            "move": {"pending": self.move.count_pending(), "done": self.move.count_done()},
            "upload": {"pending": self.upload.count_pending(), "done": self.upload.count_done()},
            "decompress": {"pending": self.decompress.count_pending(), "done": self.decompress.count_done()},
            "decompress_upload": {"pending": self.decompress_upload.count_pending(), "done": self.decompress_upload.count_done()},
            "offline_download": {"pending": self.offline_download.count_pending(), "done": self.offline_download.count_done()},
        }

    def get(self, task_id: str) -> Dict[str, Any]:
        """
        全量搜索：在所有已知的任务类型中查找指定 ID 的任务。
        一旦找到第一个匹配项即返回。
        """
        # 遍历所有助手
        helpers = [
            self.copy, self.move, self.upload, 
            self.decompress, self.decompress_upload, self.offline_download
        ]
        
        for helper in helpers:
            resp = helper.get(task_id)
            if resp["code"] == 200:
                # 找到了，为了方便后续处理，我们可以注入一个 type 字段（可选）
                # resp["data"]["_type"] = helper._task_type
                return resp
                
        return {"code": 404, "message": f"Task {task_id} not found in any known task types", "data": None}

    def get_batch(self, task_ids: List[str]) -> Dict[str, Any]:
        """
        全量批量搜索：在所有已知的任务类型中查找。
        """
        result_map = {tid: None for tid in task_ids}
        remaining_ids = set(task_ids)
        
        helpers = [
            self.copy, self.move, self.upload, 
            self.decompress, self.decompress_upload, self.offline_download
        ]
        
        for helper in helpers:
            if not remaining_ids:
                break
                
            # 只查询还在找的 ID
            current_batch_ids = list(remaining_ids)
            resp = helper.get_batch(current_batch_ids)
            
            if resp["code"] == 200:
                data = resp.get("data", {})
                for tid, task in data.items():
                    if task:
                        result_map[tid] = task
                        if tid in remaining_ids:
                            remaining_ids.remove(tid)
                            
        return {"code": 200, "message": "success", "data": result_map}
