# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Convert trusted scratch slides to Marp and render them with Node.js/Chromium."""

import argparse
import re
import shutil
import subprocess
from html import escape
from pathlib import Path

DEFAULT_SOURCE = Path(__file__).resolve().parent / "pycon_wroclaw" / "slides_scratch.md"
MARP_PACKAGE = "@marp-team/marp-cli@4.5.1"
IMAGE_LAYOUTS = (("ITL", "ITR", "IBL", "IBR"), ("IL", "IR"), ("I",))

MARP_HEADER = """---
marp: true
theme: default
size: 16:9
math: katex
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    /* Bottom padding = footer bar height (34px) + clearance above it. */
    padding: 30px 40px 58px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    box-sizing: border-box;
  }
  section > :not(.images) { flex-shrink: 0; }
  h1 { font-size: 2.2rem; margin: auto 0; text-align: center; }
  h2 { font-size: 1.8rem; margin: 0 0 10px; }
  /* The negative margins bleed the title banner over the section padding so it
     spans the full slide width (keep in sync with the section padding above). */
  h3 {
    font-size: 1.8rem;
    margin: -30px -40px 14px;
    padding: 8px 0;
    background: #000;
    color: #fff;
    text-align: center;
  }
  section.section-slide { justify-content: center; align-items: center; }
  section.section-slide h2 { font-size: 2rem; margin: 0; text-align: center; }
  /* The title slide centers its content group (title + caption) as a whole;
     h1 auto margins are disabled since they would pin the caption to the bottom. */
  section.title-slide { justify-content: center; align-items: center; }
  section.title-slide h1 { margin: 0 0 12px; }
  /* Full-width black bottom bar with white section/number labels; the section
     padding-bottom reserves caption space above it. A div, not <footer>, so
     Marp's theme footer styles cannot interfere. */
  .slide-footer {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 0 20px;
    background: #000;
    color: #fff;
    font-size: 0.9rem;
    box-sizing: border-box;
  }
  .images {
    flex: 1 1 0;
    min-height: 0;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    grid-template-rows: minmax(0, 1fr);
    gap: 12px;
    margin: 5px 0;
  }
  .images-2, .images-4 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .images-4 { grid-template-rows: repeat(2, minmax(0, 1fr)); }
  .image-cell { position: relative; min-width: 0; min-height: 0; }
  .image-cell img {
    position: absolute;
    inset: 0;
    display: block;
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
  .caption, .reference {
    display: block;
    text-align: center;
    overflow-wrap: anywhere;
    margin: 0;
  }
  p:has(> .caption), p:has(> .reference) { margin: 0; }
  .caption { font-size: 1.05rem; color: #333; padding-top: 6px; }
  .reference { font-size: 0.8rem; color: #666; padding-top: 2px; }
  .katex { font-size: 1em; }
---
"""


def update_fence(line: str, fence: str) -> str:
    """Track Markdown fences so code examples are not interpreted as slide syntax."""
    marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
    if marker:
        run = marker[1]
        if not fence:
            if run[0] == "`" and "`" in line[marker.end() :]:
                return ""  # Backticks in the info string make this inline code, not a fence.
            return run
        if run[0] == fence[0] and len(run) >= len(fence) and not line[marker.end() :].strip():
            return ""
    return fence


def split_slides(text: str) -> list[list[str]]:
    """Split into slides at 1-3 level headings, ignoring fenced code and notes."""
    slides: list[list[str]] = []
    lines: list[str] = []
    fence = ""
    in_notes = False
    for line in text.strip().splitlines():
        if not in_notes:
            fence = update_fence(line, fence)
        if not fence and re.match(r"^#{1,3}\s", line) and lines:
            slides.append(lines)
            lines = []
            in_notes = False
        if not fence and line.strip().startswith("Notes:"):
            in_notes = True
        lines.append(line)
    if lines:
        slides.append(lines)
    return slides


def heading_level(lines: list[str]) -> int | None:
    """Return the 1-3 heading level that starts a slide, or None for leading content."""
    match = re.match(r"^(#{1,3})\s", lines[0]) if lines else None
    return len(match[1]) if match else None


def render_images(images: dict[str, str]) -> str:
    layout = next(tags for tags in IMAGE_LAYOUTS if any(tag in images for tag in tags))
    if not images.keys() <= set(layout):
        raise ValueError("Do not mix single, left/right, and quadrant image tags on one slide.")
    cells: list[str] = []
    for tag in layout:
        # Empty cells preserve positions when, for example, only IBR or IR is supplied.
        image = f'<img src="{escape(images[tag], quote=True)}" alt="" />' if tag in images else ""
        cells.append(f'  <div class="image-cell">{image}</div>')
    return f'<div class="images images-{len(layout)}">\n' + "\n".join(cells) + "\n</div>"


