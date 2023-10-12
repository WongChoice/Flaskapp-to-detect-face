import os
from flask import Flask, request, render_template, jsonify, send_from_directory
import cv2

app = Flask(__name__)

# Load a pre-trained Haar Cascade Classifier for face detection.
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define a folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Create a folder to serve detected images
DETECTED_FOLDER = 'detected'
app.config['DETECTED_FOLDER'] = DETECTED_FOLDER

# Create the detected folder if it doesn't exist
if not os.path.exists(DETECTED_FOLDER):
    os.makedirs(DETECTED_FOLDER)

@app.route('/flaskapp/')
def index():
    return render_template('index.html', result_image_path=None)

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No selected file'})

    if image_file:
        # Save the uploaded image to the upload folder
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)

        # Load the image for detection
        image = cv2.imread(image_path)

        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save the image with detected faces
        output_filename = 'output_' + image_file.filename
        output_path = os.path.join(app.config['DETECTED_FOLDER'], output_filename)
        cv2.imwrite(output_path, image)

        # Return the path to the detected image
        return render_template('index.html', result_image_path=output_filename)

@app.route('/detected/<filename>')
def serve_detected_file(filename):
    return send_from_directory(app.config['DETECTED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
