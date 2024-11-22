
from flask import Flask, request, jsonify, render_template
import fitz
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Ollama model and prompt setup
template = """You are an assistant specializing in summarizing medical documents. Summarize the following content, focusing on key medical details:

{document_content}

Summary:"""
model = OllamaLLM(model="llama3:latest")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Function to extract text from any document type
def extract_text(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text") + "\n"
        return text
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_and_summarize():
    uploaded_file = request.files['file']
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    file_path = f"./uploads/{uploaded_file.filename}"
    uploaded_file.save(file_path)

    document_content = extract_text(file_path)
    if document_content:
        summary = chain.invoke({"document_content": document_content})
        return jsonify({"summary": summary})
    else:
        return jsonify({"error": "Failed to process the document"}), 500

if __name__ == '__main__':
    app.run(debug=True)
