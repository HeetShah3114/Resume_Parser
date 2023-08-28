import zipfile
import re
import io
import os
import pandas as pd
import docx2txt
import spacy
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from spacy.matcher import Matcher
from nltk.corpus import stopwords

nlp = spacy.load('en_core_web_sm')

nltk_data_path = os.environ.get('NLTK_DATA')
nltk_stopwords = stopwords.words('english')

# Unzip the NLTK data if it's a zip file
if nltk_data_path.endswith('.zip'):
    with zipfile.ZipFile(nltk_data_path, 'r') as zip_ref:
        zip_ref.extractall(nltk_data_path.replace('.zip', ''))

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
            yield text
            converter.close()
            fake_file_handle.close()

def extract_text_from_docx(docx_path):
    temp = docx2txt.process(docx_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('NAME', [pattern])
    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text

def extract_mobile_number(text):
    phone_pattern = re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?')
    phone = re.findall(phone_pattern, text)
    if phone:
        number = ''.join(phone[0])
        return '+' + number if len(number) > 10 else number

def extract_email(email):
    email_pattern = re.compile(r"([^@|\s]+@[^@]+\.[^@|\s]+)")
    email = re.findall(email_pattern, email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    tokens = [token.text for token in nlp_text if not token.is_stop and token.text.lower() not in nltk_stopwords]
    data = pd.read_csv("skills.csv")
    skills = list(data.columns.values)
    skillset = []
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    for token in nlp(resume_text).noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

# ... (rest of the code)

# Calling other functions using the extracted text
name = extract_name(text)
mobile_number = extract_mobile_number(text)
email = extract_email(text)
skills = extract_skills(text)
education = extract_education(text)

print("Name: {}\nMobile Number: {}\nEmail: {}\nSkills: {}\nEducation: {}".format(name, mobile_number, email, skills, education))


# Load pre-trained model
matcher = Matcher(nlp.vocab)

STOPWORDS = set(stopwords.words('english'))

file_path = "SSKumar_Hexaware.docx"

if file_path.lower().endswith('.pdf'):
    # PDF file
    text = ''
    for page in extract_text_from_pdf(file_path):
        text += ' ' + page
elif file_path.lower().endswith('.docx'):
    # DOCX file
    text = extract_text_from_docx(file_path)
else:
    print("Unsupported file format.")
    exit()

# Calling other functions using the extracted text
name = extract_name(text)
mobile_number = extract_mobile_number(text)
email = extract_email(text)
skills = extract_skills(text)
education = extract_education(text)

print("Name: {}\nMobile Number: {}\nEmail: {}\nSkills: {}\nEducation: {}".format(name, mobile_number, email, skills, education))
