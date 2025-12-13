"""
OpenList Python SDK

一个强大的、类型安全的 Python SDK，用于与 OpenList (AList Fork) API 进行交互。

快速开始:
    from openlist_sdk import OpenListClient
    
    client = OpenListClient("http://nas:5244", "admin", "password")
    resp = client.fs.list("/my_drive")
    if resp["code"] == 200:
        for f in resp["data"]["content"]:
            print(f["name"])
"""
from .client import OpenListClient

__version__ = "0.4.0"
__all__ = [
    "OpenListClient"
]