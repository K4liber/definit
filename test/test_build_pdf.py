"""Fast converter tests; these do not require Node.js or a browser."""

import importlib.util
import json
import os
import re
import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "presentation" / "build_pdf.py"
spec = importlib.util.spec_from_file_location("build_pdf", SCRIPT)
assert spec is not None and spec.loader is not None
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def body(text: str) -> str:
    return builder.convert_scratch_to_marp(text).removeprefix(builder.MARP_HEADER)


def test_heading_levels_split_slides():
    result = body("# Title\n\n## Slide\n### Detail\n\n## End")
    assert result.count("\n\n---\n\n") == 3
    assert "## Slide\n### Detail" not in result


def test_title_and_section_slides_are_unnumbered_content_slides_show_page_numbers():
    result = body("# Title\n## Section\n### A\n### B\n## Section Two\n### C")
    slides = result.split("\n\n---\n\n")
    assert len(slides) == 6
    assert slides[0].startswith("# Title")
    assert slides[1].startswith("<!-- _class: section-slide -->\n\n## Section")
    assert slides[2].startswith(
        '<div class="slide-section">Section</div>\n<div class="slide-number">1/3</div>\n\n### A'
    )
    assert slides[3].startswith(
        '<div class="slide-section">Section</div>\n<div class="slide-number">2/3</div>\n\n### B'
    )
    assert slides[4].startswith("<!-- _class: section-slide -->\n\n## Section Two")
    assert slides[5].startswith(
        '<div class="slide-section">Section Two</div>\n<div class="slide-number">3/3</div>\n\n### C'
    )


def test_slides_before_any_section_have_no_section_label():
    result = body("# Deck\n### Intro slide")
    assert '<div class="slide-section">' not in result
    assert '<div class="slide-number">1/1</div>' in result


def test_section_label_escapes_html():
    result = body("## Ørsted <3 & co\n### Slide")
    assert '<div class="slide-section">Ørsted &lt;3 &amp; co</div>' in result


def test_paginate_is_not_used_so_marp_cannot_drop_custom_numbers():
    # Marp's paginate directive is boolean-only; custom x/y values are silently
    # ignored, which removed all numbers. We render our own label instead.
    assert "paginate" not in builder.MARP_HEADER
    assert '<div class="slide-number">' in body("### Only")


@pytest.mark.parametrize("fence", ["```", "~~~~"])
def test_fenced_code_preserves_headings_and_special_markers(fence: str):
    code = f"{fence}text\n# Not a slide\n![I](sample.png)\nC: Not a caption\nNotes:\n{fence}"
    result = body(f"## Code\n{code}\n## Next")
    assert code in result
    assert result.count("\n\n---\n\n") == 1
    assert '<div class="images' not in result


@pytest.mark.parametrize("heading", ["##", "###"])
@pytest.mark.parametrize("tags", builder.IMAGE_LAYOUTS)
def test_layouts_render_in_positional_order(heading: str, tags: tuple[str, ...]):
    result = body(heading + " Images\n" + "\n".join(f"![{tag}]({tag}.png)" for tag in reversed(tags)))
    assert f'class="images images-{len(tags)}"' in result
    assert result.count('class="image-cell"') == len(tags)
    assert [result.index(f'src="{tag}.png"') for tag in tags] == sorted(
        result.index(f'src="{tag}.png"') for tag in tags
    )
    assert ' width="' not in result
    assert ' height="' not in result


@pytest.mark.parametrize("tag,count", [("IR", 2), ("IBR", 4)])
def test_partial_layout_keeps_empty_cells(tag: str, count: int):
    result = body(f"## Partial\n![{tag}](image.svg)")
    assert result.count('<div class="image-cell"></div>') == count - 1
    assert result.index('<div class="image-cell"></div>') < result.index("<img")


@pytest.mark.parametrize("tags", [("I", "IR"), ("IL", "ITL"), ("I", "I")])
def test_invalid_layout_raises_instead_of_dropping_images(tags: tuple[str, ...]):
    with pytest.raises(ValueError):
        body("## Invalid\n" + "\n".join(f"![{tag}](image.png)" for tag in tags))


