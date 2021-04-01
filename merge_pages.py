import PyPDF2


def merge(pdf_file_path=None):
    if not pdf_file_path:
        pdf_file_path = 'labels_example.pdf'

    with open(pdf_file_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)

    NUM_OF_PAGES = reader.getNumPages()

    first_page = reader.getPage(0)
    data_height = first_page.mediaBox.getHeight()
    data_width = first_page.mediaBox.getWidth()
    new_page_height = data_height * 3
    print(data_height, data_width)

    new_pdf_page = PyPDF2.pdf.PageObject.createBlankPage(None, data_width * 2, new_page_height)

    ty = None
    for i in range(NUM_OF_PAGES):
        if i % 2 == 0:
            ty = data_height * (i) // 2
        next_page = reader.getPage(i)
        new_pdf_page.mergeScaledTranslatedPage(
            next_page,
            scale=1,
            tx=(i % 2) * data_width,
            ty=ty,
            expand=False
        )

    writer = PyPDF2.PdfFileWriter()
    writer.addPage(new_pdf_page)

    with open('output.pdf', 'wb') as f:
        writer.write(f)


if __name__ == '__main__':
    merge()
