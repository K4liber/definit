# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow",
# ]
# ///

import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


def parse_svg_dimensions(path: str):
    try:
        root = ET.parse(path).getroot()
        width = root.attrib.get("width")
        height = root.attrib.get("height")
        viewbox = root.attrib.get("viewBox")

        if width and height:
            try:
                return float(width.rstrip("px")), float(height.rstrip("px"))
            except ValueError:
                pass

        if viewbox:
            parts = viewbox.split()
            if len(parts) == 4:
                try:
                    _, _, vb_w, vb_h = [float(p) for p in parts]
                    if vb_w and vb_h:
                        return vb_w, vb_h
                except ValueError:
                    pass
    except Exception:
        pass
    return None, None


def image_fit_style(
    path: str,
    default_max_height: int = 520,
    default_max_width: int = 900,
    portrait_factor: float = 0.9,
    slide_width: int = 1280,
    slide_height: int = 720,
):
    usable_width = slide_width - 120
    usable_height = slide_height - 120
    max_width_cap = min(default_max_width, usable_width)
    max_height_cap = min(default_max_height, usable_height)

    try:
        if path.lower().endswith(".svg"):
            width, height = parse_svg_dimensions(path)
            if width and height:
                ratio = width / height if height else 1.0
                if ratio >= 1.0:
                    target_width = min(max_width_cap, int(max_height_cap * ratio))
                    target_height = int(target_width / ratio)
                else:
                    target_height = min(max_height_cap, int(max_width_cap * ratio))
                    target_width = int(target_height / ratio)
                return (
                    f' width="{max(20, int(target_width))}" height="{max(20, int(target_height))}"'
                    f' style="max-width:{max(20, int(target_width))}px; max-height:{max(20, int(target_height))}px; width:{max(20, int(target_width))}px; height:auto; object-fit:contain;"'
                )

        with Image.open(path) as img:
            width, height = img.size
    except Exception as e:
        print(f"Error occurred while opening image: {e}")
        return (
            f' width="{max_width_cap}" height="{max_height_cap}"'
            f' style="max-width:{max_width_cap}px; max-height:{max_height_cap}px; width:{max_width_cap}px; height:auto; object-fit:contain;"'
        )

    ratio = width / height if height else 1.0
    if ratio >= 1.6:
        target_width = min(max_width_cap, int(max_height_cap * ratio))
        target_height = int(target_width / ratio)
    elif ratio >= 1.0:
        target_height = min(int(max_height_cap * 0.9), max_height_cap)
        target_width = min(int(target_height * ratio), max_width_cap)
    elif ratio >= 0.7:
        target_height = min(int(max_height_cap * portrait_factor), max_height_cap)
        target_width = min(int(target_height * ratio), max_width_cap)
    else:
        target_height = min(int(max_height_cap * 0.8), max_height_cap)
        target_width = min(int(target_height * ratio), max_width_cap)

    return (
        f' width="{max(20, int(target_width))}" height="{max(20, int(target_height))}"'
        f' style="max-width:{max(20, int(target_width))}px; max-height:{max(20, int(target_height))}px; width:{max(20, int(target_width))}px; height:auto; object-fit:contain;"'
    )


