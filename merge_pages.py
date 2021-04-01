import PyPDF2


def merge():
    reader = PyPDF2.PdfFileReader(open("labels_example.pdf", 'rb'))

    NUM_OF_PAGES = reader.getNumPages()

    page0 = reader.getPage(0)
    h = page0.mediaBox.getHeight()
    w = page0.mediaBox.getWidth()
    print(h, w)
    newpdf_page = PyPDF2.pdf.PageObject.createBlankPage(None, w * 2, h * NUM_OF_PAGES)
    ty = h * (NUM_OF_PAGES - 1) / 2
    for i in range(NUM_OF_PAGES):
        if i % 2 == 0:
            ty = h * (NUM_OF_PAGES - i - 1) / 2
        next_page = reader.getPage(i)
        newpdf_page.mergeScaledTranslatedPage(
            next_page,
            scale=1,
            tx=(i % 2) * w,
            ty=ty,
            expand=False
        )

    writer = PyPDF2.PdfFileWriter()
    writer.addPage(newpdf_page)

    with open('output.pdf', 'wb') as f:
        writer.write(f)


if __name__ == '__main__':
    merge()
