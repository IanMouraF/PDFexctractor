import PyPDF2
import tkinter as tk
from tkinter import filedialog
import os
import re

def clean_filename(filename):
    # Remove caracteres inválidos para nomes de arquivos do Windows
    invalid_chars = '\\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    # Remove quebras de linha e espaços extras
    filename = re.sub(r'\s+', ' ', filename)
    filename = filename.strip()  # Remove espaços extras no início e fim
    return filename

def extract_pages(input_pdf_path, output_dir):
    # Abra o arquivo PDF de entrada
    with open(input_pdf_path, 'rb') as input_pdf:
        # Crie um objeto PDF reader
        reader = PyPDF2.PdfReader(input_pdf)
        
        # Itere por todas as páginas do PDF
        for i, page in enumerate(reader.pages):
            # Obtenha o texto da página para extrair o nome do representante
            page_text = page.extract_text()

            # Use expressão regular para encontrar o nome do representante
            match = re.search(r'REPRESENTANTE:\s*(.+?)(?:\n|;)', page_text, re.DOTALL)
            if match:
                representante_name = match.group(1).strip()
            else:
                representante_name = "Nome_Desconhecido"

            # Limpeza do nome do representante
            representante_name_cleaned = clean_filename(representante_name)

            # Crie um novo objeto PDF writer
            writer = PyPDF2.PdfWriter()
            # Adicione a página atual ao writer
            writer.add_page(page)

            # Nome do novo arquivo PDF
            output_pdf_path = os.path.join(output_dir, f"{representante_name_cleaned}_pagina_{i + 1}.pdf")

            # Salve o novo arquivo PDF com a página atual
            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)

            print(f"Página {i + 1} extraída para {output_pdf_path}")

def select_file_and_extract():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter

    # Selecionar o arquivo PDF
    input_pdf_path = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not input_pdf_path:
        print("Nenhum arquivo PDF selecionado.")
        return

    # Selecionar o diretório de saída
    output_dir = filedialog.askdirectory(
        title="Selecione o diretório de saída"
    )
    
    if not output_dir:
        print("Nenhum diretório de saída selecionado.")
        return
    
    extract_pages(input_pdf_path, output_dir)

if __name__ == "__main__":
    select_file_and_extract()
