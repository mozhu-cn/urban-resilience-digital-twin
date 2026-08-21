"""Manually vendor python-docx + lxml wheels (no pip needed).

Downloads the wheels from PyPI and extracts them into tools/vendor so that
docx generation works offline afterwards.
"""
import io
import json
import os
import sys
import zipfile

import requests

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")
os.makedirs(VENDOR, exist_ok=True)

HEADERS = {"User-Agent": "docx-vendor/1.0"}


def _ver_key(v):
    parts = []
    for x in v.replace("-", ".").split("."):
        try:
            parts.append(int(x))
        except ValueError:
            parts.append(0)
    return parts


def pick_wheel(pkg, want):
    r = requests.get(f"https://pypi.org/pypi/{pkg}/json", timeout=30, headers=HEADERS)
    r.raise_for_status()
    files = r.json()["releases"]
    # use the latest version's files
    versions = sorted(files.keys(), key=_ver_key)
    for ver in reversed(versions):
        for f in files[ver]:
            fn = f["filename"]
            if want(fn, ver):
                return f["url"], fn
    raise RuntimeError(f"no matching wheel for {pkg}")


def fetch_and_extract(url, fn):
    print(f"downloading {fn} ...")
    r = requests.get(url, timeout=120, headers=HEADERS)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(VENDOR)
    print(f"  extracted -> {VENDOR}")


def main():
    url, fn = pick_wheel("python-docx", lambda fn, v: fn.endswith("py3-none-any.whl"))
    fetch_and_extract(url, fn)

    # lxml: cp314 + win_amd64 (CPython 3.14 on Windows 64-bit; NOT free-threaded cp314t)
    url, fn = pick_wheel(
        "lxml", lambda fn, v: ("cp314" in fn and "cp314t" not in fn
                               and "win_amd64" in fn and fn.endswith(".whl")))
    fetch_and_extract(url, fn)

    # typing_extensions: pure python
    url, fn = pick_wheel("typing_extensions", lambda fn, v: fn.endswith("py3-none-any.whl"))
    fetch_and_extract(url, fn)

    print("vendor ready. test with:  PYTHONPATH=tools/vendor python -c \"import docx, lxml\"")


if __name__ == "__main__":
    main()
