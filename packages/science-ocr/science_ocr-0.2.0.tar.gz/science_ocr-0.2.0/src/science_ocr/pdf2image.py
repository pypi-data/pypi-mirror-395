import fitz
from PIL import Image


def convert_from_path(pdf_path, dpi, first_page=0, last_page=None):
	images = []
	pdf_document = fitz.open(pdf_path)

	if first_page is None:
		first_page = 0
	if last_page is None or last_page > len(pdf_document):
		last_page = len(pdf_document)

	for page_number in range(first_page, len(pdf_document) if last_page is None else last_page):
		page = pdf_document[page_number]
		pix = page.get_pixmap(colorspace=fitz.csGRAY, dpi=dpi)
		# "L" → PIL mode for 8-bit grayscale.
		img = Image.frombytes("L", [pix.width, pix.height], pix.samples)
		images.append(img)

	pdf_document.close()

	return images
