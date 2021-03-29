import PIL
from PIL import Image


class ImageStandardizer:
    def __init__(self):
        self.output_size = (28, 28)

    def convert_from_file(self, location):
        self.input_image = Image.open(location)

        self.output_img = self.input_image.resize(self.output_size)
        self.output_img = self.output_img.convert('L')

        return(self.output_img)
