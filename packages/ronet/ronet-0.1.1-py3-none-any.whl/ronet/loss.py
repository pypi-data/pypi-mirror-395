import numpy as np
from .activations import Softmax
from typing import Optional


class Loss:
    """
    Abstract base class for all loss functions.

    Handles the calculation of data loss, accumulated loss tracking, and L1/L2
    regularization loss across all trainable layers.
    """
    def __init__(self):
        self.accumulated_sum: float = 0.0
        self.accumulated_count: int = 0
        self.trainable_layers: list =  []

    # calculates the data and regularization losses
    # given model output and ground truth values

    def calculate(self, output: np.ndarray, y: np.ndarray, *, include_regularization: bool = False) :
        """
        Calculates the mean data loss for the batch and optionally the total loss
        including regularization.

        Parameters
        ----------
        output : np.ndarray
            Predicted values from the model, shape (batch_size, n_outputs).
        y : np.ndarray
            Ground truth values (targets), shape (batch_size,) or (batch_size, n_outputs).
        include_regularization : bool, optional
            If True, returns the total loss (Data Loss + Regularization Loss).
            The default is False.

        Returns
        -------
        float or tuple of float
            The mean data loss, or (mean data loss, regularization loss) if 
            `include_regularization` is True.
        """
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses)

        self.accumulated_sum += np.sum(sample_losses)
        self.accumulated_count += len(sample_losses)

        if not include_regularization:
            return data_loss
        return data_loss, self.regularization_loss()
    
    def calculate_accumulated(self, *, include_regularization: bool = False):
        """
        Calculates the mean loss over all accumulated samples since the last reset.

        Returns
        -------
        float or tuple of float
            The accumulated mean data loss, or (mean data loss, regularization loss) 
            if `include_regularization` is True.
        
        Raises
        ------
        ZeroDivisionError
            If no samples have been accumulated (`self.accumulated_count == 0`).
        """
        data_loss = self.accumulated_sum / self.accumulated_count

        if not include_regularization:
            return data_loss

        return data_loss, self.regularization_loss()
    
    def reset(self) -> None:
        """
        Resets the accumulated loss tracking variables.
        """
        self.accumulated_count = 0
        self.accumulated_sum = 0

    def remember_trainable_layers(self, trainable_layers: list) -> None:
        """
        Stores references to all layers that have parameters (weights/biases)
        for regularization loss calculation.

        Parameters
        ----------
        trainable_layers : list of TrainableLayer
            A list of layer objects (e.g., Dense) that have `weights` and 
            `biases` attributes.
        """
        self.trainable_layers = trainable_layers
    
    def regularization_loss(self) -> float:
        """
        Calculates the total L1 and L2 regularization loss for all trainable layers.

        The total regularization loss is the sum of regularization terms for
        all weights and biases across all layers.

        Returns
        -------
        float
            The total regularization loss value.
        """
        # total data_loss = regularization_loss(layer1) + regularization_loss(layer2) + ..... n

        regularization_loss = 0
        for layer in self.trainable_layers:
        # if l1 regularization used
            if layer.weight_regularizer_l1 > 0:
                regularization_loss += layer.weight_regularizer_l1 * np.sum(np.abs(layer.weights))
            if layer.bias_regularizer_l1 > 0:
                regularization_loss += layer.bias_regularizer_l1 * np.sum(np.abs(layer.biases))

            # if l2_regularization used
            if layer.weight_regularizer_l2 > 0:
                regularization_loss += layer.weight_regularizer_l2 * np.sum(layer.weights * layer.weights)
            if layer.bias_regularizer_l2 > 0:
                regularization_loss += layer.bias_regularizer_l2 * np.sum(layer.biases * layer.biases)
        
        return regularization_loss

class CrossEntropyLoss(Loss):
    """
    Categorical Cross-Entropy Loss, typically used with Softmax activation
    for multi-class classification problems.

    Formula (for a single sample and target class i):
    L = -log(P_i)
    """
    def __init__(self):
        super().__init__()
        self.dinputs: Optional[np.ndarray] = None

    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """
        Calculates the negative log likelihood (loss) for each sample.

        Parameters
        ----------
        y_pred : np.ndarray
            Predicted probabilities (e.g., Softmax output), shape (batch_size, n_classes).
        y_true : np.ndarray
            Ground truth labels, either sparse (batch_size,) or one-hot (batch_size, n_classes).

        Returns
        -------
        np.ndarray
            An array of loss values for each sample, shape (batch_size,).
        """
        samples = len(y_pred)

        # to prevent division by zero(log(0)) 
        clipped_output = np.clip(y_pred, 1e-07, 1-1e-07)    # 1-1e-07 becuase if there is some epsilon addition the log(x > 1) will be negative instead of 0

        # Probablities for target values -
        # only if categorical labels    i.e true class index for each sample
        if len(y_true.shape) == 1:
            correct_confidences = clipped_output[range(samples), y_true]    # y_true only contains the incide of true class
        elif len(y_true.shape) ==2:     # contains one-hot encoded labels OR true probability distribution
            # mask the valus
            correct_confidences = np.sum(clipped_output*y_true, axis=1)
        
        #losses
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods
    
    def backward(self, y_pred: np.ndarray, y_true: np.ndarray) -> None:
        """
        Calculates the gradient of the loss with respect to the input predictions.

        Gradient formula (simplified for one-hot encoded y_true):
        dL/dP_i = -y_i / P_i
        """
        samples = len(y_pred)       # number of samples m
        labels = len(y_pred[0])     # number of classes c
        clipped_y_pred = np.clip(y_pred, 1e-07, 1-1e-07)

        # prev_grad shape = (m, c)

        # if labels are sparse convert to one hot encoding
        if len(y_true.shape) == 1:
            y_true = np.eye(labels)[y_true]         #[y_true] reorders the values of I to match the hot encoding
        
        self.dinputs = -y_true / clipped_y_pred

        # normalization of gradients
        self.dinputs = self.dinputs/samples