def test_paths_with_parentheses_and_html_characters():
    result = body('## Image\n![I](./img/a (1) & "b".svg)')
    assert 'src="./img/a (1) &amp; &quot;b&quot;.svg"' in result


def test_captions_references_and_notes():
    result = body("## Slide\nC: Ørsted <3\nRef: https://example.com\nRef: Book\nN: First\nNotes:\nSecond\n\nThird")
    assert '<div class="caption">Ørsted &lt;3</div>' in result
    assert result.count('<div class="reference">') == 2
    assert "<!--\nFirst\nSecond\n\nThird\n-->" in result


def test_notes_cannot_close_the_html_comment():
    assert "<!--\nsecret --&gt; still secret\n-->" in body("## Slide\nN: secret --> still secret")


def test_ordinary_markdown_images_are_unchanged():
    assert "![description](image.png)" in body("## Slide\n![description](image.png)")


def test_inline_backticks_do_not_swallow_slides_or_images():
    result = body("## One\n```inline code```\n## Two\n![I](image.png)")
    assert result.count("\n\n---\n\n") == 1
    assert '<img src="image.png"' in result


def test_inline_notes_stay_hidden_and_note_fences_do_not_swallow_slides():
    result = body("## One\nNotes: private\n```python\nprivate example\n## Two\n![I](image.png)")
    assert "<!--\nprivate\n```python\nprivate example\n-->" in result
    assert result.count("\n\n---\n\n") == 1
    assert '<img src="image.png"' in result


