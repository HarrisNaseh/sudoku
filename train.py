import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

from tensorflow.python.keras.metrics import accuracy

data = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = data.load_data()

x_train = tf.keras.utils.normalize(x_train, axis = 1)
x_test = tf.keras.utils.normalize(x_test, axis = 1)
model = tf.keras.models.Sequential()

# model.add(tf.keras.layers.Flatten(input_shape = (28, 28)))
# model.add(tf.keras.layers.Dense(units = 128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(units = 128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(units = 10, activation = tf.nn.softmax))

model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(100, activation='relu', kernel_initializer='he_uniform'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

model.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ['accuracy'])

model.fit(x_train, y_train, epochs = 10)

loss, accuracy = model.evaluate(x_test, y_test)

print(accuracy)
print(loss)

for i in range(1, 5):
    img = cv.imread(f'{i}.png')[:, :, 0]
    img = np.invert(np.array([img]))

    perdiction = model.predict(img)

    print("pridction: ", np.argmax(perdiction))

    plt.imshow(img[0], cmap= plt.cm.binary)
    plt.show()

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

model.save("final_model.h5")

