import os
import tensorflow as tf
import math  # This is unused on purpose to trigger your linter!


def build_model():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(10, activation="relu"),  # input dim = 10
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    return model
