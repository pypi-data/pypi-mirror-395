"""
认证管理模块 - Token 的保存和读取
"""

import json
import os
from pathlib import Path
from typing import Optional, Tuple

import requests

from .client import DEFAULT_BASE_URL


# 默认 token 存储目录
DEFAULT_TOKEN_DIR = Path.home() / ".moha"
DEFAULT_TOKEN_FILE = "token.json"


def get_token_path(token_dir: Optional[str] = None) -> Path:
    """获取 token 文件路径"""
    if token_dir:
        return Path(token_dir) / DEFAULT_TOKEN_FILE
    return DEFAULT_TOKEN_DIR / DEFAULT_TOKEN_FILE


def save_token(
    token: str,
    base_url: Optional[str] = None,
    username: Optional[str] = None,
    token_dir: Optional[str] = None,
) -> Path:
    """
    保存 token 到文件
    
    Args:
        token: 认证令牌
        base_url: API 地址（可选，用于记录）
        username: 用户名（可选，用于记录）
        token_dir: token 存储目录（默认: ~/.moha）
    
    Returns:
        token 文件路径
    """
    token_path = get_token_path(token_dir)
    token_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "token": token,
    }
    if base_url:
        data["base_url"] = base_url
    if username:
        data["username"] = username
    
    with open(token_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 设置文件权限为仅用户可读写
    os.chmod(token_path, 0o600)
    
    return token_path


def load_token(token_dir: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    从文件加载 token
    
    Args:
        token_dir: token 存储目录（默认: ~/.moha）
    
    Returns:
        (token, base_url, username) 元组，如果文件不存在则返回 (None, None, None)
    """
    token_path = get_token_path(token_dir)
    
    if not token_path.exists():
        return None, None, None
    
    try:
        with open(token_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("token"), data.get("base_url"), data.get("username")
    except (json.JSONDecodeError, IOError):
        return None, None, None


def delete_token(token_dir: Optional[str] = None) -> bool:
    """
    删除 token 文件
    
    Args:
        token_dir: token 存储目录（默认: ~/.moha）
    
    Returns:
        是否成功删除
    """
    token_path = get_token_path(token_dir)
    
    if token_path.exists():
        token_path.unlink()
        return True
    return False


def login(
    username: str,
    password: str,
    base_url: Optional[str] = None,
    token_dir: Optional[str] = None,
) -> Tuple[str, Path]:
    """
    登录并保存 token
    
    Args:
        username: 用户名
        password: 密码
        base_url: API 地址
        token_dir: token 存储目录
    
    Returns:
        (token, token_path) 元组
    
    Raises:
        AuthenticationError: 认证失败
        requests.RequestException: 请求失败
    """
    from .exceptions import AuthenticationError
    
    base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base_url}/api/iam/login"
    
    try:
        response = requests.post(
            url,
            json={
                "username": username, 
                "type": "Password",
                "remeberMe": True,
                "password": {
                    "algorithm": "PlainText",
                    "value": password,
                },
            },
            timeout=30,
        )
        
        if response.status_code == 401:
            raise AuthenticationError("用户名或密码错误")
        
        response.raise_for_status()
        data = response.json()
        token = data.get("token") or data.get("access_token")
        
        if not token:
            raise AuthenticationError("服务器未返回 token")
        
        token_path = save_token(token, base_url, username, token_dir)
        return token, token_path
        
    except requests.RequestException as e:
        raise AuthenticationError(f"登录请求失败: {e}")

