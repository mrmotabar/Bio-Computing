#Importing Libraries
import numpy as np #For calculations
import sklearn #For the dataset
from sklearn import datasets
import matplotlib.pyplot as plt #For plotting
from random import sample
from mpl_toolkits import mplot3d #For 3D plotting

#%matplotlib inline
#Generating the dataset
np.random.seed(0)
x, y = sklearn.datasets.make_moons(200, noise=0.20)
#plt.scatter(x[:,0], x[:,1], s=40, c=y, cmap=plt.cm.Spectral)
#plt.show()

num_examples = len(x) # training set size
nn_input_dim = 2 # input layer dimensionality
nn_output_dim = 2 # output layer dimensionality
# Gradient descent parameters (I picked these by hand)
epsilon = 0.01 # learning rate for gradient descent
reg_lambda = 0.01 # regularization strength

nn_hdim = [nn_input_dim, 3, 3, nn_output_dim]


def calculate_loss(model):
    W = []
    b = []
    for i in range(len(nn_hdim) - 1):
        W.append(model['W' + str(i)])
        b.append(model['b' + str(i)])
    # Forward propagation to calculate our predictions
    a = []
    z = []
    a.append(x)
    for i in range(len(nn_hdim) - 2):
        z.append(a[-1].dot(W[i]) + b[i])
        a.append(np.tanh(z[-1]))
    z.append(a[-1].dot(W[-1]) + b[-1])
    exp_scores = np.exp(z[-1])
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    # Calculating the loss
    corect_logprobs = -np.log(probs[range(num_examples), y])
    data_loss = np.sum(corect_logprobs)
    # Add regulatization term to loss (optional)
    temp = 0
    for i in range(len(nn_hdim) - 1):
        np.sum(np.square(W[i]))
    data_loss += reg_lambda/2 * (temp)
    return 1./num_examples * data_loss

# Helper function to predict an output (0 or 1)
def predict(model, X):
    W = []
    b = []
    for i in range(len(nn_hdim) - 1):
        W.append(model['W' + str(i)])
        b.append(model['b' + str(i)])
    # Forward propagation
    a = []
    z = []
    a.append(X)
    for i in range(len(nn_hdim) - 2):
        z.append(a[-1].dot(W[i]) + b[i])
        a.append(np.tanh(z[-1]))
    z.append(a[-1].dot(W[-1]) + b[-1])
    exp_scores = np.exp(z[-1])
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    return np.argmax(probs, axis=1)

#This function learns parameters for the neural network and returns the model.
#- nn_hdim: Number of nodes in the hidden layer
#- num_passes: Number of passes through the training data for gradient descent
#- print_loss: If True, print the loss every 1000 iterations
def build_model(nn_hdim, num_passes=20000, print_loss=False):
    #Initialize the parameters to random values. We need to learn these.
    global epsilon
    np.random.seed(0)
    W = [np.random.randn(nn_hdim[i], nn_hdim[i + 1]) / np.sqrt(nn_hdim[i]) for i in range(len(nn_hdim) - 1)]
    b = [np.zeros((1, nn_hdim[i])) for i in range(1, len(nn_hdim))]
    #This is what we return at the end
    model = {}
    #Gradient descent. For each batch...
    for i in range(0, num_passes):
        # Forward propagation
        a = []
        z = []
        a.append(x)
        for j in range(len(nn_hdim) - 2):
            z.append(a[-1].dot(W[j]) + b[j])
            a.append(np.tanh(z[-1]))
        z.append(a[-1].dot(W[-1]) + b[-1])
        exp_scores = np.exp(z[-1])
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        # Backpropagation
        delta = [0] * len(nn_hdim)
        dW = [0] * (len(nn_hdim) - 1)
        db = [0] * (len(nn_hdim) - 1)
        delta[len(nn_hdim) - 1] = probs
        delta[len(nn_hdim) - 1][range(num_examples), y] -= 1
        dW[len(nn_hdim) - 2] = (a[len(nn_hdim) - 2].T).dot(delta[len(nn_hdim) - 1])
        db[len(nn_hdim) - 2] = np.sum(delta[len(nn_hdim) - 1], axis=0, keepdims=True)
        for j in range(len(nn_hdim) - 2, 0, -1):   
            delta[j] = delta[j + 1].dot(W[j].T) * (1 - np.power(a[j], 2))
            dW[j - 1] = np.dot(a[j - 1].T, delta[j])
            db[j - 1] = np.sum(delta[j], axis=0)
        # Add regularization terms (b1 and b2 don't have regularization terms)
        for j in range(len(nn_hdim) - 1):
            dW[j] += reg_lambda * W[j]
        # Gradient descent parameter update
        for j in range(len(nn_hdim) - 1):
            W[j] += -epsilon * dW[j]
            b[j] += -epsilon * db[j]
        if i % 20 == 0:
            epsilon *= 0.9998
        # Assign new parameters to the model
        for j in range(len(nn_hdim) - 1):
            model['W' + str(j)] = W[j]
            model['b' + str(j)] = b[j]
        # Optionally print the loss.
        # This is expensive because it uses the whole dataset.
        if print_loss and i % 1000 == 0:
            print ("Iteration:", i, "Loss:", calculate_loss(model))
    return model

def find_boundary_in(model, x):
    s = -1.5
    e = 1.5
    while e - s > 0.00001:
        mid = (s + e) / 2
        if predict(model, np.array([[x, mid]])) == [0]:
            e = mid
        else:
            s = mid
    return e


def Draw_decision_boundary(model, file_name):
    x1 = []
    x2 = []
    for i in np.arange(-2.0, 2.5, 0.001):
        x1.append(i)
        x2.append(find_boundary_in(model, i))
    plt.scatter(x[:,0], x[:,1], s=40, c=y, cmap=plt.cm.Spectral) 
    plt.plot(x1, x2)
    #plt.show()
    plt.savefig(file_name + ".jpg")
    #plt.clf()


model = build_model(nn_hdim, 20000, True)
Draw_decision_boundary(model, "7")
