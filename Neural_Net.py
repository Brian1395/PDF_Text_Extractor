import numpy as np
import PIL
from ImageStandardizer import ImageStandardizer

path_to_training_data = "C:\\Users\\brian\\Documents\\GitHub\\PDF_Text_Extractor\\TrainingData\\A0.jpg"


#   DONE - Make image sizes consistent
#Neural Net training
    #   DONE - Cost Function
#Yeah... other stuff
    #Sliding window? Maybe too advanced




## Takes a PIL Image and converts it to a np array for use as the input nodes
def image_to_array(img):
    org_array = np.array(img)
    new_array = org_array.flatten()/255
    return(new_array)

## Takes 2 numpy arrays of the same size and returns the cost
def calc_cost(output,goal):
    sub = output-goal
    sqr = sub.__pow__(2)
    return(np.sum(sqr))


calc_cost(example_output, example_goal)
#input_array = image_to_array(ImageStandardizer().convert_from_file(path_to_training_data))
