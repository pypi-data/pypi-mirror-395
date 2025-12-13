"""
dlglab - A simple package with a print function
"""

def getprograms():

    from textwrap import dedent

    MENU = dedent("""
    Hi Macha what coping and all ?, what man too much cock showing only!!
    ok I will help you do this

    1. XOR using Perceptron (With Libraries)
    2. XOR using Perceptron (Without Libraries)
    3. Deep Neural Network with SGD & Adam
    4. CNN on MNIST
    5. Region-Based CNN (Object Detection)
    6. RNN for Handwriting Digit Recognition
    7. Bidirectional LSTM Sentiment Analysis
    8. Variational Autoencoder for Denoising
    """)

    TEMPLATES = {
        "1": dedent("""
        import math
import random

# Sigmoid + derivative as mentioned in PDF
def sigmoid(x): return 1 / (1 + math.exp(-x))
def d_sigmoid(x): return x * (1 - x)

# XOR truth table  -> PDF clearly states input + target format
X = [[0,0],[0,1],[1,0],[1,1]]
y = [0,1,1,0]

# Random weight initialization (PDF says initialized randomly)
hidden_w = [[random.random(), random.random()],
            [random.random(), random.random()]]
hidden_b = [random.random(), random.random()]

output_w = [random.random(), random.random()]
output_b = random.random()

lr = 0.1       # Learning rate from PDF
epochs = 10000 # Training iterations mentioned

for _ in range(epochs):

    for i in range(4):
        # Forward pass
        h1 = sigmoid(X[i][0]*hidden_w[0][0] + X[i][1]*hidden_w[0][1] + hidden_b[0])
        h2 = sigmoid(X[i][0]*hidden_w[1][0] + X[i][1]*hidden_w[1][1] + hidden_b[1])
        o  = sigmoid(h1*output_w[0] + h2*output_w[1] + output_b)

        error = y[i] - o                          # Backprop based on PDF description
        d_o = error * d_sigmoid(o)

        # Update output weights + bias
        output_w[0] += lr * d_o * h1
        output_w[1] += lr * d_o * h2
        output_b    += lr * d_o

        # Hidden layer gradient
        d_h1 = d_sigmoid(h1) * output_w[0] * d_o
        d_h2 = d_sigmoid(h2) * output_w[1] * d_o

        # Update hidden weights + biases
        hidden_w[0][0] += lr * d_h1 * X[i][0]
        hidden_w[0][1] += lr * d_h1 * X[i][1]
        hidden_b[0]    += lr * d_h1

        hidden_w[1][0] += lr * d_h2 * X[i][0]
        hidden_w[1][1] += lr * d_h2 * X[i][1]
        hidden_b[1]    += lr * d_h2

# Testing output after training (PDF expected output = 0 1 1 0)
print("\nFinal XOR Output after training:")
for i in range(4):
    h1 = sigmoid(X[i][0]*hidden_w[0][0] + X[i][1]*hidden_w[0][1] + hidden_b[0])
    h2 = sigmoid(X[i][0]*hidden_w[1][0] + X[i][1]*hidden_w[1][1] + hidden_b[1])
    o  = sigmoid(h1*output_w[0] + h2*output_w[1] + output_b)
    print(f"{X[i]} → {round(o)}")
        """),

        "2": dedent("""
        # TEMPLATE: XOR using Perceptron (No Libraries)
# XOR using Perceptron (Using Python Libraries)
# Based entirely on your PDF spec

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD

# XOR Input & Output (from PDF)
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

# Model = Sequential MLP
# Hidden Layer = 8 Neurons, Activation = ReLU (as given in PDF)
# Output = Sigmoid
model = Sequential()
model.add(Dense(8, input_dim=2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model — settings taken word-for-word from PDF:
model.compile(optimizer=SGD(learning_rate=0.1),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train model for 1000 epochs (PDF instruction)
model.fit(X, y, epochs=1000, verbose=0)

# Evaluate model
loss, acc = model.evaluate(X, y, verbose=0)
print(f"\nTraining Accuracy: {acc*100:.2f}%")

# Predictions
pred = model.predict(X)
print("\nXOR Output Predictions:")
print(np.round(pred))  # Convert sigmoid values to 0/1 as said in PDF

        """),

        "3": dedent("""
        # TEMPLATE: Deep Neural Network (SGD vs Adam)
# Deep NN with Two Optimizers: SGD & Adam
# Dataset + architecture + training process extracted only from your PDF

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD, Adam

# 1. Create Synthetic Data (as described in PDF)
X = np.random.rand(1000, 10)   # 1000 samples, 10 input features
y = np.random.rand(1000, 1)    # Regression target

# Function to train model using a selected optimizer
def train_model(optimizer, name):
    model = Sequential([
        Dense(50, activation='relu', input_dim=10),  # Input → 50
        Dense(20, activation='relu'),                 # 50 → 20
        Dense(1)                                      # Output layer for regression
    ])

    model.compile(optimizer=optimizer, loss='mse')    # MSE loss as per PDF

    loss_history = []
    for epoch in range(50):                           # 50 epochs (PDF)
        history = model.fit(X, y, epochs=1, batch_size=32, verbose=0)
        loss = history.history['loss'][0]
        loss_history.append(loss)
        print(f"{name} → Epoch {epoch+1}, Loss = {loss:.4f}")

    return loss_history

# Train using SGD & Adam separately
sgd_loss = train_model(SGD(learning_rate=0.01), "SGD")
adam_loss = train_model(Adam(learning_rate=0.001), "Adam")

# Plot loss curves for comparison (PDF instruction)
plt.plot(sgd_loss, label='SGD', color='blue')
plt.plot(adam_loss, label='Adam', color='orange')
plt.xlabel("Epochs")
plt.ylabel("Training Loss (MSE)")
plt.title("SGD vs Adam Loss Curve")
plt.legend()
plt.show()

        """),

        "4": dedent("""
        # TEMPLATE: CNN on MNIST
# PROGRAM 4: Classification of MNIST Dataset using CNN

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

# 1. Load MNIST dataset
(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

# 2. Reshape & normalize
# CNN expects (height, width, channels) → channel=1 for grayscale
train_images = train_images.reshape((train_images.shape[0], 28, 28, 1)).astype("float32") / 255.0
test_images  = test_images.reshape((test_images.shape[0], 28, 28, 1)).astype("float32") / 255.0

print("Train images shape:", train_images.shape)
print("Test images shape:", test_images.shape)

# 3. Define CNN architecture as per PDF description
model = models.Sequential([
    # First Conv + Pool
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),

    # Second Conv + Pool
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    # Third Conv (optional but mentioned in explanation)
    layers.Conv2D(64, (3, 3), activation='relu'),

    # Flatten + Dense layers
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')   # 10 classes: 0–9
])

model.summary()

# 4. Compile model
model.compile(
    optimizer='adam',                          # as in PDF
    loss='sparse_categorical_crossentropy',    # labels are integers 0–9
    metrics=['accuracy']
)

# 5. Train model
history = model.fit(
    train_images, train_labels,
    epochs=5,                                  # as specified
    batch_size=64,
    validation_data=(test_images, test_labels)
)

# 6. Evaluate on test data
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=0)
print(f"\nTest accuracy: {test_acc * 100:.2f}%")

# 7. Plot training history (accuracy and loss)
acc      = history.history['accuracy']
val_acc  = history.history['val_accuracy']
loss     = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(1, len(acc) + 1)

plt.figure(figsize=(12, 5))

# Accuracy plot
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training vs Validation Accuracy')
plt.legend()

# Loss plot
plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training vs Validation Loss')
plt.legend()

plt.tight_layout()
plt.show()

        """),

        "5": dedent("""
        # TEMPLATE: R-CNN for Object Detection
# PROGRAM 5: Region-Based CNN for Object Detection using EfficientDet (TensorFlow Hub)
# Based on your lab description (EfficientDet D0, TF Hub, OpenCV, threshold 0.5)

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import cv2

# Load EfficientDet D0 model from TensorFlow Hub (pre-trained on COCO)
MODEL_URL = "https://tfhub.dev/tensorflow/efficientdet/d0/1"
print("Loading model, wait macha...")
detector = hub.load(MODEL_URL)
print("Model loaded.")

def detect_objects(image_path, score_threshold=0.5):
    # Read image (BGR)
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        print("Image not found, check path properly.")
        return

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    h, w, _ = image_rgb.shape

    # Convert to tensor and add batch dimension
    img_tensor = tf.convert_to_tensor(image_rgb, dtype=tf.uint8)
    img_tensor = img_tensor[tf.newaxis, ...]   # shape: (1, H, W, 3)

    # Run model: returns dict with boxes, classes, scores, etc.
    outputs = detector(img_tensor)

    num_detections = int(outputs["num_detections"][0])
    boxes   = outputs["detection_boxes"][0].numpy()
    classes = outputs["detection_classes"][0].numpy().astype(np.int32)
    scores  = outputs["detection_scores"][0].numpy()

    # Draw bounding boxes for detections above threshold
    for i in range(num_detections):
        score = scores[i]
        if score < score_threshold:
            continue

        y_min, x_min, y_max, x_max = boxes[i]

        # Scale normalized box coords to image size
        x_min_px = int(x_min * w)
        x_max_px = int(x_max * w)
        y_min_px = int(y_min * h)
        y_max_px = int(y_max * h)

        # Draw rectangle
        cv2.rectangle(image_bgr,
                      (x_min_px, y_min_px),
                      (x_max_px, y_max_px),
                      (0, 255, 0), 2)

        # Put label: class ID + score (COCO labels mapping = TODO in your PDF)
        label = f"ID:{classes[i]} {score:.2f}"
        cv2.putText(image_bgr, label,
                    (x_min_px, max(0, y_min_px - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 1)

    # Show result
    cv2.imshow("Detections", image_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
# detect_objects("test_image.jpg")

        """),

        "6": dedent("""
        # TEMPLATE: RNN for Handwriting Recognition
# PROGRAM 6: RNN (LSTM) for Handwriting Digit Recognition using MNIST

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# 1. Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("Train shape:", x_train.shape)  # (60000, 28, 28)
print("Test shape:", x_test.shape)    # (10000, 28, 28)

# 2. Normalize pixel values to [0, 1]
x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32") / 255.0

# 3. Reshape for RNN/LSTM
# Already in shape (num_samples, 28, 28) → interpret as:
# time_steps = 28, features = 28
# So no extra reshape needed except ensuring correct dtype
# If you want to be explicit:
x_train = x_train.reshape((x_train.shape[0], 28, 28))
x_test  = x_test.reshape((x_test.shape[0], 28, 28))

# 4. One-hot encode labels: 0–9 → 10-dimensional vectors
y_train = to_categorical(y_train, 10)
y_test  = to_categorical(y_test, 10)

# 5. Build LSTM-based RNN model (from your PDF)
model = models.Sequential([
    layers.LSTM(
        128,
        activation='relu',     # as stated in your notes
        input_shape=(28, 28)
    ),
    layers.Dense(10, activation='softmax')  # 10 digit classes
])

model.summary()

# 6. Compile model
model.compile(
    optimizer='adam',                    # Adam optimizer
    loss='categorical_crossentropy',     # multi-class classification
    metrics=['accuracy']
)

# 7. Train the model
history = model.fit(
    x_train, y_train,
    epochs=10,                           # as per PDF
    batch_size=64,
    validation_data=(x_test, y_test)
)

# 8. Evaluate on test data
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\nTest Accuracy: {test_acc * 100:.2f}%")

        """),

        "7": dedent("""
        # TEMPLATE: Bidirectional LSTM Sentiment Analysis
# PROGRAM 7: Bidirectional LSTM for Sentiment Analysis on IMDB

import numpy as np
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dropout, Dense
from sklearn.model_selection import train_test_split

# 1. Hyperparameters (from your PDF)
num_words = 10000   # top 10k words
maxlen = 200        # fixed review length

# 2. Load IMDB dataset
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=num_words)

# 3. Pad sequences to fixed length
x_train = pad_sequences(x_train, maxlen=maxlen)
x_test  = pad_sequences(x_test,  maxlen=maxlen)

# 4. Split training into train + validation (80:20)
x_train, x_val, y_train, y_val = train_test_split(
    x_train, y_train, test_size=0.2, random_state=33
)

# 5. Build Bidirectional LSTM model
model = Sequential([
    Embedding(input_dim=num_words, output_dim=128, input_length=maxlen),
    Bidirectional(LSTM(64)),
    Dropout(0.5),
    Dense(1, activation='sigmoid')   # binary sentiment: positive / negative
])

model.summary()

# 6. Compile model (Adam + binary_crossentropy + accuracy)
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 7. Train model
history = model.fit(
    x_train, y_train,
    epochs=5,
    batch_size=64,
    validation_data=(x_val, y_val)
)

# 8. Evaluate on test data
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\nTest Accuracy on IMDB test set: {test_acc * 100:.2f}%")

# =============== Decoding & Sentiment Prediction (from your PDF) ===============

# Get word index mapping
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}

def decode_review(encoded_review):
    # Offset by 3 (for padding, start, unknown tokens) as mentioned
    return " ".join(
        reverse_word_index.get(i - 3, "?") for i in encoded_review if i > 2
    )

def encode_review(text):
    # Very simple tokenization by splitting on spaces
    words = text.lower().split()
    encoded = []
    for w in words:
        idx = word_index.get(w, 2)   # 2 usually reserved for "unknown"
        encoded.append(idx)
    return encoded

def predict_sentiment(review_text):
    encoded = encode_review(review_text)
    padded  = pad_sequences([encoded], maxlen=maxlen)
    prob    = model.predict(padded, verbose=0)[0][0]
    label   = "Positive" if prob >= 0.5 else "Negative"
    print(f"\nReview: {review_text}")
    print(f"Predicted Sentiment: {label} (score={prob:.4f})")

# Example usage:
# predict_sentiment("This movie was amazing and emotional, I loved it.")
# predict_sentiment("This was the worst boring movie I have ever seen.")

        """),

        "8": dedent("""
        # TEMPLATE: Variational Autoencoder (VAE)
# PROGRAM 8: (Variational) Autoencoder for Image Denoising using MNIST

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. Load MNIST dataset
(x_train, _), (x_test, _) = mnist.load_data()

print("Train shape:", x_train.shape)  # (60000, 28, 28)
print("Test shape:", x_test.shape)    # (10000, 28, 28)

# 2. Visualize a few original images (optional)
plt.figure(figsize=(4, 4))
for i in range(4):
    plt.subplot(2, 2, i + 1)
    plt.imshow(x_train[i], cmap="gray")
    plt.axis("off")
plt.suptitle("Sample Original Training Images")
plt.tight_layout()
plt.show()

# 3. Preprocessing: flatten & normalize to [0,1]
x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32") / 255.0

x_train = x_train.reshape((x_train.shape[0], 28 * 28))
x_test  = x_test.reshape((x_test.shape[0], 28 * 28))

print("Flattened train shape:", x_train.shape)  # (60000, 784)
print("Flattened test shape:", x_test.shape)    # (10000, 784)

# 4. Add Gaussian noise
noise_factor = 0.5
x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
x_test_noisy  = x_test  + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape)

# Clip back to [0,1]
x_train_noisy = np.clip(x_train_noisy, 0., 1.)
x_test_noisy  = np.clip(x_test_noisy,  0., 1.)

# 5. Build Autoencoder (encoder → bottleneck → decoder)
input_dim = 28 * 28

autoencoder = Sequential([
    # Encoder
    Dense(512, activation='relu', input_shape=(input_dim,)),
    Dense(256, activation='relu'),
    Dense(100, activation='relu'),   # Bottleneck / latent representation

    # Decoder
    Dense(256, activation='relu'),
    Dense(512, activation='relu'),
    Dense(input_dim, activation='sigmoid')  # Output in [0,1]
])

autoencoder.summary()

# 6. Compile model (MSE loss, Adam optimizer)
autoencoder.compile(optimizer='adam', loss='mse')

# 7. Train model: noisy → clean
history = autoencoder.fit(
    x_train_noisy, x_train,          # input = noisy, target = clean
    epochs=2,                        # as in your PDF
    batch_size=200,
    validation_data=(x_test_noisy, x_test)
)

# 8. Reconstruct (denoise) test images
x_test_denoised = autoencoder.predict(x_test_noisy)

# 9. Visualize Original vs Noisy vs Denoised
n = 10
plt.figure(figsize=(9, 9))

for i in range(n):
    # Original
    ax = plt.subplot(3, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28), cmap="gray")
    plt.axis("off")
    if i == 0:
        ax.set_title("Original")

    # Noisy
    ax = plt.subplot(3, n, i + 1 + n)
    plt.imshow(x_test_noisy[i].reshape(28, 28), cmap="gray")
    plt.axis("off")
    if i == 0:
        ax.set_title("Noisy")

    # Denoised
    ax = plt.subplot(3, n, i + 1 + 2 * n)
    plt.imshow(x_test_denoised[i].reshape(28, 28), cmap="gray")
    plt.axis("off")
    if i == 0:
        ax.set_title("Denoised")

plt.tight_layout()
plt.show()

        """),
    }


    print(MENU)
    choice = input("Select program number: ")

    print("\n============== YOUR TEMPLATE ==============\n")
    print(TEMPLATES.get(choice, "Invalid option macha, try again."))


__version__ = "0.5.0"
__all__ = ["print"]
