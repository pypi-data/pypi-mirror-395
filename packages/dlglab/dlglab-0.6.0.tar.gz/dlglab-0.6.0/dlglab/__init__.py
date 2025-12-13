"""
dlglab - A simple package with a print function
"""

def getprograms():

    from textwrap import dedent

    MENU = dedent("""
    Hi Macha what coping and all ?, what man too much cock showing only!!
    ok I will help you do this

    1. XOR using Perceptron (Without Libraries)
    2. XOR using Perceptron (With Libraries)
    3. Deep Neural Network with SGD & Adam
    4. CNN on MNIST
    5. Region-Based CNN (Object Detection)
    6. RNN for Handwriting Digit Recognition
    7. Bidirectional LSTM Sentiment Analysis
    8. Variational Autoencoder for Denoising
    """)

    TEMPLATES = {
        "1": dedent("""
        import numpy as np

# Sigmoid activation function
def sigmoid(x):
  return 1 / (1 + np.exp(-x))

# Derivative of sigmoid
def sigmoid_derivative(x):
  return x * (1 - x)

# XOR dataset
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
expected_output = np.array([[0], [1], [1], [0]])

# Initialize weights and biases
inputLayerNeurons, hiddenLayerNeurons, outputNeurons = 2, 2, 1
hidden_weights = np.random.uniform(size=(inputLayerNeurons, hiddenLayerNeurons))
hidden_bias = np.random.uniform(size=(1, hiddenLayerNeurons))
output_weights = np.random.uniform(size=(hiddenLayerNeurons, outputNeurons))
output_bias = np.random.uniform(size=(1, outputNeurons))

# Learning rate
lr = 0.1

epochs = 10000
for _ in range(epochs):
  # Forward propagation
  hidden_layer_activation = np.dot(inputs, hidden_weights) + hidden_bias
  hidden_layer_output = sigmoid(hidden_layer_activation)

  output_layer_activation = np.dot(hidden_layer_output, output_weights) + output_bias
  predicted_output = sigmoid(output_layer_activation)

  # Backpropagation
  error = expected_output - predicted_output
  d_predicted_output = error * sigmoid_derivative(predicted_output)

  error_hidden_layer = d_predicted_output.dot(output_weights.T)
  d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

  # Update weights and biases
  output_weights += hidden_layer_output. T.dot(d_predicted_output) * lr
  output_bias += np.sum(d_predicted_output, axis=0, keepdims=True) * lr
  hidden_weights += inputs.T.dot(d_hidden_layer) * lr
  hidden_bias += np.sum(d_hidden_layer, axis=0, keepdims=True) * lr

# Testing the MLP
print("Predicted Output:")
print(predicted_output)
        """),

        "2": dedent("""
        # TEMPLATE: XOR using Perceptron (No Libraries)
# XOR using Perceptron (Using Python Libraries)
# Based entirely on your PDF spec

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD

X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])


model = Sequential([
    Dense(4,input_dim = 2 ,activation = "relu"), # Hidden layer 8 neuron
    Dense(1,activation="sigmoid") # Output layer One Neuron, binary Classfication
])

model.compile(loss="binary_crossentropy",optimizer=SGD(learning_rate=0.1),metrics=["accuracy"])

model.fit(X,y,epochs=1000,verbose = 0)

_,accuracy = model.evaluate(X,y)
print(f"model accuracy = {accuracy*100:.2f}%")

predictions = model.predict(X)
print("Predictions : \n",predictions)
        """),

        "3": dedent("""
        # TEMPLATE: Deep Neural Network (SGD vs Adam)
from tensorflow.keras import layers, models, optimizers
import numpy as np
import matplotlib.pyplot as plt

X = np.random.randn(1000, 10)
y = np.random.randn(1000, 1)

#sgd
model_sgd = models.Sequential([
    layers.Dense(50,activation="relu"),
    layers.Dense(30,activation="relu"),
    layers.Dense(1)
])

model_sgd.compile(optimizer=optimizers.SGD(learning_rate=0.01), loss="mse")

print("\nTraining with SGD Optimizer\n")
history_sgd = model_sgd.fit(X, y,epochs=50)

sgd_loss = history_sgd.history["loss"]

# adam
model_adam = models.Sequential([
    layers.Dense(50,activation="relu"),
    layers.Dense(30,activation="relu"),
    layers.Dense(1)
])

model_adam.compile(optimizer=optimizers.Adam(learning_rate=0.001), loss="mse")

print("\nTraining with Adam Optimizer\n")
history_adam = model_adam.fit(X, y,epochs=50)

adam_loss = history_adam.history["loss"]

# plot
plt.plot(range(1,50+1),sgd_loss,label="SGD")
plt.plot(range(1,50+1),adam_loss,label="Adam")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("SGD vs ADAM")
plt.legend()
plt.grid(True)
plt.show()

        """),

        "4": dedent("""
        # TEMPLATE: CNN on MNIST
# PROGRAM 4: Classification of MNIST Dataset using CNN
import tensorflow as tf
from tensorflow.keras import models,layers
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt


(X_train,y_train),(X_test,y_test) = mnist.load_data()

X_train = X_train.reshape((X_train.shape[0],28,28,1))
X_test = X_test.reshape((X_test.shape[0],28,28,1))


X_train = X_train/255.0
X_test = X_test/255.0

model = models.Sequential([
    layers.Conv2D(32,(3,3),activation="relu",input_shape=(28,28,1)),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64,(3,3),activation="relu"),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64,(3,3),activation="relu"),

    layers.Flatten(),

    layers.Dense(64,activation="relu"), 

    layers.Dense(10,activation="softmax")
])

model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",
              metrics=['accuracy'])

history = model.fit(X_train,y_train,epochs=5,
                    validation_data=(X_test,y_test))

test_loss,test_accuracy = model.evaluate(X_test,y_test,verbose=2)

print("TEST ACCURACY = ",test_accuracy)

plt.figure(figsize=(12, 4))

# accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

# loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

plt.show()

        """),

        "5": dedent("""
        # TEMPLATE: R-CNN for Object Detection
# PROGRAM 5: Region-Based CNN for Object Detection using EfficientDet (TensorFlow Hub)
# Based on your lab description (EfficientDet D0, TF Hub, OpenCV, threshold 0.5)

import warnings
warnings.filterwarnings("ignore")
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2
import matplotlib.pyplot as plt


model_url = "https://tfhub.dev/tensorflow/efficientdet/d0/1"
detector = hub.load(model_url)

image_path = "/traffic1.jpg"  
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_tensor = tf.convert_to_tensor([img_rgb], dtype=tf.uint8)

detections = detector(img_tensor)
boxes = detections["detection_boxes"][0].numpy()
classes = detections["detection_classes"][0].numpy().astype(int) #each class
scores = detections["detection_scores"][0].numpy() #confidence

for i in range(len(scores)):
    if scores[i] > 0.5:
        h, w, _ = img.shape
        ymin, xmin, ymax, xmax = boxes[i]
        (x1, y1, x2, y2) = (int(xmin * w), int(ymin * h), int(xmax * w), int(ymax * h))
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"Object {classes[i]}: {scores[i]:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
  
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Detected Objects using EfficientDet (R-CNN style)")
plt.axis("off")
plt.show()

        """),

        "6": dedent("""
        # TEMPLATE: RNN for Handwriting Recognition
# PROGRAM 6: RNN (LSTM) for Handwriting Digit Recognition using MNIST
import tensorflow as tf
from tensorflow.keras import layers,models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

(X_train,y_train),(X_test,y_test) = mnist.load_data()

X_train = X_train/255.0
X_test = X_test/255.0

X_train = X_train.reshape((X_train.shape[0],28,28))
X_test = X_test.reshape((X_test.shape[0],28,28))

y_train = to_categorical(y_train,10)
y_test = to_categorical(y_test,10)

model = models.Sequential([
    layers.LSTM(128,activation="relu",input_shape=(28,28)),
    layers.Dense(10,activation="softmax")
])

model.compile(loss = "categorical_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

model.fit(X_train,y_train,epochs=20,
          batch_size=3000,
          validation_data=(X_test,y_test))

loss,accuracy = model.evaluate(X_test,y_test)

print("Accuracy = ",accuracy)
        """),

        "7": dedent("""
        # TEMPLATE: Bidirectional LSTM Sentiment Analysis
# PROGRAM 7: Bidirectional LSTM for Sentiment Analysis on IMDB

import tensorflow as tf
from tensorflow.keras import models,layers  
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tensorflow.keras.datasets import imdb
import numpy as np

num_words = 10000
maxlen = 200

(X_train,y_train),(X_test,y_test) = imdb.load_data(num_words=num_words)

X_train = pad_sequences(X_train,maxlen=maxlen)
X_test = pad_sequences(X_test,maxlen=maxlen)

X_train,X_val,y_train,y_val = train_test_split(X_train,y_train,
                                               test_size=0.2,
                                               random_state=42)
model = models.Sequential([
    layers.Embedding(input_dim=num_words, output_dim=128, input_length=maxlen),
    layers.Bidirectional(layers.LSTM(64,return_sequences=False)),
    layers.Dropout(0.5),
    layers.Dense(1,activation="sigmoid")
])

model.compile(optimizer="adam",
              loss="binary_crossentropy",
              metrics=["accuracy"])

model.summary()

history = model.fit(X_train,y_train,
                    validation_data=(X_val,y_val),
                    epochs=5,
                    batch_size=64)

loss,accuracy = model.evaluate(X_test,y_test)

print("Accuracy = ",accuracy*100)



def decode_review(encoded_review):
    word_index = imdb.get_word_index()
    reverse_words_index = {value:key for key,value in word_index.items()}

    decoded_review = []

    for i in encoded_review:
        if i>2:
            decoded_review.append(reverse_words_index.get(i-3))

    return " ".join(decoded_review)

def predict_sentiment(review):
    word_index = imdb.get_word_index()
    encoded_review = [word_index.get(word,0)+3 for word in review.split()]
    padded_review = pad_sequences([encoded_review],maxlen=maxlen)
    prediction = model.predict(padded_review,verbose=2)

    sentiment = "POSITIVE" if prediction[0][0] >= 0.5 else "NEGATIVE"

    return sentiment


print("SAMPLE SENTIMENT :\n")

for i in range(5):
    review = decode_review(X_test[i])
    sentiment = predict_sentiment(review)

    print("*"*50)
    print("\nREVIEW :", review)
    print("SENTIMENT :", sentiment)
    print()
    print("*"*50)

        """),

        "8": dedent("""
        # TEMPLATE: Variational Autoencoder (VAE)
# PROGRAM 8: (Variational) Autoencoder for Image Denoising using MNIST

import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential 
from keras.layers import Dense
from keras.datasets  import mnist
import random

(X_train,y_train),(X_test,y_test) = mnist.load_data()
print("Training Data Shape",X_train.shape)
print("Testing Data Shape",X_test.shape)

for i in range(1,5):
    plt.subplot(2,2,i)
    plt.imshow(X_train[random.randint(1,100)],plt.get_cmap("gray"))
plt.show()

num_pixels = 28*28
X_train = X_train.reshape(X_train.shape[0],num_pixels).astype("float32")
X_test = X_test.reshape(X_test.shape[0],num_pixels).astype("float32")
X_train = X_train/255
X_test = X_test/255
  
print("Reshaped Training Data Shape",X_train.shape)
print("Reshaped Testing Data Shape",X_test.shape)

noise_factor = 0.2
x_train_noisy = X_train + noise_factor * np.random.normal(
    loc=0.0, scale=1.0, size=X_train.shape
)

x_test_noisy = X_test + noise_factor * np.random.normal(
    loc=0.0, scale=1.0, size=X_test.shape
)

x_train_noisy = np.clip(x_train_noisy, 0., 1.)
x_test_noisy = np.clip(x_test_noisy, 0., 1.)

model = Sequential([
    Dense(500,activation="relu",input_dim=784),
    Dense(300,activation="relu"),
    Dense(100,activation="relu"),
    Dense(300,activation="relu"),
    Dense(500,activation="relu"),
    Dense(784,activation="sigmoid")
])

model.compile(loss="mean_squared_error",optimizer="adam")

print("Training")
history = model.fit(x_train_noisy,X_train,validation_data=(x_test_noisy,X_test),epochs=2,batch_size=200)

print("Evaluating")
pred = model.predict(x_test_noisy)

print("Shape of predicted Data = ",pred.shape)
print("Shape of Test Data = ",X_test.shape)

# back to image 
X_test      = np.reshape(X_test, (10000, 28, 28)) * 255
pred        = np.reshape(pred, (10000, 28, 28)) * 255
x_test_noisy = np.reshape(x_test_noisy, (-1, 28, 28)) * 255

# test 
plt.figure(figsize=(20, 4))
print("Test Images")
for i in range(10, 20, 1):
    plt.subplot(2, 10, i + 1)
    plt.imshow(X_test[i, :, :], cmap='gray')
    curr_lbl = y_test[i]
    plt.title(f"(Label: {curr_lbl})")
plt.show()

#  noisy 
plt.figure(figsize=(20, 4))
print("Test Images with Noise")
for i in range(10, 20, 1):
    plt.subplot(2, 10, i + 1)
    plt.imshow(x_test_noisy[i, :, :], cmap='gray')
plt.show()

#  denoised
plt.figure(figsize=(20, 4))
print("Reconstruction of Noisy Test Images")
for i in range(10, 20, 1):
    plt.subplot(2, 10, i + 1)
    plt.imshow(pred[i, :, :], cmap='gray')
plt.show()
        """),
    }


    print(MENU)
    choice = input("Select program number: ")

    print("\n============== YOUR TEMPLATE ==============\n")
    print(TEMPLATES.get(choice, "Invalid option macha, try again."))


__version__ = "0.6.0"
__all__ = ["print"]
