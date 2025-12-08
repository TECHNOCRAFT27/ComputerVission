# app.py
import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

# Load model & labels once
model = tf.keras.models.load_model("model.h5")
labels = open("labels.txt").read().splitlines()

st.title("Webcam + Teachable-Machine Model Demo")

img_file_buffer = st.camera_input("Take a picture")  # get image from webcam

if img_file_buffer is not None:
    # Convert to OpenCV image
    bytes_data = img_file_buffer.getvalue()
    nparr = np.frombuffer(bytes_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Preprocess exactly like before
    img = cv2.resize(frame, (224, 224))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    predictions = model.predict(img)
    idx = np.argmax(predictions)
    label = labels[idx]
    confidence = predictions[0][idx]

    st.image(frame, channels="BGR")  # display the captured frame
    st.write(f"Prediction: **{label}** with confidence **{confidence:.2f}**")


