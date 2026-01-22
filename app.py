import os
import base64
import random
import threading
from io import BytesIO
from flask import Flask, render_template, request, jsonify, session, redirect
import cv2
import numpy as np
import pyttsx3

# --- CONFIGURATION ---
# Point Flask to the templates folder in the PARENT directory
app = Flask(__name__, template_folder='../templates')
app.secret_key = 'sign_assist_corp_secure_key_2023'

# --- TTS ENGINE SETUP ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Set a clear voice (index 0 is usually the system default)
engine.setProperty('voice', voices[0].id if voices else None)

def speak_text(text):
    """Run Text-to-Speech in a separate thread to avoid blocking the server"""
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    threading.Thread(target=run).start()

# --- MOCK AI MODEL ---
# In a real deployment, load your TensorFlow/PyTorch model here.
SIGN_LABELS = ["Hello", "Thank You", "Please", "Help", "Yes", "No", "Good Morning", "Water", "Food", "Sorry"]

def predict_sign_from_image(image_base64):
    """
    Simulates AI processing. 
    1. Decode image (simulated).
    2. Pass through neural network.
    3. Return result.
    """
    # Simulate processing time
    # return random.choice(SIGN_LABELS)
    return random.choice(SIGN_LABELS)

# --- ROUTES ---

@app.route('/')
def home():
    """Serves the Login/Dashboard Page"""
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Handles Login and sets Session"""
    data = request.json
    name = data.get('name')
    age = data.get('age')
    
    if name and age:
        session['user'] = name
        session['age'] = age
        return jsonify({'status': 'success', 'message': f'Welcome, {name}'})
    
    return jsonify({'status': 'error', 'message': 'Please provide name and age'}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    """Clears Session"""
    session.clear()
    return jsonify({'status': 'success'})

@app.route('/api/process-speech', methods=['POST'])
def process_speech():
    """
    User speaks -> Website shows Text and Signs
    """
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Logic: The frontend already transcribed the speech. 
    # Here we log it and prepare the sign response.
    
    return jsonify({
        'status': 'success',
        'original_text': text,
        'sign_instruction': f"Displaying signs for: {text}"
    })

@app.route('/api/process-text', methods=['POST'])
def process_text():
    """
    User types -> Website speaks and shows Signs
    """
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # 1. Speak the text on the server side (optional) 
    # OR send back to frontend to speak (Client-side is faster).
    # We will let the frontend handle the speaking for responsiveness.
    
    return jsonify({
        'status': 'success',
        'message': 'Processed text input'
    })

@app.route('/api/detect-sign', methods=['POST'])
def detect_sign():
    """
    User Signs (Camera) -> Website speaks and shows Text
    """
    data = request.json
    image_data = data.get('image')
    
    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400
    
    try:
        # Decode the Base64 image to process it (Simulation)
        # header, encoded = image_data.split(",", 1)
        # data = base64.b64decode(encoded)
        # nparr = np.frombuffer(data, np.uint8)
        # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Run Prediction
        detected_word = predict_sign_from_image(image_data)
        
        return jsonify({
            'status': 'success',
            'detected_text': detected_word,
            'confidence': random.uniform(0.85, 0.99) # Mock confidence score
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