def test_build_uses_utf8_absolute_paths_and_explicit_html(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    directory = tmp_path / "R&D slides"
    directory.mkdir()
    source = directory / "slides_scratch.md"
    source.write_text("## Wrocław Ørsted 🐍\n![I](./img/test.svg)", encoding="utf-8")
    monkeypatch.chdir(tmp_path.parent)
    monkeypatch.setattr(builder.shutil, "which", Mock(return_value="npx.cmd"))
    run = Mock()
    monkeypatch.setattr(builder.subprocess, "run", run)

    assert builder.build_pdf(source) == directory / "slides.pdf"
    assert "Wrocław Ørsted 🐍" in (directory / "slides_marp.md").read_text(encoding="utf-8")
    command = run.call_args.args[0]
    assert command[:3] == ["npx.cmd", "--yes", builder.MARP_PACKAGE]
    assert "slides_marp.md" in command
    assert all("R&D" not in arg for arg in command)
    assert all(flag in command for flag in ["--html", "--pdf", "--allow-local-files"])
    assert run.call_args.kwargs == {"check": True, "cwd": directory}


def test_default_source_does_not_depend_on_working_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    assert builder.DEFAULT_SOURCE.is_absolute()
    assert builder.DEFAULT_SOURCE.is_file()


def test_html_preview_does_not_require_browser_automation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    source = tmp_path / "slides_scratch.md"
    source.write_text("## Slide", encoding="utf-8")
    monkeypatch.setattr(builder.shutil, "which", Mock(return_value="npx"))
    run = Mock()
    monkeypatch.setattr(builder.subprocess, "run", run)
    assert builder.build_pdf(source, html_only=True) == tmp_path / "slides_preview.html"
    command = run.call_args.args[0]
    assert "--template" in command and "bare" in command
    assert "--html" in command and "--pdf" not in command


def test_missing_node_has_actionable_error(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(builder.shutil, "which", Mock(return_value=None))
    with pytest.raises(RuntimeError, match="Install Node.js"):
        builder.build_pdf()


def test_render_failure_propagates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    source = tmp_path / "slides_scratch.md"
    source.write_text("## Slide", encoding="utf-8")
    monkeypatch.setattr(builder.shutil, "which", Mock(return_value="npx"))
    monkeypatch.setattr(builder.subprocess, "run", Mock(side_effect=subprocess.CalledProcessError(1, "npx")))
    with pytest.raises(subprocess.CalledProcessError):
        builder.build_pdf(source)


@pytest.mark.skipif(not os.environ.get("MARP_TEST_BROWSER"), reason="Opt-in: set MARP_TEST_BROWSER to Chrome/Edge")
def test_print_layout_contains_all_images_and_captions(tmp_path: Path):
    """Check real browser geometry, not just generated HTML strings."""
    # Include the real deck plus extreme aspect ratios and incomplete grids.
    synthetic: list[str] = []
    for label, width, height in (("portrait", 100, 1000), ("wide", 1000, 100), ("square", 100, 100)):
        image = tmp_path / f"{label}.svg"
        image.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">'
            f'<rect width="{width}" height="{height}" fill="teal"/></svg>',
            encoding="utf-8",
        )
        for tags in (*builder.IMAGE_LAYOUTS, ("IR",), ("IBR",)):
            synthetic.append(
                f"## {label}\n"
                + "\n".join(f"![{tag}]({image.as_uri()})" for tag in tags)
                + "\nC: "
                + "A long caption that wraps across lines. " * 5
                + "\nRef: https://example.com"
            )
    real_slides = builder.DEFAULT_SOURCE.read_text(encoding="utf-8").replace(
        "./img/", (builder.DEFAULT_SOURCE.parent / "img").as_uri() + "/"
    )
    scratch = real_slides + "\n\n" + "\n\n".join(synthetic)
    markdown = tmp_path / "layout.md"
    markdown.write_text(builder.convert_scratch_to_marp(scratch), encoding="utf-8")
    html = tmp_path / "layout.html"
    npx = builder.shutil.which("npx.cmd") or builder.shutil.which("npx")
    assert npx is not None
    subprocess.run(
        [npx, "--yes", builder.MARP_PACKAGE, markdown.name, "--html", "--template", "bare", "-o", html.name],
        cwd=tmp_path,
        check=True,
        timeout=120,
    )
    # Use the supported headless print interface, not DevTools (which may be
    # disabled on managed machines). beforeprint measures actual print CSS.
    probe = """<script>
            window.addEventListener('beforeprint', () => {
                const errors = [];
                const sections = [...document.querySelectorAll('section')];
                for (const [index, section] of sections.entries()) {
                    const bounds = section.getBoundingClientRect();
                    for (const element of section.querySelectorAll('.images, .caption, .reference, .image-cell img')) {
                        const rect = element.getBoundingClientRect();
                        if (rect.width <= 0 || rect.height <= 0 || rect.left < bounds.left - 1 ||
                            rect.right > bounds.right + 1 || rect.top < bounds.top - 1 || rect.bottom > bounds.bottom + 1)
                            errors.push(`Slide ${index + 1}: overflow/empty ${element.className || element.tagName}`);
                        if (element.tagName === 'IMG' && (!element.naturalWidth || !element.naturalHeight ||
                            getComputedStyle(element).objectFit !== 'contain'))
                            errors.push(`Slide ${index + 1}: unloaded or distorted image ${element.src}`);
                    }
                    const grid = section.querySelector('.images');
                    if (grid) {
                        const heading = section.querySelector('h1, h2');
                        const caption = section.querySelector('.caption, .reference');
                        const rect = grid.getBoundingClientRect();
                        if (heading && heading.getBoundingClientRect().bottom > rect.top + 1)
                            errors.push(`Slide ${index + 1}: image overlaps heading`);
                        if (caption && caption.getBoundingClientRect().top < rect.bottom - 1)
                            errors.push(`Slide ${index + 1}: image overlaps caption`);
                    }
                }
                console.log('DEFINIT_LAYOUT_RESULT=' + JSON.stringify({errors, slides: sections.length,
                    images: document.querySelectorAll('.image-cell img').length}));
            });
    </script>"""
    html.write_text(html.read_text(encoding="utf-8").replace("</body>", probe + "</body>"), encoding="utf-8")
    pdf = tmp_path / "layout.pdf"
    rendered = subprocess.run(
        [
            os.environ["MARP_TEST_BROWSER"],
            "--headless",
            f"--user-data-dir={tmp_path / 'profile'}",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf}",
            "--enable-logging=stderr",
            html.as_uri(),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        timeout=60,
    )
    match = re.search(r"DEFINIT_LAYOUT_RESULT=(\{.*\})", rendered.stderr)
    assert match is not None, rendered.stderr
    result = json.loads(match[1])
    assert result["slides"] == len(builder.split_slides(scratch))
    assert result["images"] == scratch.count("![")
    assert result["errors"] == []
    assert pdf.read_bytes().startswith(b"%PDF-")
