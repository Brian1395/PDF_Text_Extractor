#Written by Brian Goodell, using 3Blue1Brown's neural net overview series as a guide: https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi

import numpy as np
import PIL
from ImageStandardizer import ImageStandardizer

path_to_training_data = "C:\\Users\\brian\\Documents\\GitHub\\PDF_Text_Extractor\\TrainingData\\A0.jpg"
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

## Takes a uppercase char and returns a np array with the ideal result of that classification
def gen_goal(classification):
    alpha_pos = ord(classification) - 65
    blank = np.zeros(26)

    blank[alpha_pos] = 1.0
    
    return(blank)
    

## Takes 2 numpy arrays of the same size and returns the cost
def calc_cost(output,goal):
    sub = output-goal
    sqr = sub.__pow__(2)
    return(np.sum(sqr))

## Takes a prevous layer, the corresponding weights, and the biases of the next layer and returns that new layer's activations
def calc_activation(prev_layer, weights, bias):
    raw = np.matmul(weights, prev_layer) + bias
    post_sigmoid = 1/(1+np.exp(-raw))
    return(post_sigmoid)

## Same as calc_activation() but returns the pre-sigmoid activations aswell
def calc_activation_plus(prev_layer, weights, bias):
    raw = np.matmul(weights, prev_layer) + bias
    post_sigmoid = 1/(1+np.exp(-raw))
    return (post_sigmoid, raw)

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

            weights = np.random.rand(curr_layer_size, prev_layer_size)

            biases = np.random.uniform(-1, 1, (curr_layer_size))

            save_layer(weights, biases, i + 1)

def classify_image(img, net): #Takes PIL image and neural net in form list with each layer (tuple weights, biases) as an item
    prev_layer = image_to_array(img)
    
    for layer in net:
        layer_activation = calc_activation(prev_layer, layer[0], layer[1])
        prev_layer = layer_activation

    print(layer_activation)

def classify(input_array, net): #Takes PIL image and neural net in form list with each layer (tuple weights, biases) as an item
    prev_layer = input_array
    
    for layer in net:
        layer_activation = calc_activation(prev_layer, layer[0], layer[1])
        prev_layer = layer_activation

    return(layer_activation)

def classify_plus(input_array, net): #Same as classify() but returns the layer activations
    prev_layer = input_array
    layer_activations = [input_array]
    pre_sigmoids = []
    
    for layer in net:
        layer_activation, pre_sigmoid = calc_activation_plus(prev_layer, layer[0], layer[1])
        layer_activations.append(layer_activation)
        pre_sigmoids.append(pre_sigmoid)
        prev_layer = layer_activation

    return(layer_activations,pre_sigmoids)

def train_one(training_array, classification, net):
    layer_activations, pre_sigmoids = classify_plus(training_array, net)
    prediction = layer_activations[-1]
    goal = np.array([1,0])#gen_goal(classification)
    
    cost = calc_cost(prediction, goal)
    print("Prediction: ", prediction, '\n', "Goal: ", goal, "\nPrev Layer: ", layer_activations[-2], "\n\n")
    #print(layer_activations)

    weight_ders = []
    bias_ders = []

    for i in range(len(layer_activations[-1])):
        x = layer_activations[-1][i]
        weight_der = 2 * layer_activations[-2] * (pre_sigmoids[-2] * (1 - pre_sigmoids[-2])) * (x - goal[i])
        bias_der = 2 * (pre_sigmoids[-2] * (1 - pre_sigmoids[-2])) * (x - goal[i])
        
        print("Node " + str(i) + ":\n", weight_der, "\n", np.mean(bias_der))
        weight_ders.append(weight_der)
        bias_ders.append(np.mean(bias_der))

    #I don't think this is too useful, but it's very interesting to see that the averages are the same, regardless of if the goal is [1,0] or [0,1] for some reason
    print("Averages:") 
    print((weight_ders[0] + weight_ders[1])/len(weight_ders))
    print((bias_ders[0] + bias_ders[1])/len(bias_ders))

    
#img = ImageStandardizer().convert_from_file(path_to_training_data)



##Testing Bits
example_image_array = np.array([0,1,0,1])
example_layer = np.array([0,1,0.5])
example_weights = np.array([[1,1,1],
                            [0,0,0],
                            [0.5,1,0.5]])
example_biases = [-.5, 1, -0.25]

train_one(example_image_array, 'A', [(load_layer(1)),(load_layer(2))])

#classify(example_image_array, [(load_layer(1)),(load_layer(2))])

#make_random_net()

#print(load_layer(1))

#save_layer(example_weights, example_biases, 2)

#calc_activation(example_layer, example_weights, example_biases)


#calc_cost(example_output, example_goal)
#input_array = image_to_array(ImageStandardizer().convert_from_file(path_to_training_data))
