from keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt

model = load_model('final_model.h5')
def predict(img):
    image = img.copy()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)[1]
    image = cv2.resize(image, (28, 28))


    if np.sum(image) > np.prod(image.shape) * 254 * 0.95:  # Change 0.9 based on your requirements
       return 0
    # display_image(image)
    image = cv2.bitwise_not(image)
    image = image.astype('float32')
    image = image.reshape(1, 28, 28, 1)
    image /= 255

   #  plt.imshow(image.reshape(28, 28), cmap='Greys')
   #  plt.show()

    pred = model.predict(image.reshape(1, 28, 28, 1), batch_size=1)

    number = np.argmax(pred)
    # print("Predicted Number: ", number)
    return number
