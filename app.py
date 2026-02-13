import base64
import io
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
from pix2text import Pix2Text

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests

# --- LOAD MODEL ONCE AT STARTUP ---
print("Loading Model... please wait.")
p2t = Pix2Text.from_config()
print("Model Loaded!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        # 1. Get the image data from the frontend (base64 string)
        data = request.json['image']
        
        # 2. Decode the base64 string back to an image
        header, encoded = data.split(",", 1)
        binary_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(binary_data)).convert('RGB')

        # 3. Run Inference
        # We use resized_shape ensuring it matches model expectations
        res = p2t.recognize(image, resized_shape=608)
        
        # Handle list vs dict return type (your fix)
        latex_text = res

        return jsonify({'latex': latex_text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'latex': '\\text{Error or Empty}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)