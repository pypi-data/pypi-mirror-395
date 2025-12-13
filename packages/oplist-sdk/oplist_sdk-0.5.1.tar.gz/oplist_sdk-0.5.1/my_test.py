from openlist_sdk import OpenListClient

# 配置信息
HOST = ""
USERNAME = ""
PASSWORD = ""
# 如果有Token，可以直接使用 Token 避免每次请求都登录
# TOKEN = "..." 

# 初始化一个全局客户端 (或者在 main 中初始化传参)
# 这里演示直接初始化，方便通过脚本直接运行
client = OpenListClient(HOST, username=USERNAME, password=PASSWORD)

def test_login():
    # client 已经在初始化时自动登录了（如果提供了用户名密码）
    # 这里我们演示手动检查登录状态
    print("Self:", client.auth.get_me())

def test_auth():
    # 复用 client
    resp = client.auth.get_me()
    print("Auth Me:", resp)

# public
def test_setting():
    resp = client.public.settings()
    print("Settings:", resp)

def offline_download_tools():
    resp = client.public.offline_download_tools()
    print("Tools:", resp)

def archive_extensions():
    resp = client.public.archive_extensions()
    print("Extensions:", resp)

# fs
def fs_list():
    # 复用 client
    resp = client.fs.list(path="/123pan")
    print("Files:", resp)

def fs_task_status():
    # 测试 unified get
    print("--- Testing Unified Get ---")
    resp = client.task.get("xxxxxx")
    print("Unified Get Result:", resp)
    
    # 假设我们有一个真实的 ID (虽然这里还是假的，但演示调用)
    # ids = ["id1", "id2"]
    # resp_batch = client.task.get_batch(ids)
    # print("Unified Batch Result:", resp_batch)

if __name__ == "__main__":
    # 按需调用
    # test_login()
    # test_auth()
    # test_setting()
    fs_task_status()

