import numpy as np

class Optimizer:
    """
    Base class for all optimizers.
    """
    def pre_update_params(self) -> None:
        """
        Called before parameter updates. Used for updating learning rate decay.
        """
        pass

    def update_params(self, layer) -> None:
        """
        Update the parameters (weights/biases) of the given layer.
        """
        pass

    def post_update_params(self) -> None:
        """
        Called after parameter updates. Used for stepping the iteration counter.
        """
        pass

class Optimizer_SGD(Optimizer):
    """
    Stochastic Gradient Descent (SGD) optimizer.

    Supports Momentum and Learning Rate Decay.

    Update Rule (with momentum):
    v_{t} = \beta * v_{t-1} - \eta * \nabla J
    W_{t} = W_{t-1} + v_{t}

    Parameters
    ----------
    learning_rate : float
        The initial learning rate ($\eta$). Default is 1.0.
    decay : float
        The decay rate for the learning rate over time ($1 / (1 + decay * step)$).
    momentum : float
        The momentum factor ($\beta$), usually between 0.5 and 0.9. 
        Helps accelerate gradients in the right direction and dampens oscillations.
    """
    
    # momentum prevents model beign stuck in local minima
    # learning rate decay prevents exploding gradients
    def __init__(self, learning_rate: float = 1.0, decay: float = 0., momentum: float = 0.):
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.steps = 0      # how many steps have taken place so far
        self.momentum_factor = momentum 

    # implement a wrapper here if decay
    def pre_update_params(self):
        if self.decay:
            self.current_learning_rate = self.learning_rate * (1. / (1. + self.decay * self.steps))
    
    def update_params(self, layer):
        """
        Performs the update on the layer's weights and biases.

        Notes
        -----
        If momentum is used, this method initializes `weight_momentums` and 
        `bias_momentums` attributes on the layer instance to store velocity.
        """
        # if momentum is used
        if self.momentum_factor:
            # per parameter momentums
            if not hasattr(layer, 'weight_momentums'):
                layer.weight_momentums = np.zeros_like(layer.weights)
                layer.bias_momentums = np.zeros_like(layer.biases)
                            # fraction from previous updates
            weight_updates = (self.momentum_factor*layer.weight_momentums) - (self.current_learning_rate*layer.dweights)   # everything is a vector here
            layer.weight_momentums = weight_updates

            bias_updates = (self.momentum_factor*layer.bias_momentums) - (self.current_learning_rate*layer.dbiases)   # everything is a vector here
            layer.bias_momentums = bias_updates
        # vanilla sgd
        else:
            weight_updates = -self.current_learning_rate * layer.dweights
            bias_updates = -self.current_learning_rate * layer.dbiases

        layer.weights += weight_updates
        layer.biases += bias_updates
    
    def post_update_params(self):
        self.steps += 1

class Optimizer_Adagrad(Optimizer):
    """
    Adagrad Optimizer.

    Adapts the learning rate to the parameters, performing smaller updates
    (i.e. low learning rates) for parameters associated with frequently occurring
    features, and larger updates (i.e. high learning rates) for parameters
    associated with infrequent features.

    Formula:
    Cache += (gradient)^2
    W += -learning_rate * gradient / (sqrt(Cache) + epsilon)
    """
     # reduce the update size in ratio to the previous size of updates for each param
    def __init__(self, learning_rate: float = 1.0, decay: float = 0., epsilon: float = 1e-7):
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.steps= 0
        self.epsilon = epsilon

    def pre_update_params(self):
        if self.decay:
            self.current_learning_rate = self.learning_rate/( 1 + self.steps*self.decay)
        
    def update_params(self, layer):
        # cache is the history of updates
        # the layer wont have a cache to begin with
        if not hasattr(layer, 'weight_cache'):
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_cache = np.zeros_like(layer.biases)
        
        # update cache with current squared gradients
        layer.weight_cache += layer.dweights**2
        layer.bias_cache += layer.dbiases**2

        layer.weights += -(self.current_learning_rate * layer.dweights)/(np.sqrt(layer.weight_cache )+ self.epsilon)
        layer.biases += -(self.current_learning_rate * layer.dbiases)/(np.sqrt(layer.bias_cache) + self.epsilon)

    def post_update_params(self):
        self.steps += 1

