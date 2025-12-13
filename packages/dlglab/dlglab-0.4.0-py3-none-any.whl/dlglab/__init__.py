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
        # TEMPLATE: XOR using Perceptron with Libraries

        # Step 1: Import required libraries
        # import numpy as np
        # import something else if needed

        # Step 2: Define dataset (XOR truth table)

        # Step 3: Build perceptron/MLP model

        # Step 4: Train for required epochs

        # Step 5: Evaluate and print outputs

        """),

        "2": dedent("""
        # TEMPLATE: XOR using Perceptron (No Libraries)

        # Step 1: Take inputs manually
        # Step 2: Initialize weights randomly
        # Step 3: Define activation function manually
        # Step 4: Implement forward + update rule manually
        # Step 5: Train until convergence and print results

        """),

        "3": dedent("""
        # TEMPLATE: Deep Neural Network (SGD vs Adam)

        # Step 1: Build NN with dense layers
        # Step 2: Train with Optimizer 1 (SGD)
        # Step 3: Train with Optimizer 2 (Adam)
        # Step 4: Compare accuracy/loss curves

        """),

        "4": dedent("""
        # TEMPLATE: CNN on MNIST

        # Step 1: Load MNIST dataset
        # Step 2: Build CNN with Conv2D + MaxPool
        # Step 3: Train CNN & evaluate accuracy
        # Step 4: Print confusion matrix or sample predictions

        """),

        "5": dedent("""
        # TEMPLATE: R-CNN for Object Detection

        # Step 1: Load dataset
        # Step 2: Region proposal mechanism
        # Step 3: Feature extraction + classifier
        # Step 4: Train + evaluate performance

        """),

        "6": dedent("""
        # TEMPLATE: RNN for Handwriting Recognition

        # Step 1: Prepare sequence dataset
        # Step 2: Build RNN/LSTM/GRU model
        # Step 3: Train and visualize predictions

        """),

        "7": dedent("""
        # TEMPLATE: Bidirectional LSTM Sentiment Analysis

        # Step 1: Load IMDB reviews
        # Step 2: Tokenize + pad sequences
        # Step 3: Build Bi-LSTM model
        # Step 4: Train + evaluate + predict custom text

        """),

        "8": dedent("""
        # TEMPLATE: Variational Autoencoder (VAE)

        # Step 1: Encoder network
        # Step 2: Latent sampling layer
        # Step 3: Decoder network
        # Step 4: Train VAE to denoise images

        """),
    }


    print(MENU)
    choice = input("Select program number: ")

    print("\n============== YOUR TEMPLATE ==============\n")
    print(TEMPLATES.get(choice, "Invalid option macha, try again."))


__version__ = "0.3.0"
__all__ = ["print"]
