from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
from flask import Flask, request, jsonify
from textblob import TextBlob
from flask_cors import CORS
from tempfile import NamedTemporaryFile
import os
import pytesseract
from PIL import Image
from transformers import pipeline


app = Flask(__name__)
CORS(app)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

summarizer = pipeline("summarization")

def extract_text_from_file(file_stream, file_type):
    text = ""
    
    if file_type == 'pdf':
        reader = PdfReader(file_stream)
        for page in reader.pages:
            text += page.extract_text() or ''
    elif file_type in ['docx', 'pptx']:
        with NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as tmp:
            tmp.write(file_stream.read())
            tmp.close()
            if file_type == 'docx':
                doc = Document(tmp.name)
                text = '\n'.join([para.text for para in doc.paragraphs])
            elif file_type == 'pptx':
                prs = Presentation(tmp.name)
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if hasattr(shape, "text"):
                            text += shape.text + '\n'
        os.unlink(tmp.name)
    else:  
        image = Image.open(file_stream)
        text = pytesseract.image_to_string(image)
    return text


def generate_flashcards(text, num_flashcards=5):
    blob = TextBlob(text)
    sentences = [sentence.raw for sentence in blob.sentences][:num_flashcards]
    flashcards = [{'question': f"'{sentence}'?", 'answer': sentence} for sentence in sentences]
    return flashcards

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    file_type = file.filename.split('.')[-1].lower()
    text = extract_text_from_file(file.stream, file_type)
    print(text)

    num_flashcards = request.form.get('num_flashcards_limit', 15)
    flashcards = generate_flashcards(text, int(num_flashcards))
    print(flashcards)
    return jsonify({'flashcards': flashcards})

@app.route('/summarize', methods=['POST'])
def summarize_text():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    file_type = file.filename.split('.')[-1].lower()
    text = extract_text_from_file(file.stream, file_type)
    
    if not text:
        return jsonify({'error': 'No text extracted from file'}), 400

    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return jsonify({'summary': summary[0]['summary_text']})

if __name__ == '__main__':
    app.run(debug=True)