class Optimizer_RMSProp(Optimizer):
    """
    RMSProp Optimizer.

    Maintains a moving average of the squared gradients to normalize the gradient.
    This resolves Adagrad's radically diminishing learning rates.

    Formula:
    Cache = rho * Cache + (1 - rho) * (gradient)^2
    W += -learning_rate * gradient / (sqrt(Cache) + epsilon)

    Parameters
    ----------
    rho : float
        Decay rate for the moving average of squared gradients. Default 0.9.
    epsilon : float
        Small value to prevent division by zero.
    """
    
    # Slows down oscillations in dimensions where it high
    # reduce the update size in ratio to the previous size of updates for each param , but in a better way
    # adds a mechanism similar to momentum 
    # calculates per param learning rate 
    # retains global direction and slows changes in direction
    def __init__(self, learning_rate: float = 0.001, decay: float = 0., rho: float = 0.9, epsilon: float = 1e-7):
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.steps = 0      # how many steps have taken place so far
        self.rho = rho      # cache memory decay rate : factor which decides the proportion of previous cache and current gradients squared
        self.epsilon = epsilon

    def pre_update_params(self):
        if self.decay:
            self.current_learning_rate = self.learning_rate*(1./(1. + self.decay*self.steps))
    
    def update_params(self, layer):
        if not hasattr(layer, 'weight_cache'):
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_cache = np.zeros_like(layer.biases)

        # some proportion of previous gradients and some proportion of current gradients
        layer.weight_cache = self.rho*layer.weight_cache + (1-self.rho)*layer.dweights**2
        layer.bias_cache = self.rho*layer.bias_cache + (1-self.rho)*layer.dbiases**2

        # update like Adagrad
        layer.weights += -self.current_learning_rate* layer.dweights/(np.sqrt(layer.weight_cache) + self.epsilon)
        layer.biases += -self.current_learning_rate* layer.dbiases/(np.sqrt(layer.bias_cache) + self.epsilon)

    def post_update_params(self):
        self.steps += 1

class Optimizer_Adam(Optimizer):
    """
    Adam (Adaptive Moment Estimation) Optimizer.

    Combines the advantages of AdaGrad and RMSProp. It calculates an exponential 
    moving average of the gradient and the squared gradient.

    Parameters
    ----------
    beta_1 : float
        Exponential decay rate for the first moment estimates (momentum). Default 0.9.
    beta_2 : float
        Exponential decay rate for the second moment estimates (cache). Default 0.999.
    epsilon : float
        Small value to prevent division by zero.
    """
    def __init__(self, learning_rate: float = 0.001, decay: float = 0., epsilon: float = 1e-7, 
                 beta_1: float = 0.9, beta_2: float = 0.999):
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.steps = 0              # how many steps have taken place so far
        self.epsilon = epsilon
        self.beta_1 = beta_1    #    momentum factor
        self.beta_2 = beta_2            # cache memory decay rate

    def pre_update_params(self):
        if self.decay:
            self.current_learning_rate = self.learning_rate*(1./(1. + self.decay*self.steps))
    
    def update_params(self, layer):
        if not hasattr(layer, 'weight_cache'):
            layer.weight_momentums = np.zeros_like(layer.weights)
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_momentums = np.zeros_like(layer.biases)
            layer.bias_cache = np.zeros_like(layer.biases)
        
        layer.weight_momentums = (self.beta_1*layer.weight_momentums) + ((1-self.beta_1)*layer.dweights)
        layer.bias_momentums = (self.beta_1*layer.bias_momentums) + ((1-self.beta_1)*layer.dbiases)

        # adujst for early small values
        # adaptive momentums - early the momentum will be greater
        weight_momentums_corrected = layer.weight_momentums/(1 - self.beta_1**(self.steps + 1) )# + 1 to avoid div by zero
        bias_momentums_corrected = layer.bias_momentums/(1 - self.beta_1**(self.steps +1))

        layer.weight_cache = self.beta_2*layer.weight_cache + (1-self.beta_2)*layer.dweights**2
        layer.bias_cache = self.beta_2*layer.bias_cache + (1-self.beta_2)*layer.dbiases**2

        # adjust for early small values
        weight_cache_corrected = layer.weight_cache/(1 - self.beta_2**(self.steps + 1) )
        bias_cache_corrected = layer.bias_cache/(1 - self.beta_2**(self.steps +1))

        # param updates : vanilla sgd param update + normalization with sqaure rooted cache
        layer.weights += -self.current_learning_rate* weight_momentums_corrected/(np.sqrt(weight_cache_corrected)+ self.epsilon)
        layer.biases += -self.current_learning_rate*bias_momentums_corrected/(np.sqrt(bias_cache_corrected) + self.epsilon)

    def post_update_params(self):
        self.steps += 1
        