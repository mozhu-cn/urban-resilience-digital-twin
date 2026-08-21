"""Download the portable pandoc binary (no pip needed) into tools/vendor/pandoc."""
import io
import json
import os
import zipfile

import requests

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")
DEST = os.path.join(VENDOR, "pandoc")
os.makedirs(DEST, exist_ok=True)

HEADERS = {"User-Agent": "pandoc-vendor/1.0"}


def main():
    # resolve latest release
    r = requests.get("https://api.github.com/repos/jgm/pandoc/releases/latest",
                     timeout=30, headers=HEADERS)
    r.raise_for_status()
    tag = r.json()["tag_name"]
    print("latest pandoc release:", tag)

    asset_url = None
    for a in r.json()["assets"]:
        name = a["name"]
        if name.startswith("pandoc-") and name.endswith("windows-x86_64.zip"):
            asset_url = a["browser_download_url"]
            print("asset:", name)
            break
    if not asset_url:
        raise RuntimeError("windows-x86_64.zip asset not found")

    print("downloading ...")
    zip_path = os.path.join(VENDOR, "pandoc.zip")
    for attempt in range(5):
        try:
            with requests.get(asset_url, timeout=60, headers=HEADERS, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                done = 0
                with open(zip_path, "wb") as fh:
                    for chunk in r.iter_content(chunk_size=1 << 16):
                        fh.write(chunk)
                        done += len(chunk)
                if total and done < total:
                    raise IOError(f"short read {done}/{total}")
                break
        except Exception as exc:  # noqa: BLE001
            print(f"  attempt {attempt+1} failed: {type(exc).__name__}; retrying")
            continue
    else:
        raise RuntimeError("download failed after retries")

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(DEST)
    os.remove(zip_path)
    exe = os.path.join(DEST, "pandoc.exe")
    # zip may nest the exe one level deep
    if not os.path.exists(exe):
        for root, _dirs, files in os.walk(DEST):
            if "pandoc.exe" in files:
                exe = os.path.join(root, "pandoc.exe")
                break
    print("pandoc ready at:", exe)


if __name__ == "__main__":
    main()
