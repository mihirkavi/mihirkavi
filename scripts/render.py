"""Render the README images from assets/source/banners.html with headless Chromium.

Usage: python3 scripts/render.py [path-to-chrome]
Writes assets/<id>-<theme>.png at 2x for the light and dark themes.
"""
import glob
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "banners.html"
SIZES = {"hero": (1280, 600), "chapters": (1280, 560), "receiptcal": (600, 600), "manifest": (600, 600), "openmedia": (600, 600)}


def find_chrome() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    candidates = glob.glob(os.path.expanduser("~/Library/Caches/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell"))
    candidates.append("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    for candidate in sorted(candidates, reverse=True):
        if os.path.exists(candidate):
            return candidate
    raise SystemExit("No Chromium found; pass its path as the first argument.")


def main() -> None:
    chrome = find_chrome()
    for name, (width, height) in SIZES.items():
        for theme in ("light", "dark"):
            out = ROOT / "assets" / f"{name}-{theme}.png"
            subprocess.run([chrome, "--headless", "--hide-scrollbars", "--default-background-color=00000000", "--force-device-scale-factor=2",
                            f"--window-size={width},{height}", "--virtual-time-budget=4000",
                            f"--screenshot={out}", f"{SOURCE.as_uri()}#{name}-{theme}"],
                           check=True, capture_output=True)
            print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