class BinaryCrossEntropyLoss(Loss):
    """
    Binary Cross-Entropy Loss, typically used with Sigmoid activation
    for binary classification problems (two classes).

    Formula (for a single sample):
    L = - (y * log(P) + (1 - y) * log(1 - P))
    """
    def __init__(self):
        super().__init__()
        self.dinputs: Optional[np.ndarray] = None

    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """
        Calculates the mean BCE loss for each sample across all output nodes.
        """
        samples = len(y_pred)

        # to prevent division by zero(log(0))   
        y_pred_clipped = np.clip(y_pred, 1e-07, 1-1e-07)    # 1-1e-07 becuase if there is some epsilon addition the log(x > 1) will be negative instead of 0

        sample_losses = y_true*np.log(y_pred_clipped) + (1- y_true)*np.log(1- y_pred_clipped)
        sample_losses = -np.mean(sample_losses, axis=-1)
        return sample_losses
    
    def backward(self, y_pred: np.ndarray, y_true: np.ndarray) -> None:
        """
        Calculates the gradient of the BCE loss with respect to the input predictions.

        Gradient formula (for a single output P):
        dL/dP = - (y / P - (1 - y) / (1 - P))
        """
        samples = len(y_pred)       # number of samples m
        outputs = len(y_pred[0])     # number of classes c
        clipped_ypred = np.clip(y_pred, 1e-7,1 - 1e-7)
        self.dinputs = -(y_true / clipped_ypred - (1- y_true)/(1- clipped_ypred))/ outputs
        self.dinputs = self.dinputs / samples

class MeanSquaredErrorLoss(Loss):
    """
    Mean Squared Error (MSE) Loss, also known as L2 Loss.

    Typically used for regression problems.

    Formula:
    L = (1/N) * sum((y_true - y_pred)^2)
    """
    def __init__(self):
        super().__init__()
        self.dinputs: Optional[np.ndarray] = None

    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """
        Calculates the squared difference for each sample and takes the mean across output features.
        """
        sample_losses = np.mean((y_true - y_pred)**2, axis = -1, keepdims=True)
        return sample_losses
    
    def backward(self, y_pred: np.ndarray, y_true: np.ndarray) -> None:
        """
        Calculates the gradient of the MSE loss with respect to the input predictions.

        Gradient formula:
        dL/dP = (-2/M) * (y_true - y_pred)
        """
        samples = len(y_pred)
        outputs = len(y_pred[0])
        
        if len(y_true.shape) == 1:
            y_true = y_true.reshape(-1,1)

        self.dinputs = -2 * (y_true - y_pred)/ outputs
        # loss over whole batch
        self.dinputs = self.dinputs / samples

# Softmax classifier - combined Softmax activation
# and cross-entropy loss for faster backward step
# no jacobian calculation involved
class Activation_Softmax_Loss_Cross_Entropy:
    """
    A numerically optimized and stable combination of the Softmax activation 
    function and the Categorical Cross-Entropy Loss.

    This avoids calculating the Jacobian matrix of Softmax and simplifies
    the combined backward gradient calculation.

    Combined Gradient Formula:
    dL/dZ = P - Y
    (Predicted probabilities P minus the one-hot encoded true labels Y)
    """
    def __init__(self):
        self.activation = Softmax()
        self.loss = CrossEntropyLoss()
    
    def forward(self, inputs: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """
        Performs the Softmax forward pass and calculates the Cross-Entropy Loss.

        Parameters
        ----------
        inputs : np.ndarray
            Input tensor (logits) to the Softmax layer, shape (batch_size, n_classes).
        y_true : np.ndarray
            Ground truth labels.

        Returns
        -------
        np.ndarray
            An array of loss values for each sample, shape (batch_size,).
        """
        self.activation.forward(inputs)
        self.output = self.activation.output

        return self.loss.forward(self.output, y_true)
    
    def backward(self, dvalues: np.ndarray, y_true: np.ndarray) -> None:
        """
        Performs the combined backward pass for Softmax and Cross-Entropy Loss.

        This calculation is simple and numerically stable.

        Parameters
        ----------
        dvalues : np.ndarray
            The output predictions (probabilities) from the Softmax forward pass. 
            Shape: (batch_size, n_classes).
        y_true : np.ndarray
            Ground truth labels, sparse (batch_size,) or one-hot (batch_size, n_classes).
        """
        # in the combined backward pass:
        # dvalues = softmax output (p_j)  -> NOT upstream gradients
        # because the loss layer starts backprop, so it receives the model's predictions
        
        samples = len(dvalues)  # number of samples m
        # dvalues shape = (m, n_classes)

        # if true labels are one-hot encoded convert them to sparse labels
        # because we only need the index where y_j = 1
        # and subtracting 1 at that index will give (p_j - y_j)
        if len(y_true.shape) == 2:
            y_true = np.argmax(y_true, axis=1)  
            # y_true now shape = (m, ), each entry is correct class index

        # make a copy so we don't modify original softmax output
        # starting gradient = p_j
        # final gradient = p_j - y_j
        self.dinputs = dvalues.copy()

        self.dinputs[range(samples), y_true] -= 1

        # normalization
        self.dinputs = self.dinputs / samples
