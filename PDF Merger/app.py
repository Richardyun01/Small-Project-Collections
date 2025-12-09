from pypdf import PdfWriter

merger = PdfWriter()

for pdf in ["001.pdf", "002.pdf"]:
    merger.append(pdf)

merger.write("out.pdf")
