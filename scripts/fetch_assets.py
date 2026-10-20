"""Download the official, explicitly recorded site images without altering them."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
IMAGES = json.loads((ROOT / "content/images.json").read_text(encoding="utf-8"))
TARGET = ROOT / "docs/assets/images"
UI_ASSETS = {
    "fonts/inter-tight.woff2": "https://www.toocaa.com/cdn/shop/files/inter-tight-latin-wght-normal.woff2?v=1789445385",
    "fonts/OFL.txt": "https://raw.githubusercontent.com/google/fonts/main/ofl/intertight/OFL.txt",
    "icons/LICENSE.txt": "https://raw.githubusercontent.com/lucide-icons/lucide/main/LICENSE",
    **{f"icons/{name}.svg": f"https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/{name}.svg" for name in ["search", "user-round", "shopping-bag"]},
}


def download(item):
    name, url = item
    request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "image/jpeg,image/png"})
    with urlopen(request, timeout=40) as response:
        if not response.headers.get_content_type().startswith("image/"):
            raise ValueError(f"Not an image: {url}")
        payload = response.read()
    (TARGET / name).write_bytes(payload)
    return f"{name}: {len(payload)} bytes"


def download_ui(item):
    name, url = item
    target = ROOT / "docs/assets" / name
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=40) as response:
        payload = response.read()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    return f"{name}: {len(payload)} bytes"


if __name__ == "__main__":
    TARGET.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(download, IMAGES.items()):
            print(result)
        for result in pool.map(download_ui, UI_ASSETS.items()):
            print(result)
