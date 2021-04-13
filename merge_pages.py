import os
import sys
import glob
from pprint import pprint

import PyPDF2
import shutil


def merge(pdf_source=None, pdf_dest=None, page_limit=None):
    """
    saves a pdf with 6 labels per page
    :param pdf_source: full or relative path of the source pdf
    :param pdf_dest: full or relative path of the newly created pdf
    :param page_limit: limit the number of labels to be added in the final pdf. if not
           specified, all labels are added
    :return: None
    """

    # set values for default args
    if not pdf_source:
        pdf_source = 'labels_example.pdf'
    if not pdf_dest:
        dir_name, file_name = os.path.split(pdf_source)
        pdf_dest = os.path.join(dir_name, 'merged_labels', file_name)
        os.makedirs(os.path.join(dir_name, 'merged_labels'), exist_ok=True)
        print(pdf_dest)
        return

    if not page_limit:
        page_limit = sys.maxsize

    reader = PyPDF2.PdfFileReader(open(pdf_source, 'rb'), strict=False)

    # if limit is specified,then limit the number of labels. otherwise
    # add all labels. if the specified limit is more than available
    # labels then just add all the labels
    NUM_OF_PAGES = min(reader.getNumPages(), page_limit)

    # if the pdf has only one label then just copy the same pdf as output
    if NUM_OF_PAGES == 1:
        shutil.copyfile(pdf_source, pdf_dest)
        return

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

        translate_y = None
        for i in range(6):
            # update the translate y property for each 2 labels
            if i % 2 == 0:
                translate_y = data_height * i / 2
            translate_x = ((i + 1) % 2) * data_width

            # add the current label to the pdf page
            new_pdf_page.mergeScaledTranslatedPage(
                reader.getPage(NUM_OF_PAGES - i - 1),
                scale=1,
                tx=translate_x,
                ty=translate_y
            )
        # add this page to writer object
        pdf_writer.addPage(new_pdf_page)

    # save the merged pdf in source dir
    with open(pdf_dest, 'wb') as f:
        pdf_writer.write(f)


if __name__ == '__main__':
    files = glob.glob('./arco_labels/*')
    for file in files:
        merge(file)
