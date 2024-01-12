from flask import Flask, render_template, request
import requests
import fitz  # PyMuPDF

app = Flask(__name__)

def download_pdf(google_drive_url):
    response = requests.get(google_drive_url)
    return response.content

def extract_text_from_pdf(pdf_content):
    try:
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text
    except fitz.errors.DocumentError as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        google_drive_url = request.form.get('url')
        
        if google_drive_url:
            pdf_content = download_pdf(google_drive_url)

            if pdf_content:
                extracted_text = extract_text_from_pdf(pdf_content)
                return render_template('index.html', extracted_text=extracted_text)
            else:
                error_message = 'Invalid Google Drive URL format'
        else:
            error_message = 'Missing "url" parameter'
        
        return render_template('index.html', error_message=error_message)

    return render_template('index.html', extracted_text=None, error_message=None)

if __name__ == '__main__':
    app.run(debug=True)
