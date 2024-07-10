import PyPDF2
import tkinter as tk
from tkinter import filedialog
import os
import re

def extract_pages(input_pdf_path, output_dir):
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

            # Nome do novo arquivo PDF
            output_pdf_path = os.path.join(output_dir, f"{nome_representante}_pagina_{i + 1}.pdf")

            # Salve o novo arquivo PDF com a página atual
            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)

            print(f"Página {i + 1} extraída para {output_pdf_path}")

def process_all_pdfs_in_directory(output_dir):
    # Obter o diretório atual onde o executável está localizado
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Iterar sobre todos os arquivos no diretório atual
    for filename in os.listdir(current_dir):
        if filename.lower().endswith('.pdf'):
            input_pdf_path = os.path.join(current_dir, filename)
            print(f"Processando {input_pdf_path}")
            extract_pages(input_pdf_path, output_dir)

def select_directory_and_process():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter

    # Selecionar o diretório de saída
    output_dir = filedialog.askdirectory(
        title="Selecione o diretório de saída"
    )
    
    if not output_dir:
        print("Nenhum diretório de saída selecionado.")
        return
    
    process_all_pdfs_in_directory(output_dir)

if __name__ == "__main__":
    select_directory_and_process()
