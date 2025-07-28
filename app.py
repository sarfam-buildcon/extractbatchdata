# Import required modules. Load Flask and pdfplumber for PDF parsing
from flask import Flask, request, jsonify
import pdfplumber
import io

# Create the Flask web app
app = Flask(__name__)

# Define the /extract route that handles POST requests.
@app.route('/extract', methods=['POST'])
def extract_text_only():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    # Get the uploaded PDF file
    file = request.files['file']

    # This will hold all the text lines extracted from all pages
    all_text = []

    # Open the PDF in-memory using pdfplumber
    with pdfplumber.open(io.BytesIO(file.read())) as pdf:
        # Loop through each page in the PDF
        for page in pdf.pages:
            # Extract raw text from the page
            text = page.extract_text()

            if text:
                # Split the full page text into individual lines and add to the list
                all_text.extend(text.split('\n'))

    # Return the list of text lines as JSON
    return jsonify({'text': all_text})

# Only run if you run locally (Render auto-serves without this block)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
