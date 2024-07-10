import os
import re
from flask import Flask, request, render_template, send_file
import PyPDF2
import zipfile
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXTRACTED_FOLDER'] = 'extracted'

# Crie as pastas se não existirem
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXTRACTED_FOLDER'], exist_ok=True)

def sanitize_filename(filename):
    # Substitui caracteres inválidos por um sublinhado
    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
    # Remove novas linhas e múltiplos espaços
    filename = filename.replace("\n", " ").replace("\r", " ").strip()
    filename = re.sub(r'\s+', ' ', filename)
    return filename

def extract_pages(input_pdf_path, output_dir):
    extracted_files = []
    # Abra o arquivo PDF de entrada
    with open(input_pdf_path, 'rb') as input_pdf:
        # Crie um objeto PDF reader
        reader = PyPDF2.PdfReader(input_pdf)
        
        # Itere por todas as páginas do PDF
        for i in range(len(reader.pages)):
            # Crie um novo objeto PDF writer
            writer = PyPDF2.PdfWriter()
            # Adicione a página atual ao writer
            writer.add_page(reader.pages[i])

            # Extrair o nome do representante da primeira página
            text = reader.pages[i].extract_text()
            match = re.search(r'REPRESENTANTE:\s*(\d+\s+[\w\s&]+)', text)
            if match:
                nome_representante = match.group(1).strip()
            else:
                nome_representante = f'desconhecido_{i + 1}'

            # Limpe o nome do arquivo
            nome_representante = sanitize_filename(nome_representante)

            # Nome do novo arquivo PDF
            output_pdf_path = os.path.join(output_dir, f"{nome_representante}_pagina_{i + 1}.pdf")

            # Salve o novo arquivo PDF com a página atual
            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)

            extracted_files.append(output_pdf_path)
            print(f"Página {i + 1} extraída para {output_pdf_path}")

    return extracted_files

def create_zip(files, output_dir):
    zip_path = os.path.join(output_dir, 'extracted_files.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('pdf')
    extracted_files = []
    for file in files:
        if file and file.filename.lower().endswith('.pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            extracted_files.extend(extract_pages(file_path, app.config['EXTRACTED_FOLDER']))
    
    zip_path = create_zip(extracted_files, app.config['EXTRACTED_FOLDER'])
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

