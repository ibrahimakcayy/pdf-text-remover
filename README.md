# pdf-text-remover

Small Python scripts for removing specific text or all text written in a given font from PDF files. Built on [PyMuPDF](https://pymupdf.readthedocs.io/) and permanently removes content via redaction.

## Features

- **Delete by content** — searches a PDF for a specific piece of text and redacts (permanently removes) every match.
- **Delete by font** — strips every text block written in a given font directly from the PDF's content streams.
- **Link cleanup** — optionally removes all link annotations from the PDF as well.
- **Font/text inspector** — shows how the text on a page is styled (font name, size) and reports the number of images/drawings/annotations on the page.

## Files

| File | What it does |
|---|---|
| `delete_text_from_content.py` | Searches the PDF for the text you enter and redacts every match. |
| `delete_text_from_font.py` | Removes every text block written in the font name you enter from the PDF's content streams. |
| `find_font.py` | Shows the image/drawing/annotation counts on a PDF's first page and the font name/size of any searched text (useful for finding the target font name). |

## Requirements

- Python 3
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)

Install with:

```bash
pip install pymupdf
```

## Usage

### 1. Remove a specific piece of text

```bash
python delete_text_from_content.py
```

You'll be prompted for:
1. `Pdf name:` — the file to process
2. `Target text:` — the text to remove from the PDF
3. `Remove links? (y/n):` — whether to also strip link annotations

The result is saved as `deleted.pdf`; the number of matches removed per page and the number of links removed are printed to the console.

### 2. Remove all text in a given font

If you don't already know which font to target, use `find_font.py` first to inspect the fonts used in the PDF:

```bash
python find_font.py
```

After entering `Pdf:` and `Search Text:`, it lists the font name and size at every location where the searched text appears.

Once you know the font name:

```bash
python delete_text_from_font.py
```

You'll be prompted for:
1. `Pdf name:` — the file to process
2. `Target font name:` — the font to remove (matched as a substring, not an exact match)
3. `Remove links? (y/n):` — whether to also strip link annotations

The result is again saved as `deleted.pdf`, with a report of how many pages changed, how many bytes were removed, and how many links were removed.

> **Note:** Font-based removal edits the PDF's content streams directly. While more surgical than redaction, this can behave unexpectedly on complex or unusually structured PDFs. Test on a copy of any important file first.

## License

This project is licensed under the [MIT License](LICENSE).
