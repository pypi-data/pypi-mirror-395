import numpy as np
from .layers import *
from .loss import *
from .optimizers import *
from .regularization import *
from .activations import *
import math
from typing import List, Optional, Union, Any

class Input:
    """
    A placeholder layer representing the input data.
    It sits at the beginning of the model to provide the initial 'output' 
    for the first hidden layer.
    """
    def __init__(self):
        self.output: Optional[np.ndarray] = None

    def forward(self, inputs: np.ndarray, training: bool = True) -> None:
        self.output = inputs

class Accuracy:
    """
    Base class for calculating model accuracy.
    """
    def __init__(self):
        self.accumulated_sum: float = 0.0
        self.accumulated_count: int = 0

    def init(self, y: np.ndarray) -> None:
        """
        Initializes accuracy metrics based on ground truth data.
        (Used primarily in regression to determine precision tolerance).
        """
        pass

    def calculate(self, predictions: np.ndarray, y: np.ndarray) -> float:
        """
        Calculates accuracy for a given batch.
        """
        comparisons = self.compare(predictions, y)
        accuracy = np.mean(comparisons)

        self.accumulated_sum += np.sum(comparisons)
        self.accumulated_count += len(comparisons)

        return accuracy
    
    def calculate_accumulated(self) -> float:
        """
        Returns the average accuracy over all accumulated batches (epoch accuracy).
        """
        if self.accumulated_count == 0:
            return 0.0
        return self.accumulated_sum / self.accumulated_count
    
    def reset(self) -> None:
        self.accumulated_sum = 0
        self.accumulated_count = 0
    
    def compare(self, predictions: np.ndarray, y: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    
class Accuracy_Regression(Accuracy):
    """
    Accuracy calculation for regression models.
    
    Since regression outputs are continuous float values, they are rarely exactly 
    equal to the target. We consider a prediction 'correct' if it falls within 
    a certain range (precision) of the target.
    """
    def __init__(self):
        super().__init__()
        self.precision: Optional[float] = None
    
    def init(self, y: np.ndarray, reinit: bool = False) -> None:
        """
        Sets the precision threshold based on the standard deviation of the targets.
        """
        if self.precision is None or reinit:
            # Default behavior: precision is 1/250th of the data's standard deviation
            self.precision = np.std(y) / 250
    
    def compare(self, predictions: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.absolute(predictions - y) < self.precision

class Accuracy_Classification(Accuracy):
    """
    Accuracy calculation for classification models.
    """
    def init(self, y: np.ndarray) -> None:
        pass

    def compare(self, predictions: np.ndarray, y: np.ndarray) -> np.ndarray:
        # If labels are one-hot encoded, convert to class indices
        if len(y.shape) == 2:
            y = np.argmax(y, axis=1)
        # Predictions (from argmax) compared to integer targets
        return predictions == y
    
class Model:
    """
    The main container for the Neural Network.

    This class handles:
    1. Layer management.
    2. Connection compilation (linking layers).
    3. The training loop (forward/backward passes, batching).
    4. Prediction.
    """
    def __init__(self):
        self.layers: List[Any] = []
        self.loss: Any = None
        self.optimizer: Any = None
        self.accuracy: Any = None
        self.input_layer = Input()
        self.softmax_classifier_output: Any = None
        self.trainable_layers: List[Any] = []
        self.output_layer_activation: Any = None

    def add(self, layer: Any) -> None:
        """
        Adds a layer to the model.
        """
        self.layers.append(layer)
    
    def set(self, *, loss: Any, optimizer: Any, accuracy: Any) -> None:         # * ensures that loss and optimizer are required keyword args
        """
        Sets the training configuration.
        """
        self.loss = loss
        self.optimizer = optimizer
        self.accuracy = accuracy

    def finalize(self) -> None:
        """
        Compiles the model structure.

        This method connects the layers into a linked list. 
        Each layer gains a `.prev` and `.next` attribute.
        
        Structure:
        Input -> Layer1 -> Layer2 -> ... -> Loss
        """
        self.input_layer = Input()
        layer_count = len(self.layers)
        self.trainable_layers = []

        for i in range(layer_count):
            # If it's the first layer, its previous layer is the Input object
            if i == 0:
                self.layers[i].prev = self.input_layer
                self.layers[i].next = self.layers[i+1]
            
            # Hidden layers
            elif i < layer_count - 1:
                self.layers[i].prev = self.layers[i-1]
                self.layers[i].next = self.layers[i+1]
            
            # Last layer: its next object is the Loss function
            else:
                self.layers[i].prev = self.layers[i-1]
                self.layers[i].next = self.loss
                self.output_layer_activation = self.layers[i]

            # Track trainable layers for the optimizer
            if hasattr(self.layers[i], 'trainable'):
                self.trainable_layers.append(self.layers[i])

        self.loss.remember_trainable_layers(self.trainable_layers)

        # use combined softmax and crossentropy
        # Optimization: Detect Softmax + CrossEntropy
        # If the last layer is Softmax and loss is CrossEntropy, use the combined object
        # for faster backward pass (skipping Jacobian calculation).
        if isinstance(self.layers[-1], Softmax) and isinstance(self.loss, CrossEntropyLoss):
            self.softmax_classifier_output = Activation_Softmax_Loss_Cross_Entropy()

    # training loop
    def train(self, X: np.ndarray, y: np.ndarray, *, 
              epochs: int = 1, batch_size: Optional[int] = None, 
              validation_data: Optional[tuple] = None) -> None:
        """
        Main training loop.

        Parameters
        ----------
        X : np.ndarray
            Input training data.
        y : np.ndarray
            Training labels/targets.
        epochs : int
            Number of passes through the entire dataset.
        batch_size : int, optional
            Number of samples per gradient update. If None, uses full batch.
        print_every : int
            Frequency of printing log stats (in epochs).
        validation_data : tuple, optional
            A tuple of (X_val, y_val) for validation.
        """
        self.accuracy.init(y)

        # Calculate steps per epoch
        train_steps = 1
        if batch_size is not None:
            train_steps = len(X) // batch_size
            if train_steps * batch_size < len(X):
                train_steps += 1

        # actual training
        for epoch in range(1, epochs+1):
            print(f'Epoch {epoch}/{epochs}')
            # reset the accumulated loss over epoch to 0
            self.loss.reset()
            self.accuracy.reset()

            for step in range(train_steps):
                if batch_size is None:
                    batch_X = X
                    batch_y = y
                else:
                    batch_X = X[step*batch_size: (step + 1)*batch_size]
                    batch_y = y[step*batch_size: (step + 1)*batch_size]

                output = self.forward(batch_X, training=True)
                data_loss, regularization_loss = self.loss.calculate(output, batch_y, include_regularization = True)
                predictions = self.output_layer_activation.predict(output)
                accuracy = self.accuracy.calculate(predictions, batch_y)
                self.backward(output, batch_y)
                
                self.optimizer.pre_update_params()
                for layer in self.trainable_layers:
                    self.optimizer.update_params(layer)
                self.optimizer.post_update_params()
        
            epoch_data_loss, epoch_reg_loss = self.loss.calculate_accumulated(include_regularization = True)
            epoch_loss = epoch_data_loss + epoch_reg_loss
            epoch_acc = self.accuracy.calculate_accumulated()

            print(f'training - acc: {epoch_acc:.3f}, loss: {epoch_loss:.3f} ' +
                      f'(data_loss: {epoch_data_loss:.3f}, reg_loss: {epoch_reg_loss:.3f}), ' +
                      f'lr: {self.optimizer.current_learning_rate}')


            if validation_data is not None:
                self.evaluate(*validation_data, batch_size=batch_size)
    
    def evaluate(self, X_val: np.ndarray, y_val: np.ndarray, batch_size: Optional[int] = None) -> None:
        """
        Evaluates the model on validation data.
        """
        val_steps = 1
        if batch_size is not None:
            val_steps = len(X_val) // batch_size
            if val_steps * batch_size < len(X_val):
                val_steps += 1

        self.loss.reset()
        self.accuracy.reset()

        for step in range(val_steps):
            if batch_size is None:
                batch_X = X_val
                batch_y = y_val
            else:
                batch_X = X_val[step*batch_size : (step+1)*batch_size]
                batch_y = y_val[step*batch_size : (step+1)*batch_size]

            val_output = self.forward(batch_X, training=False)
            self.loss.calculate(val_output, batch_y)

            val_predictions = self.output_layer_activation.predict(val_output)
            self.accuracy.calculate(val_predictions, batch_y)
        
        val_loss = self.loss.calculate_accumulated()
        val_accuracy = self.accuracy.calculate_accumulated()
        print(f'validation - acc: {val_accuracy:.3f}, loss: {val_loss:.3f}')
    
    def forward(self, X: np.ndarray, training: bool) -> np.ndarray:
        """
        Performs the forward pass through all layers.
        """
        self.input_layer.forward(X, training = training)
        for layer in self.layers:
            layer.forward(layer.prev.output, training = training)
        
        return layer.output
    
    def backward(self, outputs: np.ndarray, y: np.ndarray) -> None:
        """
        Performs the backward pass (backpropagation).
        """
        if self.softmax_classifier_output is not None:
            self.softmax_classifier_output.backward(outputs, y)
            self.layers[-1].dinputs = self.softmax_classifier_output.dinputs

            for layer in reversed(self.layers[:-1]):
                layer.backward(layer.next.dinputs)
            return
        
        self.loss.backward(outputs, y)
        for layer in reversed(self.layers):
            layer.backward(layer.next.dinputs)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Generates predictions for input data (inference mode).
        """
        output = self.forward(X, training=False)
        return output


