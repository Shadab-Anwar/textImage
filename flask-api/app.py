from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Import CORS
import requests
import io
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the entire API
CORS(app)  # This allows requests from any origin. You can also specify the origin if needed.

# Hugging Face API Token and URL
API_URL = "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image"
headers = {"Authorization": "Bearer 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"}

# Function to send a request to Hugging Face API
def query(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Error from Hugging Face API: {response.status_code}")

# Define the route to generate the image
@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        # Get the prompt from the request
        data = request.json
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Generate the image using the Hugging Face model
        image_bytes = query(prompt)

        # Open the image from the response bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Save image to a buffer to send back in the response
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the image as a response
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="generated_image.png")

    except Exception as e:
        print("Error generating image:", str(e))
        return jsonify({"error": "Failed to generate image"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
