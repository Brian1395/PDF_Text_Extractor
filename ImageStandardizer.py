import PIL
from PIL import Image


class ImageStandardizer:
    def __init__(self):
        self.output_size = (28, 28)

    def convert_from_file(self, location):
        self.input_image = Image.open(location)

        self.input_image.thumbnail(self.output_size, Image.ANTIALIAS)
        self.output_img = Image.new('L', (28, 28), (255)) #I assume it'll be better for the neural net if the backgrounds are consistently white, but maybe the algorthim would improve if it could identify the bufferspace. An experiement for another time?
        
        self.x_offset = int((28 - self.input_image.width) / 2)
        self.y_offset = int((28 - self.input_image.height) / 2)
        
        self.output_img.paste(self.input_image, (self.x_offset, self.y_offset))#img.crop((-10,0,28,28)), )

        return(self.output_img)
