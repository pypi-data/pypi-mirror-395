# OpenList SDK 打包与发布指南 (uv 版)

本指南介绍如何使用 `uv` 工具链高效地构建和发布 `oplist-sdk`。

## 1. 准备工作

### 1.1 注册 PyPI 账号
- **PyPI (正式)**: [https://pypi.org/](https://pypi.org/)
- **TestPyPI (测试)**: [https://test.pypi.org/](https://test.pypi.org/)

### 1.2 获取 API Token
在 PyPI 账号设置 -> **API tokens** 中创建一个新 Token。
- 权限：**Entire account** (首次发布) 或 **Project: oplist-sdk** (后续发布)。
- **保存 Token**: 它是以 `pypi-` 开头的长字符串。

---

## 2. 构建项目 (Build)

在项目根目录下，直接运行：

```bash
uv build
```

**输出来源**:
- `dist/oplist_sdk-0.4.0-py3-none-any.whl` (Wheel 包)
- `dist/oplist_sdk-0.4.0.tar.gz` (源码包)

---

## 3. 发布 (Publish)

### 方法 A: 交互式发布 (推荐)

直接运行 publish 命令，`uv` 会自动提示或者尝试从环境读取。如果是首次，建议显式指定 Token。

```bash
# 发布到正式 PyPI
uv publish --token pypi-AgEIcHl...您的Token...
```

或者设置环境变量避免每次输入：
```powershell
$env:UV_PUBLISH_TOKEN = "pypi-..."
uv publish
```

### 方法 B: 发布到 TestPyPI (测试用)

如果您想先在测试环境验证：

```bash
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-AgENdGV...您的测试Token...
```

---

## 4. 常见问题

### 版本冲突 (HTTP 400)
PyPI 不允许覆盖版本。如果您修改了代码，**必须**在 `pyproject.toml` 中增加 `version` 版本号 (如 `0.4.0` -> `0.4.1`)，然后重新 `uv build`。

### 检查包内容
如果不确定包里打包了什么，可以用 tar 命令查看：
```bash
tar -tf dist/oplist_sdk-0.4.0.tar.gz
```
