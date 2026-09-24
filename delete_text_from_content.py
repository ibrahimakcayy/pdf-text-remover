import pymupdf

input_file = input("Pdf name: ")
output_file = "deleted.pdf"
TARGET_TEXT = input("Target text: ")
REMOVE_LINKS = input("Remove links? (y/n): ").strip().lower() == "y"
REPORT_INTERVAL = 100


def remove_links(page) -> int:
    """Removes all link annotations on the page, returns number of links removed."""
    links = page.get_links()
    for link in links:
        page.delete_link(link)
    return len(links)


doc = pymupdf.open(input_file)
total_removed = 0
pages_changed = 0
total_links_removed = 0

for page in doc:
    if REMOVE_LINKS:
        total_links_removed += remove_links(page)

    rects = page.search_for(TARGET_TEXT)
    if rects:
        for r in rects:
            # fill=None keeps the area transparent (no visible box) after redaction
            page.add_redact_annot(r, fill=None)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
        total_removed += len(rects)
        pages_changed += 1

    if (page.number + 1) % REPORT_INTERVAL == 0:
        print(f"{page.number + 1}/{len(doc)} pages processed...")

print(f"{pages_changed} pages changed, {total_removed} matches removed, {total_links_removed} links removed")
doc.save(output_file, garbage=3, deflate=True)
doc.close()
