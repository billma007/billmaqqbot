import os
import tempfile
import time
import json
import zipfile
import io
from pathlib import Path

import requests

API_BASE = "https://api.github.com"
API_VERSION = "2022-11-28"  # 固定一个稳定版号

# def load_config(path: str) -> dict:
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)

def gh_session(token: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
    })
    return s

def dispatch_workflow(sess: requests.Session, owner: str, repo: str, workflow_file: str, ref: str, inputs: dict):
    url = f"{API_BASE}/repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches"
    payload = {"ref": ref, "inputs": inputs or {}}
    r = sess.post(url, json=payload, timeout=30)
    r.raise_for_status()  # 成功返回 204
    return True

def find_latest_run(sess: requests.Session, owner: str, repo: str, workflow_file: str, ref: str,
                    timeout_sec: int, interval_sec: int):
    """ 查找最新的一次由 workflow_dispatch 触发、且 head_branch 为 ref 的 run。 """
    url = f"{API_BASE}/repos/{owner}/{repo}/actions/workflows/{workflow_file}/runs"
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        params = {"event": "workflow_dispatch", "branch": ref, "per_page": 10}
        r = sess.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        runs = data.get("workflow_runs", []) or []
        # GitHub 返回通常按创建时间倒序；取第一个分支匹配的
        for run in runs:
            if run.get("head_branch") == ref:
                return int(run["id"]), run.get("html_url")
        time.sleep(interval_sec)
    raise TimeoutError("未在预期时间内找到刚触发的 workflow run，请到 Actions 页面核对。")

def wait_run_completed(sess: requests.Session, owner: str, repo: str, run_id: int,
                       timeout_sec: int, interval_sec: int):
    url = f"{API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}"
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        r = sess.get(url, timeout=30)
        r.raise_for_status()
        run = r.json()
        status = run.get("status")        # queued / in_progress / completed
        conclusion = run.get("conclusion")  # success / failure / cancelled / ...
        if status == "completed":
            return conclusion
        time.sleep(interval_sec)
    raise TimeoutError("等待工作流完成超时。")

