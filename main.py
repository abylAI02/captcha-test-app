from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model("new_Model.h5")

# Character set and helper functions
CHAR_SET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHAR_TO_INT = {char: idx for idx, char in enumerate(CHAR_SET)}
INT_TO_CHAR = {idx: char for char, idx in CHAR_TO_INT.items()}

IMAGE_HEIGHT = 50
IMAGE_WIDTH = 100
MAX_LABEL_LENGTH = 6  # Adjust based on your trained model's label length

def preprocess_image(image_path):
    """Preprocess the uploaded image to feed into the model."""
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))  # Resize
    img_array = np.array(img) / 255.0  # Normalize
    img_array = img_array.reshape(1, IMAGE_HEIGHT, IMAGE_WIDTH, 1)  # Reshape
    return img_array

def decode_predictions(predictions):
    """Decode the model's predictions into readable text."""
    decoded_labels = []
    for prediction in predictions:
        decoded_label = ''.join([INT_TO_CHAR[np.argmax(char_probs)] for char_probs in prediction])
        decoded_labels.append(decoded_label)
    return decoded_labels

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'captcha' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['captcha']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save and preprocess the image
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    image = preprocess_image(file_path)

    # Predict using the model
    predictions = model.predict(image)
    decoded_label = decode_predictions(predictions)[0]

    # Clean up the uploaded file
    os.remove(file_path)

    return jsonify({'captcha_text': decoded_label})

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Create uploads directory if not exists
    app.run(debug=True)