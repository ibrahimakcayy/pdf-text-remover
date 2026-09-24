import re
import pymupdf

input_file = input("Pdf name: ")
output_file = "deleted.pdf"
TARGET_FONT = input("Target font name: ")
REMOVE_LINKS = input("Remove links? (y/n): ").strip().lower() == "y"
REPORT_INTERVAL = 100

TF = re.compile(rb"/([^\s/\[\]()<>]+)\s+[-\d.]+\s+Tf")
PATTERN = re.compile(
    rb"/([^\s/\[\]()<>]+)\s+[-\d.]+\s+Tf|\bBT\b.*?\bET\b", re.S
)

def clean_stream(stream: bytes, names: set) -> bytes:
    state = [False]  # whether the last set font was a target font

    def remove(m):
        if m.group(1):  # standalone Tf outside BT
            state[0] = m.group(1) in names
            return m.group(0)
        block = m.group(0)
        flags = [f in names for f in TF.findall(block)]
        if not flags:          # font inherited from previous state
            flags = [state[0]]
        else:
            state[0] = flags[-1]
        return b"" if all(flags) else block

    return PATTERN.sub(remove, stream)


def remove_links(page) -> int:
    """Removes all link annotations on the page, returns number of links removed."""
    links = page.get_links()
    for link in links:
        page.delete_link(link)
    return len(links)


doc = pymupdf.open(input_file)
processed = set()      # (xref, names) -> avoid reprocessing shared stream
total_removed = 0
pages_changed = 0
total_links_removed = 0

for page in doc:
    if REMOVE_LINKS:
        total_links_removed += remove_links(page)

    names = {
        f[4].encode("latin-1", "ignore")
        for f in page.get_fonts(full=False)
        if TARGET_FONT in f[3]
    }
    if names:
        xrefs = page.get_contents()
        if len(xrefs) > 1:
            page.clean_contents()
            xrefs = page.get_contents()

        if xrefs:
            xref = xrefs[0]
            key = (xref, frozenset(names))
            if key not in processed:
                processed.add(key)
                stream = doc.xref_stream(xref)
                if b"BT" in stream:
                    new_stream = clean_stream(stream, names)
                    if len(new_stream) != len(stream):
                        doc.update_stream(xref, new_stream)
                        total_removed += len(stream) - len(new_stream)
                        pages_changed += 1

    if (page.number + 1) % REPORT_INTERVAL == 0:
        print(f"{page.number + 1}/{len(doc)} pages processed...")

print(f"{pages_changed} pages changed, {total_removed} bytes removed, {total_links_removed} links removed")
doc.save(output_file, garbage=3, deflate=True)
doc.close()
