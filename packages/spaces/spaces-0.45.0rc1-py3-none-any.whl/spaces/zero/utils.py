"""
"""
from __future__ import annotations

import base64
import ctypes
import json
import os
import stat
import shutil
import traceback
from functools import cache
from pathlib import Path
import requests_unixsocket
from urllib.parse import quote
from uuid import uuid4
from typing import Any

from ..config import ZEROGPU_HOME
from ..config import Config
from ..utils import debug


CLEANUPS_BASE_DIR = ZEROGPU_HOME / 'cleanups'


def register_cleanup(pid: int, target_dir: Path):
    cleanups_dir = CLEANUPS_BASE_DIR / f'{pid}'
    cleanups_dir.mkdir(parents=True, exist_ok=True)
    cleanup = cleanups_dir / f'{uuid4()}'
    cleanup.symlink_to(target_dir, target_is_directory=True)


def apply_cleanups(pid: int):
    cleanups_dir = CLEANUPS_BASE_DIR / f'{pid}'
    try:
        targets = [cleanup.readlink() for cleanup in cleanups_dir.iterdir()]
    except FileNotFoundError:
        return
    for target in targets:
        shutil.rmtree(target, ignore_errors=True)
    shutil.rmtree(cleanups_dir, ignore_errors=True)


@cache
def self_cgroup_device_path() -> str:
    cgroup_socket = Config.cgroup_socket
    if cgroup_socket:
        if os.path.exists(cgroup_socket):
            mode = os.stat(cgroup_socket).st_mode
            if stat.S_ISSOCK(mode):
                debug(f"Getting cgroup path through the unix socket {cgroup_socket}")
                try:
                    encoded_path = quote(cgroup_socket, safe="")
                    session = requests_unixsocket.Session()
                    url = f"http+unix://{encoded_path}/"  # endpoint path after /
                    response = session.get(url)
                    if response.status_code == 200:
                        cgroup_path = response.text.strip()
                        debug(f"Cgroup path {cgroup_path} returned from service")
                        return cgroup_path
                    else:
                        debug(f"Error from socket service {response.status_code}: {response.text}")
                except Exception as e:
                    print(f"Error getting cgroup path from socket, falling back to legacy method: {e}")
                    traceback.print_exc()
            else:
                debug(f"{cgroup_socket} exists but is NOT a socket.")
        else:
            debug(f"Specified socket path {cgroup_socket} not found")
    return self_cgroup_device_path_legacy()


def self_cgroup_device_path_legacy() -> str:
    # Cgroup v1 and v2 compatible, for v1 return the devices subsystem cgroup
    debug("Calling the legacy method to get the cgroup path")
    cgroup_content = Path(Config.zerogpu_proc_self_cgroup_path).read_text()
    lines = []
    for line in cgroup_content.splitlines():
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
    if len(lines) > 1:
        # cgroup v1, return the devices cgroup
        for line in lines:
            contents = line.split(':devices:')
            if len(contents) != 2:
                continue  # pragma: no cover
            return contents[1]
        raise Exception  # pragma: no cover
    elif len(lines) == 1:
        # cgroup v2
        line = lines[0]
        if not line.startswith("0::"):
            msg = f"Unexpected cgroup path line {line}"
            raise Exception(msg)
        return line.removeprefix('0::')
    else:
        raise Exception("No content in cgroup path")


def malloc_trim():
    ctypes.CDLL("libc.so.6").malloc_trim(0)


def jwt_payload(token: str) -> dict[str, Any]:
    _, payload, _ = token.split('.')
    return json.loads(base64.urlsafe_b64decode(f'{payload}=='))
