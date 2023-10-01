# Python
import string
import random
from math import floor
from pathlib import Path
import os
# 3rd Party
import fitz  # PyMuPDF
from PyPDF2 import PdfWriter, PdfReader
from magic import from_file

# initializing size of string
N = 10

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PDF_PATH = f'{Path(__file__).resolve().parent.parent}/media/pdf/'

# Get or Create Directory
def get_or_create_dir(k):
    if Path(f'{PDF_PATH}{k}').exists():
        return f'{PDF_PATH}{k}'
    
    Path(f'{PDF_PATH}{k}').mkdir(parents=True, exist_ok=True)
    # Syntax: echo "<command>" | at now + <interval>
    os.system(f'echo rm -rf {PDF_PATH}{k} | at now + 1 hour')
    return f'{PDF_PATH}{k}'

def get_file_data(file_path):
    # Path has useful functions
    pdf_file   = Path(file_path)
    pdf_reader = PdfReader(file_path)
    file_size = pdf_file.stat().st_size
    # convert the size into an easy to read number
    if file_size > 1024:
        if file_size > 1048576:
            file_size = f'{floor(file_size / 1048576)}mb'
        else:
            file_size = f'{floor(file_size / 1024)}kb'
    else:
        file_size = f'{file_size}b'

    context = {
        "file_name": str(pdf_file.name),
        "file_size": file_size,
        "file_type": from_file(file_path, mime=True),
        "file_pages": len(pdf_reader.pages)
    }
    return context

# Create a list of file dicts
def list_files(folder_path):
    # create a list of the files in this path
    files = Path(folder_path).glob('*')
    files_list = []
    for fl in files:
        files_list.append(get_file_data(f'{folder_path}/{fl.name}'))
    
    return files_list

# create a session if not created
def make_session(request):
    if not request.session.session_key:
        request.session.create()
    return

def upload_pdf(fh, file_path):
    pdf_handler = PdfWriter()
    pdf_handler.append(fh)
    pdf_handler.write(file_path)
    pdf_handler.close()

def merge_pdf(folder_path, ordered_list):
    merger             = PdfWriter()
    # generating random strings using random.choices()
    randomized_name    = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))

    # merges the files in the order chosen by the user
    for file_obj in ordered_list:
        if file_obj["startPage"] != "False":
            start_page = int(file_obj["startPage"])-1
            if file_obj["endPage"] != "False":
                end_page = int(file_obj["endPage"])
                pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
                merger.append(pdf_file,pages=(start_page, end_page))
            else:
                pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
                merger.append(pdf_file,pages=(start_page, start_page+1))
        else:
            pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
            merger.append(pdf_file)

    # Where to save the file and what to name it
    merged_pdf = f'{folder_path}/{randomized_name}.pdf'
    merger.write(merged_pdf)
    merger.close()
    
    return merged_pdf

def split_pdf(folder_path, ordered_list):
    split_list = []
    # split the files in the order chosen by the user
    for file_obj in ordered_list:
        splitter = PdfWriter()
        if file_obj["startPage"] != "False":
            start_page = int(file_obj["startPage"])-1
            if file_obj["endPage"] != "False":
                end_page = int(file_obj["endPage"])
                pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
                splitter.append(pdf_file,pages=(start_page, end_page))
                # Where to save the file and what to name it
                splitted_pdf = f'{folder_path}/({start_page}-{end_page}){file_obj["name"]}'
            else:
                pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
                splitter.append(pdf_file,pages=(start_page, start_page+1))
                splitted_pdf = f'{folder_path}/({start_page}){file_obj["name"]}'
        else:
            continue

        split_list.append(splitted_pdf)
        splitter.write(splitted_pdf)
        splitter.close()
    
    return split_list

def compress_pdf(folder_path, ordered_list):
    compress_list = []
    # compress the files in the order chosen by the user
    for file_obj in ordered_list:
        input_pdf_path = f'{folder_path}/{file_obj["name"]}'
        output_pdf_path = f'{folder_path}/compressed-{file_obj["name"]}'

        pdf_document = fitz.open(input_pdf_path)
        pdf_document.save(output_pdf_path, garbage=4, deflate=True, clean=True)
        pdf_document.close()
        compress_list.append(f'{folder_path}/compressed-{file_obj["name"]}')
    
    return compress_list
# PyPdf2 method not very usefull
#    for file_obj in ordered_list:
#        reader = PdfReader(f'{folder_path}/{file_obj["name"]}')
#        compressor = PdfWriter()
#        for page in reader.pages:
#            page.compress_content_streams()  # This is CPU intensive!
#            compressor.add_page(page)
#
#        with open(f'{folder_path}/compressed-{file_obj["name"]}', "wb") as f:
#            compressor.write(f)
#            compressor.close()
#
#        compress_list.append(f'{folder_path}/compressed-{file_obj["name"]}')
#    
#    return compress_list