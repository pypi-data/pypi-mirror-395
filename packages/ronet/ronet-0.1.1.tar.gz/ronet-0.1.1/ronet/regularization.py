import numpy as np

# regularization
# l1 and l2 regularization already added in dense layer and loss function
from typing import Optional

class Dropout:
    """
    Dropout Layer.

    Randomly sets input units to 0 with a frequency of `rate` at each step 
    during training time, which helps prevent overfitting.

    This implementation uses **Inverted Dropout**. This means we scale the 
    activations by `1/(1-rate)` during training. This ensures that during 
    inference (testing), we can simply pass the data through without any 
    scaling, making prediction faster and simpler.

    Parameters
    ----------
    rate : float
        The probability of dropping a neuron (0 < rate < 1). 
        E.g., rate=0.2 means 20% of neurons will be zeroed out.
    """
    def __init__(self, dropout_rate: float):
        self.dropout_rate = 1 - dropout_rate    # stored as inverted rate (ratio of neurons to keep)
    
    def forward(self, inputs: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Applies the dropout mask.

        Parameters
        ----------
        inputs : np.ndarray
            Input tensor.
        training : bool
            If True, applies dropout. If False, returns inputs unchanged.
        """
        self.inputs = inputs
        if not training :
            self.output = inputs.copy()
            return
        
        self.binary_mask = np.random.binomial(1, self.dropout_rate, inputs.shape)/self.dropout_rate
        self.output = self.inputs * self.binary_mask

    def backward(self, prev_grads: np.ndarray) -> None:
        """
        Backpropagates gradients. 
        Gradients strictly flow only through the neurons that were NOT dropped.
        """
        self.dinputs = prev_grads  * self.binary_mask

class BatchNorm:
    """
    Batch Normalization Layer.

    Normalize the activations of the previous layer at each batch, i.e. applies 
    a transformation that maintains the mean activation close to 0 and the 
    activation standard deviation close to 1.

    Equations:
    1. Calculate Batch Mean: mu = (1/m) * sum(x)
    2. Calculate Batch Variance: var = (1/m) * sum((x - mu)^2)
    3. Normalize: x_hat = (x - mu) / sqrt(var + epsilon)
    4. Scale and Shift: y = gamma * x_hat + beta

    During inference (training=False), it uses a moving average of the mean 
    and variance tracked during training.

    Parameters
    ----------
    epsilon : float, optional
        Small float added to variance to avoid dividing by zero. Default 1e-7.
    momentum : float, optional
        Momentum for the moving average of the mean and variance. Default 0.99.
    """
    # normalizes data to 0 mean and unit std deviation
    # adds regulariztion
    # allows for more aggresive learning rates
    def __init__(self, epsilon: float = 1e-7, momentum: float = 0.99):
        self.epsilon = epsilon
        self.gamma = None       # scaling parameter learnable parameter
        self.beta = None        # shift parameter   both of them neccessary to regain the lost dimensions
        self.trainable = True

        # Running statistics for inference
        self.running_mean: Optional[np.ndarray] = None
        self.running_var: Optional[np.ndarray] = None
    
    def forward(self, inputs: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Parameters
        ----------
        inputs : np.ndarray
            Input batch of shape (batch_size, n_features).
        training : bool
            If True, normalizes using batch statistics and updates running stats.
            If False, normalizes using running statistics.
        """
        if not training:
            self.output = inputs
            return
        if self.gamma is None:
            _, features = inputs.shape
            self.gamma = np.ones((1, features))
            self.beta  = np.zeros((1, features))
            self.running_mean = np.zeros((1, features))
            self.running_var = np.ones((1, features))

        self.inputs = inputs
        self.samples = len(input)
        if training:
            self.sample_mean = np.mean(inputs, axis=0, keepdims=True)                   # shape( 1,  n_neurons)
            self.sample_var = np.var(inputs, axis=0, keepdims=True)     # shape (1, n_neurons)

            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * self.sample_mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * self.sample_var

            mean = self.sample_mean
            var = self.sample_var
        else:
            # Use running statistics for inference
            mean = self.running_mean
            var = self.running_var

        self.x_mu = inputs - mean                              # shape (m, n_neurons)
        self.std_inv = 1.0 / np.sqrt(var + self.epsilon)      # shape(1, n_neurons)
        self.x_hat = self.x_mu * self.std_inv                       # shape (m, n_neurons)      broadcasting done

        self.output = self.gamma * self.x_hat + self.beta   # shape (m, n_neurons)
        return self.output

    def backward(self, prev_grads: np.ndarray) -> None:
        """
        Calculates gradients for Gamma, Beta, and Inputs.

        The gradient calculation for BatchNorm is complex because the means
        and variances depend on the inputs.
        """
        batch_size = len(prev_grads)

        # Gradient w.r.t. learnable parameters
        self.dgamma = np.sum(prev_grads * self.x_hat, axis=0, keepdims=True)
        self.dbeta = np.sum(prev_grads, axis=0, keepdims=True)

        # Gradient w.r.t. inputs
        # We use the optimized derivation for performance
        # dL/dx = (1/m * std_inv) * ( m * dL/dx_hat - sum(dL/dx_hat) - x_hat * sum(dL/dx_hat * x_hat) )
        
        dx_hat = prev_grads * self.gamma
        
        self.dinputs = (self.std_inv / batch_size) * (
            batch_size * dx_hat - 
            np.sum(dx_hat, axis=0, keepdims=True) - 
            self.x_hat * np.sum(dx_hat * self.x_hat, axis=0, keepdims=True)
        )
