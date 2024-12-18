from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Get Ollama API host from environment variable or use default
OLLAMA_API_HOST = os.getenv('OLLAMA_API_HOST', 'http://localhost:11434')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/models', methods=['GET'])
def get_models():
    try:
        print(f"Attempting to connect to Ollama at: {OLLAMA_API_HOST}")
        response = requests.get(f"{OLLAMA_API_HOST}/api/tags", timeout=5)
        if response.status_code != 200:
            print(f"Ollama returned status code: {response.status_code}")
            return jsonify({"error": f"Ollama returned status code: {response.status_code}"}), 500
        
        models_data = response.json()
        if 'models' not in models_data:
            # Convert old format to new format if necessary
            models = [{"name": model['name']} for model in models_data.get('models', [])]
            return jsonify({"models": models})
        return jsonify(models_data)
    except requests.exceptions.ConnectionError:
        print(f"Connection error: Could not connect to Ollama at {OLLAMA_API_HOST}")
        return jsonify({"error": "Could not connect to Ollama. Please ensure Ollama is running."}), 503
    except Exception as e:
        print(f"Error getting models: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        model = data.get('model')
        prompt = data.get('prompt', '')
        images = data.get('images', [])
        
        # Prepare the request body
        body = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        # Add images if present
        if images:
            body["images"] = images
        
        response = requests.post(
            f"{OLLAMA_API_HOST}/api/generate",
            json=body
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
            
        if file:
            # Read and encode the image
            file_data = file.read()
            base64_image = base64.b64encode(file_data).decode('utf-8')
            return jsonify({"image": base64_image})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # In Docker, we need to listen on 0.0.0.0
    app.run(host='0.0.0.0', debug=True)
