import pymupdf

doc = pymupdf.open(input("Pdf: "))
page = doc[0]

print("Images:", len(page.get_images()))
print("Vector drawings:", len(page.get_drawings()))
print("Annotations:", [a.type[1] for a in (page.annots() or [])])

for r in page.search_for(input("Search Text: ")):
    print("Text Location:", r)
    for b in page.get_text("dict", clip=r)["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                print("  text:", repr(s["text"]), "font:", s["font"], "size:", round(s["size"], 1))
