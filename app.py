from flask import Flask, render_template, request, send_file
import pdfplumber
from gtts import gTTS
import os
import time

app = Flask(__name__)

# Ensure output directory exists
OUTPUT_DIR = "static/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf' not in request.files:
        return "No file uploaded", 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return "No file selected", 400

    # Save PDF temporarily
    pdf_path = os.path.join(OUTPUT_DIR, "temp.pdf")
    pdf_file.save(pdf_path)

    # Extract text from PDF
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        return "No readable text found in the PDF.", 400

    # Convert text to speech
    tts = gTTS(text=text, lang="en")
    timestamp = str(int(time.time()))
    audio_path = os.path.join(OUTPUT_DIR, f"audio_{timestamp}.mp3")
    tts.save(audio_path)

    # Send audio file to user
    return send_file(audio_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
