# Ronet: A NumPy-only Deep Learning Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

**Ronet** is a lightweight, modular deep learning library built entirely from scratch using only `numpy`. 

It is designed for educational purposes, demystifying the "black box" of frameworks like PyTorch or TensorFlow. It implements backpropagation, optimizers, and layer logic using raw matrix operations, making it an excellent tool for understanding the mathematics of deep learning.

## 🚀 Features

* **No Heavy Dependencies:** Built strictly on NumPy.
* **Keras-like API:** Familiar `.add()`, `.compile()`, and `.train()` structure.
* **Modular Design:** easily extensible layers, optimizers, and loss functions.
* **Implements Core Concepts:**
    * **Layers:** Dense (Fully Connected), Dropout, BatchNorm.
    * **Activations:** ReLU, Softmax, Sigmoid, Linear.
    * **Optimizers:** Adam, RMSProp, SGD (with Momentum), Adagrad.
    * **Losses:** Categorical Cross-Entropy, Binary Cross-Entropy, MSE.

## 📦 Installation

You can install Ronet via pip (coming soon):

```bash
pip install ronet
```

Or clone the repository and install locally:

```bash
git clone [https://github.com/YOUR_USERNAME/ronet.git](https://github.com/YOUR_USERNAME/ronet.git)
cd ronet
pip install .
```

```python
import numpy as np
from ronet.model import Model, Accuracy_Classification
from ronet.layers import Dense, Dropout
from ronet.activations import ReLU, Softmax
from ronet.loss import CrossEntropyLoss
from ronet.optimizers import Optimizer_Adam

# 1. Prepare Data (Dummy data for demonstration)
# In reality, load MNIST data here and normalize to 0-1
X_train = np.random.randn(1000, 784) # 1000 samples, 784 features
y_train = np.random.randint(0, 10, size=(1000,)) # 10 classes

# 2. Build Model
model = Model()

model.add(Dense(784, 128))
model.add(ReLU())
model.add(Dropout(0.1))

model.add(Dense(128, 64))
model.add(ReLU())

model.add(Dense(64, 10))
model.add(Softmax())

# 3. Configure
model.set(
    loss=CrossEntropyLoss(),
    optimizer=Optimizer_Adam(learning_rate=0.005, decay=1e-3),
    accuracy=Accuracy_Classification()
)

model.finalize()

# 4. Train
model.train(X_train, y_train, epochs=10, batch_size=128, print_every=1)
```
🧠 Architecture Overview
Ronet uses a Doubly Linked List approach for its computational graph. When you call model.finalize(), the framework links layers together:

Input -> Dense -> ReLU -> Dense -> Softmax -> Loss

During the Forward Pass, data flows sequentially. During the Backward Pass, gradients flow in reverse, with each layer computing its own derivatives (Jacobians or element-wise) and passing the result to the previous layer.

🤝 Contributing
Contributions are welcome! This is an educational project, so readability is prioritized over raw performance.

Fork the project.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📝 License
Distributed under the MIT License. See LICENSE for more information.