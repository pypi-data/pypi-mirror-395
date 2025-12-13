from pathlib import Path
from pdf2image import convert_from_path

class Pdf2Img:

    def __init__(self, pdf, ouput, password= None) -> None:
        self.pdf = Path(pdf)
        self.output = Path(ouput)
        self.password = password
    

    def extrat_image(self):
        """
        Docstring for extrat_image

        The objective of this method is to get images from Path
        
        :param self: Description
        """
        self.images = convert_from_path(self.pdf, userpw=self.password)

    def to_image(self):
        """
        Docstring for to_image

        The objective of this method is to convert all pdf into high-quality images
        
        :param self: Description
        """
        self.extrat_image()
        for page,i in zip(self.images,range(len(self.images)+1)):
            name_pdf = self.pdf.name.split('.')[0]
            if not self.output.is_dir():
                self.output.mkdir(parents=True, exist_ok=True)
                
            name = self.output / name_pdf
            
            page.save(f"./{name}_{i}.png", 'JPEG')
            print(f"save image : ./{name}_{i}.png")