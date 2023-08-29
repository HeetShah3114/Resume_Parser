import os
import spacy
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from resume import extract_education
from resume import extract_email
from resume import extract_mobile_number
from resume import extract_name
from resume import extract_skills
from resume import extract_text_from_docx
from resume import extract_text_from_pdf

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = upload_files/
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rest of your extraction functions

# Rest of your routes and logic
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = ""
            if filename.lower().endswith('.pdf'):
                for page in extract_text_from_pdf(filepath):
                    text += ' ' + page
            elif filename.lower().endswith('.docx'):
                text = extract_text_from_docx(filepath)
            else:
                return "Unsupported file format."
            
            # Extract information using your functions
            name = extract_name(text)
            mobile_number = extract_mobile_number(text)
            email = extract_email(text)
            skills = extract_skills(text)
            education = extract_education(text)
            
            # Render the result template with extracted information
            return render_template('result.html', name=name, mobile_number=mobile_number, email=email, skills=skills, education=education)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
