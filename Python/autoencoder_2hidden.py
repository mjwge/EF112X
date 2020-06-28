import tensorflow as tf
print("Hello ")
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image

"""
Making the Autoencoder using keras
"""

dbg = False

class Encoder(tf.keras.layers.Layer):
    """Making the Encoder part of the Autoencoder"""

    def __init__(self, hidden_dim):
        """Initializer"""
        super(Encoder, self).__init__()
        """Run the initialization for the legacy (tf.keras.layers.Layer)"""
        print(hidden_dim)
        self.hidden_enc_1 = tf.keras.layers.Dense(units=hidden_dim[0], activation=tf.nn.relu, kernel_initializer='he_uniform')
        self.hidden_enc_2 = tf.keras.layers.Dense(units=hidden_dim[1], activation=tf.nn.relu, kernel_initializer='he_uniform')

        self.output_layer = tf.keras.layers.Dense(units=hidden_dim[1], activation=tf.nn.relu)
        """Create layers of size 'hidden_dim[i]' in a order of decreasing sizes. Can be expanded arbitrarily"""

    def call(self, input_features):
        """Make the call method, which is ran when the encoder is called. """

        if dbg: print(input_features.shape, "input shape")
        x = self.hidden_enc_1(input_features)
        x = self.hidden_enc_2(x)

        activation = x

        out = self.output_layer(activation)  # Mittenlagret som går till decodern.
        """Let the input vector go through all layers and return the latent representation"""

        return out

class Decoder(tf.keras.layers.Layer):
    """Making the Decoder part of the Autoencoder"""
    def __init__(self, hidden_dim, original_dim):
        """Initializer"""
        super(Decoder, self).__init__()
        """Run the init of the legacy (tf.keras.layers.Layer)"""

        self.hidden_dec_1 = tf.keras.layers.Dense(units=hidden_dim[1], activation=tf.nn.relu, kernel_initializer='he_uniform')
        self.hidden_dec_2 = tf.keras.layers.Dense(units=hidden_dim[0], activation=tf.nn.relu, kernel_initializer='he_uniform')

        self.output_layer = tf.keras.layers.Dense(units=original_dim, activation=tf.nn.sigmoid)
        """Create layers of size 'hidden_dim[i]', in a increasing order regarding sizes."""

    def call(self, code):
        """Call method of the decoder which is ran when the object is called"""
        x = self.hidden_dec_1(code)

        x1 = self.hidden_dec_2(x)

        activation = x1
        """Increase the latent representation of the input by putting it through all layers, until it reaches original size again. """

        return self.output_layer(activation)


class Autoencoder(tf.keras.Model):
    """The complete Autoencoder class"""
    def __init__(self, hidden_dim, original_dim):
        """Initialization"""
        super(Autoencoder, self).__init__()
        """Run init of legacy (tf.keras.layers.Layer)"""
        self.encoder = Encoder(hidden_dim=hidden_dim)
        self.decoder = Decoder(hidden_dim=hidden_dim, original_dim=original_dim)
        """Create encoder and decoder"""

    def call(self, input_features):
        """Call method that compresses and reconstructs the input vector."""
        code = self.encoder(input_features)
        reconstructed = self.decoder(code)
        return reconstructed



def loss(model, original):
    """Define the loss function"""
    if dbg: print(model(original).shape, "rec",original[0][0:1439].shape, " original", flush=True)

    reconstruction_error = tf.reduce_mean(tf.square(tf.subtract(model(original), original.reshape(1, original.shape[1]))))
    """Useing the built in 'reduce_mean' function in tf, comparing the original input and the reconstructed vector. """
    return reconstruction_error


def train(loss, model, optimizer, original):
    """Updating the weigths. Is used by the .fit function in the main training program. """
    with tf.GradientTape() as tape:
        gradients = tape.gradient(loss(model, original), model.trainable_variables)
    gradient_variables = zip(gradients, model.trainable_variables)
    optimizer.apply_gradients(gradient_variables)