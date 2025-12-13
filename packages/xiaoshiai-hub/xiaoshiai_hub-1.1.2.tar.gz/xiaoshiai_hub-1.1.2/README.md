# XiaoShi AI Hub Python SDK

[![PyPI version](https://badge.fury.io/py/xiaoshiai-hub.svg)](https://badge.fury.io/py/xiaoshiai-hub)
[![Python Support](https://img.shields.io/pypi/pyversions/xiaoshiai-hub.svg)](https://pypi.org/project/xiaoshiai-hub/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

XiaoShi AI Hub Python SDK 是一个功能强大的 Python 库，用于与 XiaoShi AI Hub 平台进行交互。它提供了简单易用的 API 和命令行工具，支持模型和数据集的上传、下载，并支持大型模型文件的透明加密功能。


## ✨ 特性

- 🚀 **简单易用** - 类似 Hugging Face Hub 的 API 设计，上手即用
- 🖥️ **命令行工具** - 提供 `moha` CLI，无需编写代码即可上传下载
- 📥 **下载功能** - 支持下载单个文件或整个仓库
- 📤 **上传功能** - 支持上传文件和文件夹到仓库
- 🔐 **智能加密** - 自动加密大型模型文件（≥5MB 的 .safetensors、.bin、.pt、.pth、.ckpt 文件）
- 🎯 **模式匹配** - 支持使用 allow/ignore 模式过滤文件
- 📊 **进度显示** - 下载和上传时显示进度条
- 🔑 **多种认证** - 支持用户名/密码和 Token 认证
- 🌐 **环境变量配置** - 灵活的 Hub URL 配置
- 💾 **缓存支持** - 高效的文件缓存机制
- 🔍 **类型提示** - 完整的类型注解，IDE 友好
- ✅ **仓库验证** - 上传前自动检查仓库是否存在

## 📦 安装

### 基础安装

```bash
pip install xiaoshiai-hub
```



## 🚀 快速开始

### 命令行工具 (CLI)

安装后即可使用 `moha` 命令行工具：

```bash
# 查看帮助
moha --help

# 上传文件夹到仓库
moha upload ./my_model org/my-model --username your-username --password your-password

# 上传单个文件
moha upload-file ./config.yaml org/my-model --username your-username --password your-password

# 下载整个仓库
moha download org/my-model --username your-username --password your-password

# 下载单个文件
moha download-file org/my-model config.yaml --username your-username --password your-password
```

详细的 CLI 使用说明请参考 [命令行工具](#-命令行工具-cli) 章节。

### Python API

#### 下载单个文件

```python
from xiaoshiai_hub import moha_hub_download

# 下载单个文件
file_path = moha_hub_download(
    repo_id="demo/demo",
    filename="config.yaml",
    repo_type="models",  # 或 "datasets"
    username="your-username",
    password="your-password",
)
print(f"文件已下载到: {file_path}")
```

#### 下载整个仓库

```python
from xiaoshiai_hub import snapshot_download

# 下载整个仓库
repo_path = snapshot_download(
    repo_id="demo/demo",
    repo_type="models",
    username="your-username",
    password="your-password",
)
print(f"仓库已下载到: {repo_path}")
```

#### 使用过滤器下载

```python
from xiaoshiai_hub import snapshot_download

# 只下载 YAML 和 Markdown 文件
repo_path = snapshot_download(
    repo_id="demo/demo",
    allow_patterns=["*.yaml", "*.yml", "*.md"],
    ignore_patterns=[".git*", "*.log"],
    username="your-username",
    password="your-password",
)
```

#### 上传文件

```python
from xiaoshiai_hub import upload_file

# 上传单个文件
result = upload_file(
    path_file="./config.yaml",
    path_in_repo="config.yaml",
    repo_id="demo/my-model",
    repo_type="models",
    commit_message="Upload config file",
    username="your-username",
    password="your-password",
)
print(f"上传成功: {result}")
```

#### 上传文件夹

```python
from xiaoshiai_hub import upload_folder

# 上传整个文件夹
result = upload_folder(
    folder_path="./my_model",
    repo_id="demo/my-model",
    repo_type="models",
    commit_message="Upload model files",
    ignore_patterns=["*.log", ".git*"],  # 忽略这些文件
    username="your-username",
    password="your-password",
)
print(f"上传成功: {result}")
```

#### 加密上传

SDK 会自动加密大型模型文件（≥5MB 的 .safetensors、.bin、.pt、.pth、.ckpt 文件）：

```python
from xiaoshiai_hub import upload_file

# 上传文件，大型模型文件会自动加密
result = upload_file(
    path_file="./model.safetensors",  # 如果 ≥5MB，会自动加密
    path_in_repo="model.safetensors",
    repo_id="demo/my-model",
    repo_type="models",
    encryption_password="your-secure-password",  # 设置加密密码
    username="your-username",
    password="your-password",
)
```

#### 上传文件夹（自动加密大文件）

```python
from xiaoshiai_hub import upload_folder

# 上传文件夹，大型模型文件会自动加密
result = upload_folder(
    folder_path="./my_model",
    repo_id="demo/my-model",
    repo_type="models",
    encryption_password="your-secure-password",  # 大文件会自动加密
    ignore_patterns=["*.log", ".git*"],
    username="your-username",
    password="your-password",
)

```

#### 使用 HubClient API

```python
from xiaoshiai_hub import HubClient

# 创建客户端
client = HubClient(
    username="your-username",
    password="your-password",
)

# 获取仓库信息
repo_info = client.get_repository_info("demo", "models", "my-model")
print(f"仓库名称: {repo_info.name}")
print(f"组织: {repo_info.organization}")

# 列出分支
branches = client.list_branches("demo", "models", "my-model")
for branch in branches:
    print(f"分支: {branch.name} (commit: {branch.commit_sha})")

# 浏览仓库内容
content = client.get_repository_content("demo", "models", "my-model", "main")
for entry in content.entries:
    print(f"{entry.type}: {entry.name}")
```

## 🔐 加密功能

SDK 提供了智能加密功能，支持 **AES** 和 **SM4** 两种加密算法对大型模型文件进行加密。

### 支持的加密算法

| 算法 | 说明 |
|------|------|
| `AES` | AES-256-CTR 模式，国际通用标准（默认） |
| `SM4` | SM4-CTR 模式，国密标准 |

### 自动加密规则

上传时，SDK 会自动加密符合以下条件的文件：

1. **文件大小** ≥ 5MB
2. **文件扩展名**为：`.safetensors`、`.bin`、`.pt`、`.pth`、`.ckpt`

小文件和其他类型的文件（如配置文件、README 等）不会被加密，保持可读性。

### 使用加密功能

```python
from xiaoshiai_hub import upload_folder

# 上传文件夹，使用 AES 加密（默认）
result = upload_folder(
    folder_path="./llama-7b",
    repo_id="demo/llama-7b",
    encryption_password="my-secure-password-123",
    username="your-username",
    password="your-password",
)

# 使用 SM4 国密算法加密
result = upload_folder(
    folder_path="./llama-7b",
    repo_id="demo/llama-7b",
    encryption_password="my-secure-password-123",
    algorithm="SM4",  # 使用 SM4 加密
    username="your-username",
    password="your-password",
)

# 文件夹中的大型模型文件（如 model.safetensors）会被自动加密
# 小文件（如 config.json、README.md）保持原样
```

### 临时目录管理

上传时可以指定临时目录用于存放加密文件：

```python
result = upload_folder(
    folder_path="./my_model",
    repo_id="demo/my-model",
    encryption_password="password",
    temp_dir="/tmp/encrypted_files",  # 指定临时目录
    username="your-username",
    password="your-password",
)
# 如果不指定 temp_dir，会自动创建临时目录并在上传后清理
```

## ⚙️ 配置

### 环境变量

```bash
# Hub 服务端点
export MOHA_ENDPOINT="https://your-hub-url.com"

# 认证信息（可选，避免每次输入）
export MOHA_USERNAME="your-username"
export MOHA_PASSWORD="your-password"
export MOHA_TOKEN="your-token"

# 加密密码（可选）
export MOHA_ENCRYPTION_PASSWORD="your-encryption-password"
```

## 🖥️ 命令行工具 (CLI)

SDK 提供了 `moha` 命令行工具，支持常见的上传下载操作。

### 基本用法

```bash
moha --help
```

### 上传文件夹

```bash
# 基本用法
moha upload-folder ./my_model org/my-model

# 使用别名 upload
moha upload ./my_model org/my-model

# 完整参数示例
moha upload ./my_model org/my-model \
    --repo-type models \
    --revision main \
    --message "Upload model files" \
    --ignore "*.log" \
    --ignore ".git*" \
    --username your-username \
    --password your-password

# 启用加密（默认使用 AES）
moha upload ./my_model org/my-model \
    --encrypt \
    --encryption-password "your-secret" \
    --username your-username \
    --password your-password

# 使用 SM4 国密算法加密
moha upload ./my_model org/my-model \
    --encrypt \
    --encryption-password "your-secret" \
    --algorithm SM4 \
    --username your-username \
    --password your-password
```

### 上传单个文件

```bash
# 基本用法（使用文件名作为仓库路径）
moha upload-file ./config.yaml org/my-model

# 指定仓库中的路径
moha upload-file ./config.yaml org/my-model \
    --path-in-repo configs/config.yaml

# 完整参数示例
moha upload-file ./model.safetensors org/my-model \
    --path-in-repo weights/model.safetensors \
    --repo-type models \
    --revision main \
    --message "Upload model weights" \
    --encrypt \
    --encryption-password "your-secret" \
    --username your-username \
    --password your-password
```

### 下载仓库

```bash
# 基本用法
moha download org/my-model

# 使用别名 download-repo
moha download-repo org/my-model

# 完整参数示例
moha download org/my-model \
    --local-dir ./downloaded_model \
    --repo-type models \
    --revision main \
    --include "*.safetensors" \
    --include "*.json" \
    --ignore "*.log" \
    --username your-username \
    --password your-password
```

### 下载单个文件

```bash
# 基本用法
moha download-file org/my-model config.yaml

# 完整参数示例
moha download-file org/my-model model.safetensors \
    --local-dir ./downloads \
    --repo-type models \
    --revision main \
    --username your-username \
    --password your-password
```

### CLI 参数说明

| 参数 | 说明 | 适用命令 |
|------|------|----------|
| `--repo-type, -t` | 仓库类型：`models` 或 `datasets`（默认：models） | 所有 |
| `--revision, -r` | 分支/标签/提交（默认：main） | 所有 |
| `--base-url` | API 基础 URL（默认：环境变量 MOHA_ENDPOINT） | 所有 |
| `--token` | 认证令牌 | 所有 |
| `--username` | 用户名 | 所有 |
| `--password` | 密码 | 所有 |
| `--message, -m` | 提交消息 | upload, upload-file |
| `--ignore, -i` | 忽略模式（可多次使用） | upload, download |
| `--include` | 包含模式（可多次使用） | download |
| `--encrypt, -e` | 启用加密 | upload, upload-file |
| `--encryption-password` | 加密密码 | upload, upload-file |
| `--algorithm, -a` | 加密算法：`AES` 或 `SM4`（默认：AES） | upload, upload-file |
| `--path-in-repo, -p` | 仓库中的文件路径 | upload-file |
| `--temp-dir` | 加密临时目录 | upload |
| `--local-dir, -o` | 本地保存目录 | download, download-file |
| `--quiet, -q` | 禁用进度条 | download, download-file |

### 使用环境变量

可以通过环境变量设置认证信息，避免每次输入：

```bash
# 设置环境变量
export MOHA_USERNAME="your-username"
export MOHA_PASSWORD="your-password"
export MOHA_ENCRYPTION_PASSWORD="your-secret"

# 然后直接使用命令
moha upload ./my_model org/my-model --encrypt
moha download org/my-model
```

## 📋 使用场景

### 场景 1: 上传开源模型到私有 Hub

```python
from xiaoshiai_hub import upload_folder

# 上传 Hugging Face 下载的模型到私有 Hub
result = upload_folder(
    folder_path="~/.cache/huggingface/hub/models--meta-llama--Llama-2-7b-hf",
    repo_id="myorg/llama-2-7b",
    repo_type="models",
    commit_message="Upload Llama 2 7B model",
    username="your-username",
    password="your-password",
)
```

### 场景 2: 加密上传敏感模型

```python
from xiaoshiai_hub import upload_folder

# 上传模型并加密大文件
result = upload_folder(
    folder_path="./proprietary-model",
    repo_id="myorg/proprietary-model",
    encryption_password="super-secret-password",  # 大文件自动加密
    ignore_patterns=["*.log", "checkpoints/"],
    username="your-username",
    password="your-password",
)
```

### 场景 3: 批量下载数据集

```python
from xiaoshiai_hub import snapshot_download

# 下载整个数据集
dataset_path = snapshot_download(
    repo_id="myorg/my-dataset",
    repo_type="datasets",
    allow_patterns=["*.parquet", "*.json"],  # 只下载数据文件
    ignore_patterns=["*.md"],  # 忽略文档
    username="your-username",
    password="your-password",
)
```

### 场景 4: 检查仓库是否存在

```python
from xiaoshiai_hub import HubClient
from xiaoshiai_hub.exceptions import RepositoryNotFoundError

client = HubClient(username="your-username", password="your-password")

try:
    repo_info = client.get_repository_info("myorg", "models", "my-model")
    print(f"仓库存在: {repo_info.name}")
except RepositoryNotFoundError:
    print("仓库不存在，请先创建")
```


## ⚠️ 重要说明

### 仓库必须先创建

在上传文件或文件夹之前，必须先在 Hub 上创建仓库。SDK 会自动检查仓库是否存在：

```python
from xiaoshiai_hub import upload_file
from xiaoshiai_hub.exceptions import RepositoryNotFoundError

try:
    result = upload_file(
        path_file="./model.bin",
        path_in_repo="model.bin",
        repo_id="myorg/my-model",
        username="your-username",
        password="your-password",
    )
except RepositoryNotFoundError as e:
    print(f"错误: {e}")
    print("请先在 Hub 上创建仓库")
```

### 加密文件的大小和类型限制

只有满足以下条件的文件才会被加密：

1. **文件大小** ≥ 5MB
2. **文件扩展名**为：`.safetensors`、`.bin`、`.pt`、`.pth`、`.ckpt`

其他文件保持原样，不会被加密。

### 临时文件清理

使用 `encryption_password` 时，SDK 会创建临时目录存放加密文件。上传完成后会自动清理，但如果上传失败，可能需要手动清理临时目录。

## 🔧 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/poxiaoyun/moha-sdk.git
cd moha-sdk

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 🤝 贡献

欢迎贡献！请随时提交 Issue 或 Pull Request。

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 Apache 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件

## 💬 支持

如有问题或需要帮助，请：

1. 查看文档和示例
2. 搜索或创建 [Issue](https://github.com/poxiaoyun/moha-sdk/issues)
3. 联系维护者
