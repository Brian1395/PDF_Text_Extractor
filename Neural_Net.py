import numpy as np
import PIL
from ImageStandardizer import ImageStandardizer

path_to_training_data = "C:\\Users\\brian\\Documents\\GitHub\\PDF_Text_Extractor\\TrainingData\\I0.jpg"
#path_to_weights = "C:\\Users\\brian\\Documents\\GitHub\\PDF_Text_Extractor"
#path_to_biases = "C:\\Users\\brian\\Documents\\GitHub\\PDF_Text_Extractor"

#Net Constants
##NUMBER_OF_NET_LAYERS = 3 #2 intermediate and 1 output
##LAYER_SIZES = [10, 10, 26] #
##INPUT_IMAGE_SIZE = (28, 28) #

#Testing Constants. (Much easier to visualize)
NUMBER_OF_NET_LAYERS = 2
LAYER_SIZES = [3, 2] #
INPUT_IMAGE_SIZE = (2, 2) #

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

4## Takes a prevous layer, the corresponding weights, and the biases of the next layer and returns that new layer
def calc_activation(prev_layer, weights, bias):
    raw = np.matmul(weights, prev_layer) + bias
    post_sigmoid = 1/(1+np.exp(-raw))
    return(post_sigmoid)

## Saves the provided weights and biases provided to files in the active directory to be retrived later
def save_layer(weights, biases, depth):
    name_base = "layer" + str(depth)
    np.save(name_base + "weigths", weights)
    np.save(name_base + "biases", biases)
    return

## Retrives the saved weights and biases given any layer depth (input layer is 0)
def load_layer(depth):
    name_base = "layer" + str(depth)
    weights = np.load(name_base + "weigths.npy")
    biases = np.load(name_base + "biases.npy")
    return(weights, biases)

## Initalizes the random values for biases and weights
def make_random_net():
    check = input('This will overwrite any saved weights and baises you currently have. Are you sure you wish to continue? (y/n) ')
    if(check == 'y'):
        for i in range(NUMBER_OF_NET_LAYERS): #For each layer create the weights and biases
            if(i == 0):
                prev_layer_size = INPUT_IMAGE_SIZE[0] * INPUT_IMAGE_SIZE[1]
            else:
                prev_layer_size = LAYER_SIZES[i - 1]

            curr_layer_size = LAYER_SIZES[i]

            biases = np.random.rand(curr_layer_size, prev_layer_size)

            weights = np.random.uniform(-1, 1, (curr_layer_size))

            save_layer(weights, biases, i + 1)

            

#img = ImageStandardizer().convert_from_file(path_to_training_data)



##Testing Bits
example_layer = np.array([0,1,0.5])
example_weights = np.array([[1,1,1],
                            [0,0,0],
                            [0.5,1,0.5]])
example_biases = [-.5, 1, -0.25]

#make_random_net()

#load_layer()

#save_layer(example_weights, example_biases, 2)

#calc_activation(example_layer, example_weights, example_biases)


#calc_cost(example_output, example_goal)
#input_array = image_to_array(ImageStandardizer().convert_from_file(path_to_training_data))
