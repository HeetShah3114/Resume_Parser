import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import pickle
import resume

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load the serialized functions
with open('serialized_functions.pkl', 'rb') as f:
    serialized_functions = pickle.load(f)

with open('stopwords.pkl', 'rb') as f:
    STOPWORDS = pickle.load(f)

# Assign the loaded functions to variables
extract_education = serialized_functions[0]
extract_email = serialized_functions[1]
extract_mobile_number = serialized_functions[2]
extract_name = serialized_functions[3]
extract_skills = serialized_functions[4]
extract_text_from_pdf = serialized_functions[5]
extract_text_from_docx = serialized_functions[6]

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
            
            # Extract information using the serialized functions
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