def convert_scratch_to_marp(scratch_text: str) -> str:
    slide_sources = split_slides(scratch_text)
    numbered_total = sum(heading_level(lines) not in (1, 2) for lines in slide_sources)
    slides: list[str] = []
    number = 0
    section_name = ""
    for lines in slide_sources:
        slide_lines: list[str] = []
        notes: list[str] = []
        captions: list[str] = []
        references: list[str] = []
        images: dict[str, str] = {}
        in_notes = False
        fence = ""
        for line in lines:
            stripped = line.strip()
            if in_notes:
                notes.append(line)
                continue
            previous_fence = fence
            fence = update_fence(line, fence)
            if previous_fence or fence:
                slide_lines.append(line)
            elif stripped.startswith("Notes:"):
                in_notes = True
                if inline_note := stripped[len("Notes:") :].strip():
                    notes.append(inline_note)
            elif stripped.startswith("N: "):
                notes.append(stripped[3:])
            elif stripped.startswith("C: "):
                captions.append(stripped[3:])
            elif stripped.startswith("Ref: "):
                references.append(stripped[5:])
            elif match := re.fullmatch(r"!\[(ITL|ITR|IBL|IBR|IL|IR|I)\]\((.+)\)", stripped):
                tag, path = match.groups()
                if tag in images:
                    raise ValueError(f"Duplicate image tag {tag!r} on one slide.")
                images[tag] = path
            else:
                slide_lines.append(line)

        # Blank lines keep HTML blocks separate from Markdown and from each other.
        if images:
            slide_lines.extend(["", render_images(images), ""])
        for css_class, values in (("caption", captions), ("reference", references)):
            for value in values:
                # Spans (not divs) keep captions inside Markdown processing so
                # $...$ KaTeX math renders; display:block puts each on its own line.
                slide_lines.extend(["", f'<span class="{css_class}">{escape(value)}</span>', ""])
        if notes:
            safe_notes = "\n".join(notes).replace("-->", "--&gt;")
            slide_lines.append(f"\n<!--\n{safe_notes}\n-->")
        # `#` is the title slide and `##` a centered section slide: both stay
        # unnumbered. Only `###` slides count; they show x/y in the bottom-right
        # corner and the current section name in the bottom-left corner.
        level = heading_level(lines)
        directives: list[str] = []
        if level == 1:
            directives.append("<!-- _class: title-slide -->")
        if level == 2:
            directives.append("<!-- _class: section-slide -->")
            words = lines[0].split(None, 1)
            section_name = words[1].strip() if len(words) > 1 else ""
        content = "\n".join(slide_lines).strip()
        if level not in (1, 2):
            number += 1
            # Marp's paginate directive is boolean-only: a custom x/y value is
            # silently ignored, so render our own bar with white labels on black.
            labels = []
            if section_name:
                labels.append(f'<span class="slide-section">{escape(section_name)}</span>')
            labels.append(f'<span class="slide-number">{escape(f"{number}/{numbered_total}")}</span>')
            bar = '<div class="slide-footer">' + "".join(labels) + "</div>"
            content = ("\n\n".join(part for part in (bar, content) if part)).strip()
        slides.append(("\n".join(directives) + "\n\n" + content).strip() if directives else content)
    return MARP_HEADER + "\n\n---\n\n".join(slides) + "\n"


def build_pdf(source: Path = DEFAULT_SOURCE, *, html_only: bool = False) -> Path:
    """Write outputs beside the source so relative image URLs work from any cwd."""
    source = source.resolve()
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx:
        raise RuntimeError("Node.js and npx are required to build the PDF. Install Node.js and retry.")
    content = convert_scratch_to_marp(source.read_text(encoding="utf-8"))
    out_md = source.with_name("slides_marp.md")
    output = source.with_name("slides_preview.html" if html_only else "slides.pdf")
    out_md.write_text(content, encoding="utf-8")
    print(f"Generated Marp Markdown at: {out_md}", flush=True)
    # HTML is required for our image grids. Only render trusted slide sources.
    # A preview can be printed manually when browser automation is unavailable.
    format_args = ["--template", "bare"] if html_only else ["--pdf", "--allow-local-files"]
    subprocess.run(
        [npx, "--yes", MARP_PACKAGE, out_md.name, "--html", *format_args, "-o", output.name],
        check=True,
        cwd=source.parent,
    )
    print(f"Successfully generated: {output}")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE, help="Scratch Markdown to render")
    parser.add_argument("--html-only", action="store_true", help="Generate a preview for manual browser printing")
    args = parser.parse_args()
    build_pdf(args.source, html_only=args.html_only)
