"""Checks the profile README's structure, images, links and privacy boundaries."""
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    require(data[:8] == b"\x89PNG\r\n\x1a\n", f"{path.name} is not a PNG")
    return struct.unpack(">II", data[16:24])


# Every image the README references exists, in a light and a dark version at 2x.
images = set(re.findall(r'(?:src|srcset)="\./(assets/[^"]+)"', README))
for name in ("hero", "chapters", "receiptcal", "manifest", "openmedia"):
    for theme in ("light", "dark"):
        require(f"assets/{name}-{theme}.png" in images, f"README does not use {name}-{theme}.png")
for image in images:
    path = ROOT / image
    require(path.is_file(), f"missing image: {image}")
    require(png_size(path)[0] >= 1200, f"{image} is not rendered at 2x")
    require(path.stat().st_size < 600_000, f"{image} is too large")

# Every image has descriptive alt text.
for alt in re.findall(r'alt="([^"]*)"', README):
    require(len(alt) >= 40, f"alt text too short: {alt!r}")

for heading in ("Three products. Less friction.", "Tools engineers use every day.", "Ideas from the work, and beyond.", "Let’s talk."):
    require(heading in README, f"missing section: {heading}")

for destination in (
    "https://receiptcal.com",
    "https://manifeststartup.com/home",
    "https://openmedia.site",
    "https://github.com/mihirkavi/open-media",
    "https://www.mihirkavishwar.com/blogs",
    "https://cal.com/mihirkavishwar/30min",
    "mailto:hello@mihirkavishwar.com",
):
    require(destination in README, f"missing destination: {destination}")

# Rate-limited third-party widgets break; keep them out.
for host in ("vercel.app", "herokuapp.com", "komarev.com", "readme-typing-svg"):
    require(host not in README, f"unreliable widget host: {host}")

# Privacy: customer names, internal figures and immigration details stay out of the public profile.
source = README + (ROOT / "assets" / "source" / "banners.html").read_text(encoding="utf-8")
for term in ("Apple Inc", "supporting Apple", "visa", "immigration", "GPA", "revenue", "$"):
    require(term not in source, f"private detail in public profile: {term}")

print("Profile README validation passed")
