from pdf2img_cli.pdf2img import Pdf2Img


def main(pdf, ouput, password = None):

	pdf2img = Pdf2Img(pdf, ouput, password)
	pdf2img.to_image()