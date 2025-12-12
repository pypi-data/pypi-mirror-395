import numpy as np
from typing import Optional

# dense layer
class Dense:
    """
    A fully connected (dense) layer.
    
    This layer implements the operation: output = dot(input, kernel) + bias.
    It supports L1 and L2 regularization for both weights and biases.

    The weights are initialized using Xavier (Glorot) Uniform initialization,
    drawing samples from a uniform distribution within [-limit, limit] where
    limit is sqrt(6 / (fan_in + fan_out)).

    Parameters
    ----------
    n_in : int
        The dimensionality of the input space (number of input features).
    n_neurons : int
        The number of neurons (units) in this layer; determines the output dimensionality.
    weight_regularizer_l1 : float, optional
        L1 regularization factor for the weights. Default is 0.
    bias_regularizer_l1 : float, optional
        L1 regularization factor for the biases. Default is 0.
    weight_regularizer_l2 : float, optional
        L2 regularization factor for the weights. Default is 0.
    bias_regularizer_l2 : float, optional
        L2 regularization factor for the biases. Default is 0.

    Attributes
    ----------
    weights : np.ndarray
        The weight matrix of shape (n_in, n_neurons).
    biases : np.ndarray
        The bias vector of shape (1, n_neurons).
    trainable : bool
        Flag indicating if the layer's parameters should be updated during training.
    inputs : np.ndarray
        Stored input from the forward pass, used for backpropagation.
    output : np.ndarray
        The result of the forward pass.
    dweights : np.ndarray
        Gradients with respect to weights, calculated during backward pass.
    dbiases : np.ndarray
        Gradients with respect to biases, calculated during backward pass.
    dinputs : np.ndarray
        Gradients with respect to inputs (to pass to the previous layer).
    """
    def __init__(self, n_in: int, n_neurons: int, 
                 weight_regularizer_l1: float = 0, bias_regularizer_l1: float = 0, 
                 weight_regularizer_l2: float = 0, bias_regularizer_l2: float = 0):
        upper = (np.sqrt(6/(n_in + n_neurons)))
        lower = -upper
        # Xavier Initialization
        self.weights = np.random.uniform(lower, upper, (n_in, n_neurons))    # w^T shape
        self.biases = np.zeros((1, n_neurons))              # b^T shape

        self.weight_regularizer_l1 = weight_regularizer_l1
        self.bias_regularizer_l1 = bias_regularizer_l1
        self.weight_regularizer_l2 = weight_regularizer_l2
        self.bias_regularizer_l2 = bias_regularizer_l2

        self.trainable = True

    def __call__(self, inputs):
        """
        Convenience wrapper for the forward method.
        """
        self.output = np.dot(inputs, self.weights) + self.biases
        return self.output
    
    def forward(self, inputs, training = True):
        """
        Performs the forward pass of the layer.

        Calculates Y = XW + b.

        Parameters
        ----------
        inputs : np.ndarray
            Input tensor of shape (batch_size, n_in).
        training : bool, optional
            Flag to indicate if the model is in training mode. 
            (Kept for consistency with layers like Dropout, though unused here).

        Returns
        -------
        np.ndarray
            Output tensor of shape (batch_size, n_neurons).
        """
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases
        return self.output
         
    def backward(self, prev_grads):
        """
        Performs the backward pass (backpropagation).

        Calculates gradients for weights, biases, and inputs. 
        Applies L1 and L2 regularization derivatives if parameters are set.

        Parameters
        ----------
        prev_grads : np.ndarray
            Gradient of the loss function with respect to the output of this layer.
            Shape: (batch_size, n_neurons).

        Notes
        -----
        This method updates the instance attributes:
        - self.dweights: Gradient w.r.t weights.
        - self.dbiases: Gradient w.r.t biases (summed over the batch).
        - self.dinputs: Gradient w.r.t inputs (to be propagated to the previous layer).
        """
        self.dweights = np.dot(self.inputs.T, prev_grads)       # inputs.T = (no. of features, no. of samples)
        self.dbiases = np.sum(prev_grads, axis=0, keepdims=True)    # sum over columns (i.e wrt to each neuron)
        # gradients on inputs
        # each dinputi will be sum over dai*wi for all neurons, da is upstream gradient
        # upstream grad shape = (m , self.n_neurons) 
        # self.weights.T shape = (self.n_neurons, self.n_in)
        # dinputs shape = (m, self.n_in)    [n_in are the n_neurons for prev layer]
        self.dinputs = np.dot(prev_grads, self.weights.T)   # required to propogate gradients


        # if l1 regularization used
        if self.weight_regularizer_l1 > 0:
            l1_dweights = np.ones_like(self.weights)
            l1_dweights[self.weights < 0] = -1
            self.dweights += self.weight_regularizer_l1 * l1_dweights

        if self.bias_regularizer_l1 > 0:
            l1_dbias = np.ones_like(self.biases)
            l1_dbias[self.biases < 0] = -1
            self.dbiases += self.bias_regularizer_l1 * l1_dbias

        if self.weight_regularizer_l2 > 0:
            self.dweights += 2 * self.weight_regularizer_l2 * self.weights

        if self.bias_regularizer_l2 > 0:
            self.dbiases += 2 * self.bias_regularizer_l2 * self.biases

    def __repr__(self):
        return f"Dense Layer ({self.weights.shape[0]} -> {self.weights.shape[1]})"
    
    def __str__(self):
        return self.__repr__()
