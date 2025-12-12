import numpy as np
from typing import Optional

# activation functions

class Linear:
    """
    Linear (Identity) activation function.
    
    This function returns the input unchanged: f(x) = x.
    It is typically used on the output layer for regression tasks.
    """
    def __call__(self, inputs: np.ndarray) -> np.ndarray:
        return inputs
    
    def forward(self, inputs: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Passes inputs through unchanged.
        """
        self.output = inputs
    
    def backward(self, prev_grads: np.ndarray) -> None:
        """
        The derivative of f(x) = x is 1.
        Therefore, gradients form the next layer are passed back unchanged.
        """
        self.dinputs =  prev_grads.copy()
    
    def predict(self, outputs: np.ndarray) -> np.ndarray:
        """
        Returns the raw outputs (regression values).
        """
        return outputs

class ReLU:
    """
    Rectified Linear Unit (ReLU) activation function.

    f(x) = max(0, x)

    This is the most common activation function for hidden layers in deep learning.
    It solves the vanishing gradient problem found in Sigmoid/Tanh by having 
    a constant gradient of 1 for positive inputs.
    """
    def __call__(self, inputs: np.ndarray) -> np.ndarray:
            self.output = np.maximum(0, inputs)
            return self.output
    
    def forward(self, inputs: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Applies f(x) = max(0, x) element-wise.
        """
        # relu = 0 for x < 0
        #      = x for x >= 0
        self.output = np.maximum(0, inputs)
        return self.output
    
    def backward(self, prev_grads: np.ndarray) -> None:
        """
        Calculates gradients.
        
        Derivative:
        f'(x) = 1 if x > 0
        f'(x) = 0 if x <= 0
        """
        #prev_grads shape = (m , self.n_neurons)
        #self.outputs shape = (m , self.n_neurons)
        self.dinputs = prev_grads.copy()
        # dinputs = self.output * prev_grad         ---- element wise multiplication not dot product
        self.dinputs[self.output <= 0] = 0 
    
    def predict(self, outputs: np.ndarray) -> np.ndarray:
        return outputs

class Sigmoid:
    """
    Sigmoid activation function.

    f(x) = 1 / (1 + e^-x)

    Squashes inputs to the range (0, 1). often used for binary classification 
    in the output layer.
    """
    def __init__(self):
        self.output: Optional[np.ndarray] = None
        self.dinputs: Optional[np.ndarray] = None

    def __call__(self, inputs: np.ndarray) -> np.ndarray:
        exp = np.exp(inputs)
        self.output = exp/(exp + 1)
        return self.output

    def forward(self, inputs: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Applies the sigmoid function element-wise.
        """
        # sigmoid(x) = 1/1+e^-x = e^x / 1 + e^x
        exp = np.exp(inputs)
        self.output = exp/(exp + 1)
        return self.output
    
    def backward(self, prev_grads: np.ndarray) -> None:
        """
        Calculates gradients using the derivative of Sigmoid.
        
        f'(x) = f(x) * (1 - f(x))
        """
        # sigmoid(x) = e^x / 1 + e^x
        # sigmoid'(x) = e^x(1 + e^x) * 1/1+e^x
        #             = sigmoid(x) * (1 - sigmoid(x))

        # prev_grads shape = (m , self.n_neurons)
        # self.output shape = (m , self.n_neurons)
        self.dinputs = (self.output*(1-self.output)) * prev_grads   # element-wise multiplication
    
    def predict(self, outputs: np.ndarray) -> np.ndarray:
        """
        Converts probability outputs to binary class labels (0 or 1) 
        using a threshold of 0.5.
        """
        return (outputs > 0.5)*1

class Softmax:
    """
    Softmax activation function.

    Used for multi-class classification. It converts a vector of raw scores (logits)
    into a probability distribution.

    Formula:
    S(x_i) = e^{x_i} / sum(e^{x_j})
    """
    def __init__(self):
        self.output: Optional[np.ndarray] = None
        self.dinputs: Optional[np.ndarray] = None

    def __call__(self, inputs: np.ndarray) -> np.ndarray:
        # sofmax(xi) = e^-
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True)) # to prevent exploding gradients by preventing overflow from exponent function
        norm_values = exp_values/np.sum(exp_values, axis=1, keepdims=True)
        self.output = norm_values
        return self.output
    
    def forward(self, inputs: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Performs the forward pass using the numerically stable Softmax formula.
        """
        # sofmax(xi) = e^-xi / sum(e^xj) j = 1 to n_neurons
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True)) # to prevent exploding gradients by preventing overflow from exponent function
        norm_values = exp_values/np.sum(exp_values, axis=1, keepdims=True)
        self.output = norm_values
        return self.output
    
    def backward(self, prev_grads: np.ndarray) -> None:
        """
        Calculates the gradient of the Softmax function.
        
        Unlike element-wise activations, the Softmax gradient is a Jacobian matrix 
        because the output of one neuron depends on the sum of all other neurons.

        Jacobian J_ij = S_i * (delta_ij - S_j)
        where delta_ij is the Kronecker delta.
        """
        # sofmax(xi) = e^-xi / sum(e^xj) j = 1 to n_neurons
        # dsoftmax(xi)/dxi = softmax(xi)*(1-sofmax(xi))
        # dsoftmax(xi)/dxj = -softmax(xi)*softmax(xj)

        # dsoftmax(xi)dxj = softmax(xi)*(1-sofmax(xi))   i = j
        #                 = -softmax(xi)*softmax(xj)    i != j
        # Kronecker delta function dij = 1 if i = j 
        #                              = 0 i!=j
        # dsoftmax(xi)/dxj = softmax(xi)(dij - softmax(xj))
        #                  = softmax(xi)dij - softmax(xi)softmax(xj)

        # but xi = ipi - max
        # dxi = 1

        # prev_grads shape = (m , n_classes)
        # self.output shape = (m, n_classes)
        self.dinputs = np.empty_like(prev_grads)

        # enumerate outputs and gradients
        for index, (single_output, single_grad) in enumerate(zip(self.output, prev_grads)):
            # flatten output array
            single_output = single_output.reshape(-1,1) # col matrix
            # Jacobian matrix is an array of partial derivatives in all of the combinations of both input vectors.
            # Jacobian matrix of a vector-valued function of several variables is the matrix of all its first-order partial derivatives
            # calculate jacobian matrix of the output s
            # comes from jacobian matrix
            jacobian_matrix = np.diagflat(single_output) - np.dot(single_output, single_output.T)

            # calculate sample-wise gradient
            # and add it to the array of sample gradients
            # here single grad is shape (1, )
            # numpy treats it as column vector when it is on the left of dot product
            self.dinputs[index] = np.dot(jacobian_matrix, single_grad)  # shape(n_classes, 1) but numpy gives shape (1, ) which will be row vector in out context
    
    def predict(self, outputs: np.ndarray) -> np.ndarray:
        """
        Returns the class index with the highest probability.
        """
        return np.argmax(outputs, axis=1)