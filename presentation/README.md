# Building presentation PDFs

Run `uv run --script presentation/build_pdf.py` from the repository root.
Requires Node.js/npm and Chrome, Edge, or Firefox. On the first run, `npx`
downloads the pinned Marp CLI version. The Python script has no dependencies.

The default is the PyCon Wrocław deck. An optional source argument selects
another deck, for example
`uv run --script presentation/build_pdf.py presentation/warsaw_python_pizza/slides_scratch.md`.
The generated Markdown and PDF are written beside the source, with the names
slides_marp.md and slides.pdf. The default source also works when the script is
invoked by absolute path from another working directory.

## Scratch format

- `#` and `##` headings start slides (except inside fenced code blocks).
- `![I](./img/example.png)` fills the available image area.
- `IL` / `IR` place images in left/right columns.
- `ITL` / `ITR` / `IBL` / `IBR` place images in a 2×2 grid.
- Missing positions stay empty; duplicate tags or mixed layouts are errors.
- `C: ` adds a plain-text caption; `S: ` / `R: ` add plain-text sources.
- `N: ` adds a single note; `Notes:` starts notes until the next slide heading.

Images are centered and scaled to fit without cropping or changing their aspect
ratio, including SVGs. Headings, text, captions, and sources take space first;
the image grid uses the remainder. Images may be enlarged, so use sufficiently
high-resolution assets. Text-only overflow is not automatically shrunk: shorten
the text or split the slide if it exceeds a page.

Only build trusted Markdown: HTML and local-file access are enabled to support
the layouts and local images. Ordinary Markdown images without the positional
tags retain Marp's default sizing.

## Managed browsers and preview mode

Marp's PDF export requires browser automation. If browser logs say **“DevTools
remote debugging is disallowed by the system admin”**, the machine policy blocks
that export (Marp may instead report a misleading “browser is already running”
error). Do not change the policy to run this script.

Use `uv run --script presentation/build_pdf.py --html-only` instead, then open
the generated HTML preview beside the source in Chrome/Edge and use Print →
Save as PDF. Disable browser headers and footers. This does not require remote
debugging. The `BROWSER_PATH` environment variable can select an executable for
Marp, but it cannot override an administrator policy.

## Tests

Run `python -m pytest test/test_build_pdf.py` for the fast regression tests.
To also exercise actual print layout, set `MARP_TEST_BROWSER` to the full path
of a Chrome/Edge executable and run the same tests. The opt-in test requires
Node.js/npm, renders the real deck plus extreme aspect ratios and long captions,
and checks geometry during headless PDF printing. It does not require Playwright
or remote debugging.
