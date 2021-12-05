import os
import sys
import glob
import shutil
import PyPDF2


def merge(pdf_sources: [str] = None, pdf_dest=None, page_limit=None):
    """
    saves a pdf with 6 labels per page
    :param pdf_sources: list of full or relative path of the source pdf files
    :param pdf_dest: full or relative path of the newly created pdf
    :param page_limit: limit the number of labels to be added in the final pdf. if not
           specified, all labels are added
    :return: None
    """

    # set values for default args

    if not page_limit:
        page_limit = sys.maxsize
    if not pdf_sources:
        pdf_sources = []

    readers = [PyPDF2.PdfFileReader(open(pdf_source, 'rb'), strict=False) for pdf_source in pdf_sources]

    # if limit is specified,then limit the number of labels. otherwise
    # add all labels. if the specified limit is more than available
    # labels then just add all the labels
    num_of_pages = min(len(pdf_sources), page_limit)

    # divide the labels into segments of 6 labels per page
    segmented_pages = [list(range(num_of_pages))[offset:offset + 6] for offset in range(0, num_of_pages, 6)]
    print('page segments:', segmented_pages)

    # if the pdf has only one label then just copy the same pdf as output
    if num_of_pages == 1:
        shutil.copyfile(pdf_sources[0], pdf_dest)
        return

    first_page = readers[0].getPage(0)
    data_height = first_page.mediaBox.getHeight()
    data_width = first_page.mediaBox.getWidth()

    new_page_height = data_height * 3
    new_page_width = data_height * 2

    # create the pdf writer object
    pdf_writer = PyPDF2.PdfFileWriter()

    for dest_page in segmented_pages:
        new_pdf_page = PyPDF2.pdf.PageObject.createBlankPage(None, new_page_width, new_page_height)
        translate_y = None

        for idx, source_page_num in enumerate(dest_page):
            # update the translate y property for each 2 labels
            if source_page_num % 2 == 0:
                translate_y = data_height * (3 - idx // 2 - 1)
            translate_x = (source_page_num % 2) * data_width

            # add the current label to the pdf page
            try:
                new_pdf_page.mergeScaledTranslatedPage(
                    readers[source_page_num].getPage(0),
                    scale=1,
                    tx=translate_x,
                    ty=translate_y
                )
            except IndexError:
                print('error')
                continue

            # add this page to writer object
        pdf_writer.addPage(new_pdf_page)

    # save the merged pdf in source dir
    with open(pdf_dest, 'wb') as f:
        pdf_writer.write(f)


def test():
    merge(glob.glob('gls/*.pdf'), 'dest.pdf')


if __name__ == '__main__':
    test()
