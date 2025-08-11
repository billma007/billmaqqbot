#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import traceback
from bot_debug import info,success,warning,error
import socket
import json
from save_settings import get_value
from bot_checkdata import pause_ter
import re
from typing import Any, Union
info("开始初始化监听端口...")
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    ListenSocket.bind((get_value("ip"), get_value("listen")))
except OSError:
    error("通常每个套接字地址只能使用一次")
    warning("检测到端口冲突，请检查本软件是否已经启动过；如果没有，请修改settings.json的listen数字（随机4位数），再打开go-cqhttp的config.yml拉到最底下的url的数字改成相同数字。")
    pause_ter()
    os._exit(0x0)
ListenSocket.listen(100)
success("成功初始化监听端口：http://"+(str(get_value("ip"))+":"+str(get_value("listen"))))


HttpResponseHeader = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'

def http_request_to_json(raw: Union[str, bytes]) -> Any:
    """
    将包含 HTTP 请求行、头部和（可能为 chunked）的消息体的原始字符串解析为 JSON 对象。
    仅需传入一次完整请求文本（如从 socket 累积读取到的字符串）。
    """
    if isinstance(raw, bytes):
        # 尽量不破坏原始字节；后续 JSON 为 UTF-8，常见场景下 OK
        raw = raw.decode('utf-8', errors='replace')

    # --- 定位头/体分界 ---
    # 既兼容 \r\n\r\n 也兼容 \n\n
    sep = '\r\n\r\n' if '\r\n\r\n' in raw else '\n\n'
    parts = raw.split(sep, 1)
    headers_text = parts[0]
    body_text = parts[1] if len(parts) > 1 else ''

    headers_lower = headers_text.lower()

    # --- 根据传输编码解码消息体 ---
    if 'transfer-encoding' in headers_lower and 'chunked' in headers_lower:
        body = _decode_chunked_body(body_text)
    elif 'content-length' in headers_lower:
        m = re.search(r'content-length\s*:\s*(\d+)', headers_text, re.I)
        if not m:
            # 没有找到长度，退化为直接尝试解析
            body = body_text.strip()
        else:
            length = int(m.group(1))
            # 这里以字符长度近似字节长度（JSON 为 ASCII/UTF-8 时等价）
            body = body_text[:length]
    else:
        # 无明确长度与编码时，直接取余下内容尝试解析
        body = body_text.strip()

    # --- 尝试 JSON 解析，失败则做兜底剪裁 ---
    obj = _loads_json_safely(body)
    return obj


def _decode_chunked_body(s: str) -> str:
    """
    解析 HTTP chunked 编码消息体，返回合并后的原始正文字符串。
    允许前置空行；严格按照 “size CRLF data CRLF … 0 CRLF CRLF” 解码。
    """
    i = 0
    n = len(s)
    # 跳过可能的前置空白/空行
    while i < n and s[i] in ('\r', '\n', ' '):
        i += 1

    chunks = []
    while True:
        # 读取 chunk size 行（到换行符）
        j = s.find('\n', i)
        if j == -1:
            # 找不到 size 行，视为异常；尽量返回已解析部分
            break
        size_line = s[i:j].strip()   # 可能包含 \r，strip 会去掉
        size_str = size_line.split(';', 1)[0]  # 兼容 "a3f;extension"
        try:
            size = int(size_str, 16)
        except ValueError:
            # 非法 size：终止并返回已解析部分
            break

        i = j + 1  # 跳过 size 行的换行

        if size == 0:
            # 读到终止块；规范上后面可能还有 trailer 与空行，这里忽略
            break

        # 读取 size 个字符（UTF-8/ASCII JSON 时与字节数等价）
        if i + size > n:
            # 数据不完整，尽量取到结尾
            data = s[i:n]
            chunks.append(data)
            i = n
            break
        else:
            data = s[i:i + size]
            chunks.append(data)
            i += size

        # 吃掉块数据后的 CRLF（如果存在）
        if i < n and s[i] == '\r':
            i += 1
        if i < n and s[i] == '\n':
            i += 1

    return ''.join(chunks)


def _loads_json_safely(body: str) -> Any:
    """
    先直接 json.loads；失败则截取第一个 '{' 到最后一个 '}' 的子串再尝试。
    仍失败则抛出原始异常，便于上层定位问题。
    """
    body_strip = body.strip()
    try:
        return json.loads(body_strip)
    except json.JSONDecodeError:
        # 兜底：去掉非 JSON 杂质（如多余的 0、额外日志）
        start = body_strip.find('{')
        end = body_strip.rfind('}')
        if start != -1 and end != -1 and end >= start:
            candidate = body_strip[start:end + 1]
            return json.loads(candidate)
        # 若仍失败，抛出以便调用者捕获
        raise

def rev_msg():# json or None
    try:
        Client, Address = ListenSocket.accept()
        Request = Client.recv(8192).decode(encoding='utf-8')
        rev_json=http_request_to_json(Request)
        Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
        Client.close()
        #print("收到信息：",rev_json)
        return rev_json
    except:
        traceback.print_exc()

if __name__=="__main__":
    while True:
        print(rev_msg())
        