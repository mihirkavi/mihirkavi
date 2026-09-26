from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


require((ROOT / "assets" / "profile-hero.svg").is_file(), "missing branded hero")
require((ROOT / "assets" / "impact-strip.svg").is_file(), "missing impact strip")

hero_root = ET.parse(ROOT / "assets" / "profile-hero.svg").getroot()
label_pill = next(
    element
    for element in hero_root
    if element.tag.endswith("rect") and element.attrib.get("x") == "88" and element.attrib.get("y") == "63"
)
require(float(label_pill.attrib["width"]) >= 310, "hero eyebrow label lacks right-side padding")

require("github-readme-stats-sigma-five.vercel.app" not in README, "unreliable stats provider remains")
require("github-readme-streak-stats.herokuapp.com" not in README, "unreliable streak provider remains")
require("github-readme-activity-graph.vercel.app" not in README, "unreliable activity provider remains")

for heading in (
    "About",
    "Ventures",
    "Tech & Tools",
    "MathWorks Engineering Work",
    "From the Blog",
    "GitHub Activity",
):
    require(heading in README, f"missing section: {heading}")

for destination in (
    "https://receiptcal.com",
    "https://manifeststartup.com/home",
    "https://github.com/mihirkavi/open-media",
    "https://www.mihirkavishwar.com/blogs",
    "mailto:hello@mihirkavishwar.com",
):
    require(destination in README, f"missing destination: {destination}")

print("Profile README validation passed")