def download_artifact(sess: requests.Session, owner: str, repo: str, run_id: int,
                      artifact_name: str, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    # 列出 run 下的 artifacts
    url = f"{API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
    r = sess.get(url, timeout=60)
    r.raise_for_status()
    artifacts = r.json().get("artifacts", []) or []

    target = None
    if artifact_name:
        for a in artifacts:
            if a.get("name") == artifact_name:
                target = a
                break
    if target is None:
        if len(artifacts) == 1:
            target = artifacts[0]
        else:
            names = [a.get("name") for a in artifacts]
            raise RuntimeError(f"未找到名为 {artifact_name!r} 的 artifact；当前可用：{names}")

    art_id = target["id"]
    dl = sess.get(f"{API_BASE}/repos/{owner}/{repo}/actions/artifacts/{art_id}/zip", timeout=300)
    dl.raise_for_status()

    # 解压 zip（artifact 外层）
    zf = zipfile.ZipFile(io.BytesIO(dl.content))
    saved = []
    for m in zf.namelist():
        fn = Path(m).name  # 忽略路径层级，直接平铺保存
        out = out_dir / fn
        with zf.open(m) as src, open(out, "wb") as dst:
            dst.write(src.read())
        saved.append(out)
    return saved
import os
import requests

ONEBOT_API_URL = "http://127.0.0.1:3000"

def upload(nameit: str, groupnumber: int):
    """
    使用 OneBot v11 标准 API 向指定群发送文件

    :param nameit: 文件名（相对路径 jmdownloads/{nameit}）
    :param groupnumber: 群号（int）
    """
    file_path = os.path.join("jmdownloads", nameit)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # OneBot send_group_file API
    url = f"{ONEBOT_API_URL}/upload_group_file"

    payload = {
        "group_id": groupnumber,
        "file": os.path.abspath(file_path),  # 转为绝对路径
        "name": nameit                       # 群内显示的文件名
    }

    # 发送请求
    resp = requests.post(url, json=payload)
    resp.raise_for_status()  # 检查 HTTP 状态

    data = resp.json()
    if data.get("status") != "ok":
        raise RuntimeError(f"发送失败: {data}")

    return data
from pathlib import Path

def delete_download_file(nameit: str, base_dir: str = "jmdownloads", missing_ok: bool = False) -> bool:
    """
    删除相对路径为 `jmdownloads/{nameit}` 的本地文件（或指向文件的符号链接）。

    参数：
    - nameit:    目标文件名或相对子路径（例如 "本子.zip" 或 "subdir/本子.zip"）
    - base_dir:  根目录，默认 "jmdownloads"
    - missing_ok:若目标不存在，True 则静默返回 False；False 则抛 FileNotFoundError

    返回：
    - 成功删除返回 True；当 missing_ok=True 且文件不存在时返回 False。

    可能抛出：
    - FileNotFoundError: 目标不存在（且 missing_ok=False）
    - IsADirectoryError: 目标是目录（为安全起见不删除）
    - PermissionError:   无权限
    - ValueError:        目标不在 base_dir 内（疑似路径穿越）
    """
    base = Path(base_dir).resolve()
    target = (base / nameit).resolve()

    # 防路径穿越：确保目标仍在 base 目录下
    if not target.is_relative_to(base):
        raise ValueError(f"拒绝删除越界路径：{target}")

    if not target.exists():
        if missing_ok:
            return False
        raise FileNotFoundError(f"文件不存在：{target}")

    # 仅允许删除文件或符号链接
    if target.is_dir() and not target.is_symlink():
        raise IsADirectoryError(f"目标是目录，已拒绝删除：{target}")

    target.unlink()  # 对文件/符号链接有效
    return True
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, Union, List

import subprocess
import tempfile
from pathlib import Path
from typing import Union
import shutil
import os

def _find_7z() -> str:
    # 优先从 PATH 查找；其次检查常见安装路径
    candidates = [
        "7z", "7z.exe",
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
    ]
    for c in candidates:
        p = shutil.which(c) if "\\" not in c else (c if Path(c).exists() else None)
        if p:
            return p
    raise FileNotFoundError("未找到 7z 可执行文件，请安装 7-Zip 并将其加入 PATH。")

def reencrypt_zip_inplace_with_7z_sync(
    zip_path: Union[str, Path],
    password: str,
    *,
    method: str = "AES256"  # 也可用 'ZipCrypto'
) -> str:
    """
    将现有“明文 ZIP”重打包为**加密 ZIP**并覆盖原文件。
    - 同步阻塞直到 7z 完成（使用 subprocess.run(check=True)）
    - 覆盖前先写到同目录的临时文件，最后原子替换
    - 覆盖后用 `7z t` 进行一次校验（同样阻塞）
    """
    seven = _find_7z()
    zip_path = Path(zip_path).resolve()
    if not zip_path.exists():
        raise FileNotFoundError(zip_path)
    if method not in ("AES256", "ZipCrypto"):
        raise ValueError("method 仅支持 'AES256' 或 'ZipCrypto'")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # 1) 解压到临时目录（阻塞直至完成）
        cmd_x = [seven, "x", str(zip_path), f"-o{tmpdir}", "-y"]
        subprocess.run(cmd_x, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # 2) 重新加密打包到临时目标（阻塞直至完成）
        enc_tmp = zip_path.with_suffix(".zip.__enc_tmp__")
        # 注意：不要使用 shell=True 或 'start'，以避免异步
        cmd_a = [seven, "a", "-tzip", f"-p{password}", f"-mem={method}", str(enc_tmp), str(tmpdir / "*")]
        subprocess.run(cmd_a, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # 3) 覆盖原文件（原子替换）
        os.replace(enc_tmp, zip_path)

        # 4) 校验（阻塞直至完成；若密码不对或包未完成会非零退出）
        cmd_t = [seven, "t", str(zip_path), f"-p{password}"]
        subprocess.run(cmd_t, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    return str(zip_path)


def jm_main(_jmconfig,jmnumber,groupnumber):
    cfg = _jmconfig

    token = cfg.get("token") or os.getenv("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("缺少 token：请在 config.json 的 token 字段填写，或设置环境变量 GITHUB_TOKEN。")

    owner = cfg.get("owner", "billma007")
    repo = cfg.get("repo", "JMComic-Crawler-Python")
    workflow_file = cfg.get("workflow_file", "download_dispatch.yml")
    ref = cfg.get("ref", "master")
    inputs = cfg.get("inputs", {})
    out_dir = Path(cfg.get("output_dir", "downloads"))
    poll = cfg.get("poll", {})
    find_run_timeout = int(poll.get("find_run_timeout_sec", 180))
    find_run_interval = int(poll.get("find_run_interval_sec", 3))
    run_timeout = int(poll.get("run_timeout_sec", 7200))
    run_interval = int(poll.get("run_poll_interval_sec", 10))

    sess = gh_session(token)

    print(f"[1/4] 触发 workflow_dispatch：ref={ref}, inputs={inputs}")
    dispatch_workflow(sess, owner, repo, workflow_file, ref, inputs)
    print("[OK] 已发送（HTTP 204）")
    time.sleep(10)
    print("[2/4] 查找对应的 run ...")
    run_id, run_url = find_latest_run(sess, owner, repo, workflow_file, ref,
                                      timeout_sec=find_run_timeout, interval_sec=find_run_interval)
    print(f"[OK] run_id={run_id}\n     查看页面：{run_url}")
    print("[3/4] 等待运行完成 ...（视下载体量耗时较长）")
    conclusion = wait_run_completed(sess, owner, repo, run_id,
                                    timeout_sec=run_timeout, interval_sec=run_interval)
    print(f"[OK] conclusion={conclusion}")
    if conclusion != "success":
        raise RuntimeError("工作流未成功完成，请打开运行页面查看日志。")
    artifact_name = inputs.get("UPLOAD_NAME") #or "Click me to download"
    print(f"[4/4] 下载 artifact：{artifact_name!r}")
    files = download_artifact(sess, owner, repo, run_id, artifact_name, out_dir)
    print(f"[OK] 已保存至：{out_dir.resolve()}")
    for p in files:
        print(" -", p.name)
        reencrypt_zip_inplace_with_7z_sync(f"jmdownloads\\{jmnumber}.zip", password=jmnumber, method="ZipCrypto")
        #time.sleep(6)
        upload(f"{jmnumber}.zip", groupnumber)
        #delete_download_file(f"{p.name}")

import re

def only_digits(s: str, ascii_only: bool = True) -> str:
    """
    删除字符串中所有非数字字符，返回仅包含数字的字符串。

    :param s: 输入字符串
    :param ascii_only: True 时仅保留 ASCII 数字 0-9；False 时保留所有 Unicode 数字（使用 str.isdigit）
    :return: 仅包含数字的字符串（顺序与原字符串一致）
    """
    if ascii_only:
        # 仅保留 0-9
        return re.sub(r'[^0-9]', '', s)
    else:
        # 保留所有 Unicode 数字（例如 '٣٤٥'，上标 ² 等）
        return ''.join(ch for ch in s if ch.isdigit())
from pathlib import Path
import zipfile
import pyzipper
import shutil


def jm_out_main(jmnumber,groupnumber):
    jmnumber=only_digits(jmnumber)
    _jmconfig={
  "token": "YourAccessToken", 
  "owner": "YourGithubAccount",
  "repo": "JMComic-Crawler-Python",
  "workflow_file": "download_dispatch.yml",
  "ref": "master",
  "inputs": {
    "JM_ALBUM_IDS": jmnumber,
    "JM_PHOTO_IDS": "",
    "CLIENT_IMPL": "",
    "IMAGE_SUFFIX": "jpg",
    "DIR_RULE": "",
    "ZIP_NAME": f"{jmnumber}.zip",
    "UPLOAD_NAME": f"{jmnumber}.zip"
  },
  "output_dir": "jmdownloads",
  "poll": {
    "find_run_timeout_sec": 180,
    "find_run_interval_sec": 3,
    "run_timeout_sec": 7200,
    "run_poll_interval_sec": 10
  }
}
    jm_main(_jmconfig,jmnumber,groupnumber)
    return "下载成功"

if __name__ == "__main__":
    #jm_out_main()
    pass