def convert_scratch_to_marp(scratch_text: str) -> str:
    # Header with Marp theme and styles for custom layouts
    marp_header = """---
marp: true
theme: default
paginate: true
math: katex
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    padding: 30px 40px 20px 40px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 720px;
    box-sizing: border-box;
  }
  h1 { font-size: 2.2rem; margin-top: auto; margin-bottom: auto; text-align: center; }
  h2 { font-size: 1.8rem; margin-top: 0; margin-bottom: 10px; flex-shrink: 0; }
  
  .img-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 0;
    width: 100%;
    height: calc(100% - 55px);
    margin: 5px 0;
  }

  .grid-2x2 {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 12px;
    width: 100%;
    min-height: 0;
    height: calc(100% - 60px);
    margin: 5px 0;
  }
  .grid-2x2-item {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    min-height: 0;
    overflow: hidden;
  }
  .grid-2x2-item img {
    display: block;
    width: auto;
    max-width: 100%;
    max-height: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 6px;
  }

  .grid-1x2 {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    width: 100%;
    min-height: 0;
    height: calc(100% - 60px);
    margin: 5px 0;
  }
  .grid-1x2-item {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    min-height: 0;
    overflow: hidden;
  }
  .grid-1x2-item img {
    display: block;
    width: auto;
    max-width: 100%;
    max-height: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 6px;
  }

  .single-img-item {
    display: block;
    width: auto;
    max-width: 100%;
    max-height: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 6px;
  }

  .caption {
    font-size: 1.05rem;
    color: #333;
    text-align: center;
    width: 100%;
    margin-top: auto;
    padding-top: 6px;
    flex-shrink: 0;
  }
  .source {
    font-size: 0.8rem;
    color: #666;
    text-align: center;
    width: 100%;
    margin-top: 2px;
    flex-shrink: 0;
  }
---
"""

    slides = []
    # Split by level-1 or level-2 headers
    raw_slides = re.split(r"\n(?=#{1,2}\s)", scratch_text.strip())

    for raw in raw_slides:
        lines = raw.strip().splitlines()
        slide_lines = []
        notes = []
        captions = []
        sources = []
        images_pos = {}
        in_notes = False

        for line in lines:
            line_str = line.strip()

            # Speaker notes detection
            if line_str.startswith("Notes:"):
                in_notes = True
                continue
            if line_str.startswith("N: "):
                notes.append(line_str[3:])
                continue
            if in_notes:
                if line_str:
                    notes.append(line_str)
                continue

            # Captions & References
            if line_str.startswith("C: "):
                captions.append(line_str[3:])
                continue
            if line_str.startswith("S: ") or line_str.startswith("R: "):
                sources.append(line_str)
                continue

            # Positional image tags: ![ITL](path), ![IL](path), ![I](path)
            img_match = re.match(r"!\[(ITL|ITR|IBL|IBR|IL|IR|I)\]\((.*?)\)", line_str)
            if img_match:
                tag, path = img_match.groups()
                images_pos[tag] = path
                continue

            slide_lines.append(line)

        # Reconstruct image containers based on positional tags
        if any(k in images_pos for k in ["ITL", "ITR", "IBL", "IBR"]):
            grid_html = ['<div class="grid-2x2">']
            for tag in ["ITL", "ITR", "IBL", "IBR"]:
                if tag in images_pos:
                    img_path = images_pos[tag]
                    img_style = image_fit_style(
                        str(Path("presentation/pycon_wroclaw") / img_path.replace("./img/", "img/")),
                        default_max_height=230,
                        default_max_width=360,
                        slide_width=1280,
                        slide_height=720,
                    )
                    grid_html.append(f'  <div class="grid-2x2-item"><img src="{img_path}"{img_style} /></div>')
            grid_html.append("</div>")
            slide_lines.append("\n".join(grid_html))
        elif any(k in images_pos for k in ["IL", "IR"]):
            grid_html = ['<div class="grid-1x2">']
            for tag in ["IL", "IR"]:
                if tag in images_pos:
                    img_path = images_pos[tag]
                    img_style = image_fit_style(
                        str(Path("presentation/pycon_wroclaw") / img_path.replace("./img/", "img/")),
                        default_max_height=360,
                        default_max_width=500,
                        slide_width=1280,
                        slide_height=720,
                    )
                    grid_html.append(f'  <div class="grid-1x2-item"><img src="{img_path}"{img_style} /></div>')
            grid_html.append("</div>")
            slide_lines.append("\n".join(grid_html))
        elif "I" in images_pos:
            img_path = images_pos["I"]
            img_style = image_fit_style(
                str(Path("presentation/pycon_wroclaw") / img_path.replace("./img/", "img/")),
                default_max_height=520,
                default_max_width=860,
                slide_width=1280,
                slide_height=720,
            )
            slide_lines.append(
                f'<div class="img-container"><img class="single-img-item" src="{img_path}"{img_style} /></div>'
            )

        # Append captions & sources at the bottom
        for cap in captions:
            slide_lines.append(f'<div class="caption">{cap}</div>')
        for src in sources:
            slide_lines.append(f'<div class="source">{src}</div>')

        # Append presenter notes
        if notes:
            slide_lines.append(f"\n<!--\n{chr(10).join(notes)}\n-->")

        slides.append("\n".join(slide_lines))

    return marp_header + "\n\n---\n\n".join(slides)


if __name__ == "__main__":
    src = Path("presentation/pycon_wroclaw/slides_scratch.md")
    out_md = Path("presentation/pycon_wroclaw/slides_marp.md")
    out_pdf = Path("presentation/pycon_wroclaw/slides.pdf")

    marp_content = convert_scratch_to_marp(src.read_text())
    out_md.write_text(marp_content)
    print(f"Generated Marp Markdown at: {out_md}")

    # Build PDF with Marp CLI
    cmd = ["npx", "@marp-team/marp-cli", str(out_md), "--pdf", "--allow-local-files", "-o", str(out_pdf)]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"Successfully generated PDF: {out_pdf}")
