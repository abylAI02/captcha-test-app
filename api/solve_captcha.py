from http.server import BaseHTTPRequestHandler
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import json
import os

# Load the model once
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/new_model.h5)
model = load_model(MODEL_PATH)

# Character set for decoding predictions
CHAR_SET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
int_to_char = {idx: char for idx, char in enumerate(CHAR_SET)}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read and decode the incoming data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            image_bytes = np.frombuffer(post_data, dtype=np.uint8)

            # Convert bytes to image and preprocess
            image = cv2.imdecode(image_bytes, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (100, 50))
            image = image / 255.0
            image = image.reshape(1, 50, 100, 1)

            # Make predictions
            predictions = model.predict(image)
            decoded_label = ''.join([int_to_char[np.argmax(p)] for p in predictions[0]])

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'captcha_text': decoded_label}).encode())

        except Exception as e:
            # Handle errors
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())