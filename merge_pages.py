import sys
import PyPDF2


def merge(pdf_file_path=None, page_limit=None):
    """
    :param pdf_file_path: full or relative path of the pdf
    :param page_limit: limit the number of labels to be added in the final pdf. if not
           specified, all labels are added
    :return: None. saves a pdf with 6 labels per page
    """

    # set values for default args
    if not pdf_file_path:
        pdf_file_path = 'labels_example.pdf'
    if not page_limit:
        page_limit = sys.maxsize

    reader = PyPDF2.PdfFileReader(open(pdf_file_path, 'rb'), strict=False)

    # if limit is specified,then limit the number of labels. otherwise
    # add all labels. if the specified limit is more than available
    # labels then just add all the labels
    NUM_OF_PAGES = min(reader.getNumPages(), page_limit)

    first_page = reader.getPage(0)
    data_height = first_page.mediaBox.getHeight()
    data_width = first_page.mediaBox.getWidth()

    new_page_height = data_height * 3
    new_page_width = data_height * 2

    # create the pdf writer object
    pdf_writer = PyPDF2.PdfFileWriter()

    # for every 6 labels, create a new page
    for _ in range(0, NUM_OF_PAGES, 6):
        new_pdf_page = PyPDF2.pdf.PageObject.createBlankPage(None, new_page_width, new_page_height)

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

        pdf_writer.addPage(new_pdf_page)

    with open('output.pdf', 'wb') as f:
        pdf_writer.write(f)


if __name__ == '__main__':
    merge()
