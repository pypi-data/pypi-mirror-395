"""
信封加密核心模块

实现基于 AES-256-CTR 的信封加密/解密逻辑。
支持随机访问和流式解密，适合大文件部分读取场景。

信封加密文件格式:
- 前 4 字节: 元数据长度 (big-endian)
- 元数据: JSON 格式，包含 encryptedKey 和 password
- 16 字节: IV (用于 AES-256-CTR)
- 剩余部分: 加密后的文件内容
"""

import io
import os
import json
from dataclasses import dataclass
from pathlib import Path
import shutil
import tempfile
from typing import Optional, Union

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# IV 长度 (AES-256-CTR)
IV_SIZE = 16
# 元数据长度字段大小
METADATA_LENGTH_SIZE = 4
CHUNK_SIZE = 64 * 1024  # 64KB chunks

@dataclass
class DataKey:
    """数据密钥对象，包含明文密钥和加密后的密钥"""
    plaintext_key: bytes  # 明文密钥（32字节，用于 AES-256）
    encrypted_key: str 

def _raw_open(path, mode="rb"):
    """
    获取原始的文件句柄，绕过 decrypt_patch 的 hook。

    使用 io.FileIO 直接访问文件系统，不经过 builtins.open。
    """
    # io.FileIO 是底层实现，不会被 builtins.open 的 hook 影响
    file_io = io.FileIO(path, mode.replace("b", ""))
    if "b" in mode:
        return io.BufferedReader(file_io) if "r" in mode else io.BufferedWriter(file_io)
    return file_io


def create_aes_ctr_cipher(key: bytes, iv: bytes):
    """创建 AES-256-CTR cipher"""
    return Cipher(
        algorithms.AES(key),
        modes.CTR(iv),
        backend=default_backend()
    )


@dataclass
class EnvelopeMetadata:
    """加密文件元数据"""
    encrypted_key: str   # 加密后的数据密钥（Base64）
    password: str        # 用于解密 DEK 的密码

    def to_bytes(self) -> bytes:
        """序列化为 JSON 字节"""
        return json.dumps({
            "encryptedKey": self.encrypted_key,
            "password": self.password
        }).encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> "EnvelopeMetadata":
        """从 JSON 字节反序列化"""
        obj = json.loads(data.decode("utf-8"))
        return cls(
            encrypted_key=obj["encryptedKey"],
            password=obj["password"]
        )


def _envelope_encrypt_file(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    password: str,
    data_key: DataKey,
) -> None:
    """
    使用信封加密对文件进行加密 (AES-256-CTR)

    Args:
        input_path: 明文文件路径
        output_path: 加密文件输出路径
        password: 用于 KMS 密钥派生的密码
        kms_client: KMS 客户端实例（可选，不提供则使用默认客户端）
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    iv = os.urandom(IV_SIZE)
    cipher = create_aes_ctr_cipher(data_key.plaintext_key, iv)
    encryptor = cipher.encryptor()
    with _raw_open(input_path, "rb") as f:
        plaintext = f.read()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    metadata = EnvelopeMetadata(
        encrypted_key=data_key.encrypted_key,
        password=password
    )
    metadata_bytes = metadata.to_bytes()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with _raw_open(output_path, "wb") as f:
        f.write(len(metadata_bytes).to_bytes(METADATA_LENGTH_SIZE, "big"))
        f.write(metadata_bytes)
        f.write(iv)
        f.write(ciphertext)
    del data_key.plaintext_key


def envelope_enc_file(
    source: Union[Path, str],
    *,
    password: str,
    data_key: DataKey,
    dest: Optional[Union[Path, str]] = None,
    replace: bool = False,
    chunked: bool = True,
    chunk_size: int = CHUNK_SIZE,  # 默认 64KB，与 envelope_crypto 一致
) -> Path:
    """使用信封加密模式加密单个文件 (AES-256-CTR)。

    信封加密使用 KMS 服务生成数据密钥，数据密钥用于加密文件内容，
    加密后的数据密钥存储在文件头部。

    Args:
        source: 源文件路径
        password: 用于 KMS 密钥派生的密码
        dest: 目标文件路径（默认添加 .encrypted 后缀）
        replace: 是否原地加密（替换原文件）
        chunked: 是否使用流式加密（适用于大文件，减少内存占用）
        chunk_size: 流式加密时每次处理的块大小

    Returns:
        加密后的文件路径
    """
    src = Path(source)
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"Source file not found: {src}")

    # 确定输出路径
    if replace:
        dst = _make_temp_path(src.parent, ".encrypted.tmp")
    elif dest:
        dst = Path(dest)
    else:
        dst = src.with_suffix(src.suffix + ".encrypted")

    dst.parent.mkdir(parents=True, exist_ok=True)

    if chunked:
        _envelope_encrypt_file_streaming(src, dst, password, data_key, chunk_size)
    else:
        _envelope_encrypt_file(src, dst, password, data_key)

    # 替换模式：移动加密文件到原位置
    if replace:
        shutil.move(str(src), str(dst))
        return src

    return dst

def _make_temp_path(parent: Path, suffix: str) -> Path:
    """创建临时文件路径（使用 mkstemp 避免竞态条件）"""
    fd, path = tempfile.mkstemp(suffix=suffix, dir=parent)
    os.close(fd)
    return Path(path)





def _envelope_encrypt_file_streaming(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    password: str,
    data_key: DataKey,
    chunk_size: int = CHUNK_SIZE,
) -> None:
    """
    使用信封加密对大文件进行流式加密 (AES-256-CTR)

    AES-CTR 模式天然支持流式加密，不需要将整个文件加载到内存。
    加密后的文件格式与普通模式完全相同，可以用普通模式解密。

    Args:
        input_path: 明文文件路径
        output_path: 加密文件输出路径
        password: 用于 KMS 密钥派生的密码
        kms_client: KMS 客户端实例
        chunk_size: 每次读取的块大小
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    iv = os.urandom(IV_SIZE)
    metadata = EnvelopeMetadata(
        encrypted_key=data_key.encrypted_key,
        password=password
    )
    metadata_bytes = metadata.to_bytes()
    cipher = create_aes_ctr_cipher(data_key.plaintext_key, iv)
    encryptor = cipher.encryptor()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with _raw_open(input_path, "rb") as fin, _raw_open(output_path, "wb") as fout:
        # 写入元数据
        fout.write(len(metadata_bytes).to_bytes(METADATA_LENGTH_SIZE, "big"))
        fout.write(metadata_bytes)
        # 写入 IV
        fout.write(iv)

        # 流式加密
        while True:
            chunk = fin.read(chunk_size)
            if not chunk:
                break
            encrypted_chunk = encryptor.update(chunk)
            fout.write(encrypted_chunk)

        # 完成加密
        final = encryptor.finalize()
        if final:
            fout.write(final)

    del data_key.plaintext_key

