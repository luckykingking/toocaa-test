"""Download the official, explicitly recorded site images without altering them."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
IMAGES = json.loads((ROOT / "content/images.json").read_text(encoding="utf-8"))
TARGET = ROOT / "docs/assets/images"


def download(item):
    name, url = item
    request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "image/jpeg,image/png"})
    with urlopen(request, timeout=40) as response:
        if not response.headers.get_content_type().startswith("image/"):
            raise ValueError(f"Not an image: {url}")
        payload = response.read()
    (TARGET / name).write_bytes(payload)
    return f"{name}: {len(payload)} bytes"


if __name__ == "__main__":
    TARGET.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(download, IMAGES.items()):
            print(result)
